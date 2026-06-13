# 🚀 Testing Checklist - Frontend & Backend Integration

## ✅ Pre-Flight Checks

### Backend Verification
- [ ] Backend running at `http://127.0.0.1:8000`
- [ ] Verify health check: `curl http://127.0.0.1:8000/health`
- [ ] Expected response: `{"status": "ok", "service": "Agentic Geography Assistant"}`
- [ ] Check API docs: `http://127.0.0.1:8000/docs`

### Frontend Verification  
- [ ] Frontend running at `http://localhost:3000`
- [ ] CSS loads properly (Paper Design styling visible)
- [ ] Page title shows "Agentic Geography Assistant"
- [ ] Search input is visible and interactive

## 🧪 Functional Tests

### Test 1: Basic Search
1. Enter "Islamabad, Pakistan" in search box
2. Click "Search" button
3. **Expected:**
   - Search icon "🔍 Searching for: Islamabad, Pakistan" appears
   - Loading spinner shows for ~2-3 seconds
   - Text response appears with geographic information
   - One or more images load below the text

### Test 2: Response Streaming
1. Watch the response appear in real-time
2. **Expected:**
   - Text streams word-by-word (not all at once)
   - Loading spinner continues until done
   - "done" event received (invisible but logged)

### Test 3: Image Rendering
1. After response completes, check images
2. **Expected:**
   - Images display below the text response
   - Images are not placeholder/404
   - Images are related to the searched location

### Test 4: Error Handling
1. Stop the backend server
2. Try searching in the frontend
3. **Expected:**
   - Error banner appears: "Connection lost..."
   - "http://127.0.0.1:8000" mentioned in error
   - User can dismiss error and try again

### Test 5: Multiple Searches
1. Search for "Tokyo, Japan"
2. Wait for response
3. Search for "Paris, France"
4. **Expected:**
   - Previous results cleared
   - New query displays
   - New results stream in

### Test 6: Responsive Design
1. Open browser DevTools (F12)
2. Toggle device toolbar (mobile view)
3. **Expected:**
   - Layout stacks vertically on mobile
   - Input field remains usable
   - Images resize to fit screen
   - No horizontal scroll

## 🔍 Debug Checklist

### If responses aren't arriving:

**Check 1: Backend Logs**
```bash
# Terminal where backend is running - should show:
# INFO: Executing tool: get_place_info...
# INFO: Stream error: (if there's an error)
```

**Check 2: Browser Network Tab**
1. Open DevTools → Network tab
2. Perform a search
3. Look for:
   - `POST /api/chat/start` → 200 status ✓
   - `GET /api/chat/stream?...` → 200 status, streaming response ✓

**Check 3: Browser Console**
1. Open DevTools → Console tab
2. Check for errors (red messages)
3. Should NOT see:
   - CORS errors
   - "Cannot read properties of null"
   - "Failed to fetch"

**Check 4: API Key Verification**
```bash
# In backend/main.py, verify line 14 has your actual Grok API key:
os.environ["GROK_API_KEY"] = "xai-your-actual-key-here"
```

### If images aren't loading:

**Check:** Image URLs in network tab
1. DevTools → Network → search for ".png" or ".jpg"
2. Click on image request
3. Check:
   - Status should be 200
   - Headers show valid image type
   - Preview shows actual image

## 📊 Expected Server Responses

### Session Start (POST /api/chat/start)
```json
{
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Stream (GET /api/chat/stream)
```
data: {"type": "message", "text": "word "}
data: {"type": "message", "text": "by "}
data: {"type": "image", "url": "https://..."}
data: {"type": "done"}
```

## 🎨 Visual Verification

### Paper Design System Check
- [ ] Primary color (#111111 - dark gray/black) on buttons
- [ ] Secondary color (#8B5CF6 - purple) for secondary elements
- [ ] Success green (#16A34A) - not visible in current flow
- [ ] Proper spacing with 16px, 24px, 32px gaps
- [ ] Roboto font on body text
- [ ] Montserrat font on headings

### UI Elements Check
- [ ] Header with title "🌍 Geography Assistant"
- [ ] Search section in a white box with border
- [ ] Error banner appears red (#fee2e2) when errors occur
- [ ] Messages display in white boxes with shadows
- [ ] Loading spinner (rotating animation) visible during load
- [ ] Footer with attribution

## 📝 Logs to Expect

### Backend (Success Case)
```
INFO: Executing tool: get_place_info with input: {'place_name': 'Islamabad, Pakistan'}
INFO: Agent response generated successfully
INFO: Stream completed
```

### Browser Console (Success Case)
```
No errors - just normal logging
```

## ✨ Final Verification

### All Systems Go ✓
- Backend health check passes
- Frontend loads without errors
- Search for "Islamabad" returns:
  - Text response about the location
  - At least one image
  - No error messages

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Connection lost" error | Start backend: `python main.py` in backend folder |
| Images as `https://via.placeholder.com...` | Agent is returning mock data - normal fallback |
| "Cannot GET /api/chat/stream" | Backend main.py not using app routers - check main.py |
| CORS error | Restart backend after main.py changes |
| EventSource connection hangs | Check backend logs for errors, verify API key |

## 🚀 How to Test Locally

### Terminal 1 - Backend
```bash
cd backend
python main.py
# Should see: "Uvicorn running on http://127.0.0.1:8000"
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
# Should see: "Local: http://localhost:3000"
```

### Terminal 3 - Testing
```bash
# Test API directly
curl -X POST http://127.0.0.1:8000/api/chat/start \
  -H "Content-Type: application/json" \
  -d '{"query": "Islamabad"}'
```

---

**Last Updated:** 2026-06-09  
**Status:** Ready for Production Testing
