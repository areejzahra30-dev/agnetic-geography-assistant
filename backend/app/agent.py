"""
Agent orchestration using OpenAI Agents SDK + litellm + grok-3-fast
and MCP tool connectors for Apify (web scraping) and Pexels (images).
"""

import json
import logging
import asyncio
from typing import AsyncGenerator
import litellm
from app.config import GROK_API_KEY, GROK_MODEL, MCP_APIFY_HEADER, PEXELS_API_KEY

logger = logging.getLogger(__name__)

# Configure litellm for grok-3-fast via OpenAI-compatible API
litellm.set_verbose = True


class AgentOrchestrator:
    """
    Orchestrates the agent that:
    1. Receives a place query
    2. Calls tool functions for place info (MCP Apify placeholder)
    3. Calls tool functions for images (MCP Pexels placeholder)
    4. Uses grok-3-fast (via litellm) to compose a natural response
    5. Returns structured JSON with description + image URLs
    """
    
    def __init__(self):
        self.model = GROK_MODEL  # "grok-3-fast"
        self.api_key = GROK_API_KEY
        self.tools = self._define_tools()
    
    def _define_tools(self) -> list:
        """Define tool schema for agent to use"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_place_info",
                    "description": "Retrieve geographical and cultural information about a place using web scraping (MCP Apify)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "place_name": {"type": "string", "description": "Name of the place (city, state, or country)"},
                        },
                        "required": ["place_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_place_images",
                    "description": "Search for images of a place using MCP Pexels integration",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "place_name": {"type": "string", "description": "Name of the place to search images for"},
                            "count": {"type": "integer", "description": "Number of images to return", "default": 3},
                        },
                        "required": ["place_name"],
                    },
                },
            },
        ]
    
    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """Execute a tool and return result as JSON string"""
        logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
        
        if tool_name == "get_place_info":
            # TODO: Integrate with MCP Apify server for real web scraping
            place_name = tool_input.get("place_name", "Unknown")
            info = {
                "place": place_name,
                "description": f"{place_name} is a fascinating destination with rich history and culture.",
                "population": "~13.9 million" if "Tokyo" in place_name else "Unknown",
                "coordinates": {"lat": 35.6762, "lon": 139.6503} if "Tokyo" in place_name else None,
                "notable_features": [
                    "Historic temples and shrines",
                    "Modern technology hub",
                    "Vibrant street culture",
                ] if "Tokyo" in place_name else [],
            }
            return json.dumps(info)
        
        elif tool_name == "search_place_images":
            # TODO: Integrate with MCP Pexels server for real image search
            place_name = tool_input.get("place_name", "Unknown")
            count = tool_input.get("count", 3)
            # Placeholder image URLs (in production, these come from Pexels MCP)
            images = [
                f"https://images.pexels.com/photos/placeholder-{i}?auto=compress&cs=tinysrgb&w=500" 
                for i in range(count)
            ]
            return json.dumps({"images": images, "count": len(images)})
        
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
    async def query_place(self, place_name: str) -> dict:
        """
        Query place information and images using grok-3-fast agent.
        
        Returns:
        {
            "place": "Tokyo, Japan",
            "description": "...",
            "image_urls": ["..."],
            "sources": ["..."],
        }
        """
        if not self.api_key:
            logger.warning("GROK_API_KEY not set; using mock response")
            return self._generate_response(place_name)
        
        try:
            from concurrent.futures import ThreadPoolExecutor
            
            # Wrap the synchronous litellm call to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as executor:
                # Add 10-second timeout for the API call
                response = await asyncio.wait_for(
                    loop.run_in_executor(
                        executor,
                        self._call_litellm,
                        place_name
                    ),
                    timeout=10.0
                )
            
            if response is None:
                logger.warning(f"Litellm returned None for {place_name}")
                return self._generate_response(place_name)
            
            # Process tool calls if any
            description = ""
            image_urls = []
            
            if response.choices[0].message.content:
                description = response.choices[0].message.content
            
            # Handle tool use (if the model called tools)
            if hasattr(response.choices[0].message, "tool_calls") and response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)
                    tool_result = self._execute_tool(tool_name, tool_input)
                    
                    if tool_name == "search_place_images":
                        try:
                            result_json = json.loads(tool_result)
                            image_urls.extend(result_json.get("images", []))
                        except json.JSONDecodeError:
                            pass
                    elif tool_name == "get_place_info":
                        try:
                            result_json = json.loads(tool_result)
                            if not description:
                                description = result_json.get("description", "")
                        except json.JSONDecodeError:
                            pass
            
            return {
                "place": place_name,
                "description": description or f"Information about {place_name}",
                "image_urls": image_urls or self._get_fallback_images(place_name),
                "sources": ["grok-3-fast agent"],
            }
        
        except asyncio.TimeoutError:
            logger.error(f"Litellm call timed out for {place_name}")
            return self._generate_response(place_name)
        except Exception as e:
            logger.error(f"Agent error: {e}", exc_info=True)
            return self._generate_response(place_name)
    
    def _call_litellm(self, place_name: str):
        """Synchronous wrapper for litellm completion"""
        try:
            messages = [
                {
                    "role": "user",
                    "content": f"Tell me about {place_name}. Use the available tools to get current information and images.",
                }
            ]
            
            response = litellm.completion(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
                api_key=self.api_key,
                temperature=0.7,
                timeout=8,  # 8-second timeout for the actual API call
            )
            return response
        except Exception as e:
            logger.error(f"Litellm error: {e}")
            return None
    
    def _generate_response(self, place_name: str) -> dict:
        """Generate a realistic response without API call"""
        descriptions = {
            "islamabad": "Islamabad is the capital city of Pakistan, located in the north-central part of the country. Known for its strategic location at the foot of the Margalla Hills, it's a well-planned city with modern architecture and green spaces. The city is famous for the Faisal Mosque, one of the largest mosques in the world, and serves as the political and administrative center of Pakistan. Islamabad offers stunning views of surrounding mountains and is known for its pleasant climate.",
            "tokyo": "Tokyo is the vibrant capital city of Japan, known for its blend of ancient traditions and cutting-edge technology. From historic temples and traditional gardens to futuristic skyscrapers and neon-lit streets, Tokyo offers a unique cultural experience. The city is famous for its cherry blossoms, incredible food scene, organized public transportation system, and friendly people. It's one of the world's largest metropolitan areas with a rich history spanning centuries.",
            "paris": "Paris, the City of Light, is the capital of France and one of the world's most romantic and culturally significant cities. Famous landmarks include the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral, and Arc de Triomphe. The city is renowned for its world-class art museums, charming cafés, exquisite cuisine, and picturesque streets lined with historic architecture. Paris remains a global center for art, fashion, culture, and education.",
            "sydney": "Sydney is Australia's largest city and the capital of New South Wales, renowned for its stunning harbor and iconic landmarks. The Sydney Opera House and Harbour Bridge are world-famous symbols of the city. Known for its beautiful beaches, vibrant culture, and outdoor lifestyle, Sydney offers a diverse mix of attractions including museums, galleries, botanical gardens, and excellent restaurants. The city enjoys a temperate climate and is a gateway to exploring Australia's unique natural beauty.",
        }
        
        # Get description (default to generic if place not in dictionary)
        place_lower = place_name.lower()
        description = descriptions.get(place_lower)
        if not description:
            description = f"{place_name} is a fascinating place with rich cultural heritage, beautiful landscapes, and interesting history. It's worth visiting to explore its unique attractions, local cuisine, and meet the friendly people who call it home."
        
        return {
            "place": place_name,
            "description": description,
            "image_urls": self._get_fallback_images(place_name),
            "sources": ["fallback-response"],
        }

    def _get_fallback_images(self, place_name: str) -> list:
        """Return generic fallback images if no specific images are found"""
        return [
            "https://images.unsplash.com/photo-1469022563149-aa64dbd37dae?w=600&q=80",
            "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600&q=80",
        ]

    async def stream_place_info(self, place_name: str) -> AsyncGenerator:
        """
        Generator that yields progressive chunks of place info for SSE streaming.
        Streams description chunks first, then images.
        """
        systemPrompt = (
            "You are a Geography Assistant. "
            "Provide a clean, natural overview of the destination. "
            "Do not repeat the template query text."
        )
        userPrompt = f"Tell me about {place_name}."

        logging.info("Querying place: %s", place_name)
        response = await self.query_place(place_name)
        logging.info("Response: %s", response)

        if not response:
            logging.error("No response received")
            return

        description = response.get("description", "")
        chunks = description.split()

        for chunk in chunks:
            yield {
                "type": "message",
                "text": chunk + " ",
            }
            # Simulate streaming delay
            await asyncio.sleep(0.02)
        
        # Stream images
        for idx, image_url in enumerate(response.get("image_urls", [])):
            yield {
                "type": "image",
                "url": image_url,
            }
            await asyncio.sleep(0.05)


_agent = None


def get_agent() -> AgentOrchestrator:
    global _agent
    if _agent is None:
        _agent = AgentOrchestrator()
    return _agent