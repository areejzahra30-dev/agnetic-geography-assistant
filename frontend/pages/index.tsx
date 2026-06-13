import { useState, useEffect, useRef } from "react";
import Head from "next/head";
import styles from "./index.module.css";
import AIInput from "../components/AIInput";

interface Message {
  id: string;
  type: "text" | "image" | "error" | "loading";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Cleanup EventSource on unmount
  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  const handleSubmit = async (query: string) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setMessages([
      {
        id: `query-${Date.now()}`,
        type: "text",
        content: `🔍 Searching for: ${query}`,
      },
    ]);

    try {
      // Step 1: Start a chat session
      const baseUrl = "http://127.0.0.1:8000";
      const startResponse = await fetch(`${baseUrl}/api/chat/start`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!startResponse.ok) {
        throw new Error(`Failed to start session: ${startResponse.status}`);
      }

      const startData = await startResponse.json();
      const sessionId = startData.sessionId || startData.id;

      if (!sessionId) {
        throw new Error("No session ID returned from server");
      }

      // Step 2: Connect to SSE stream
      const streamUrl = `${baseUrl}/api/chat/stream?query=${encodeURIComponent(
        query
      )}&sessionId=${encodeURIComponent(sessionId)}`;

      // Close any existing connection
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }

      const eventSource = new EventSource(streamUrl);
      eventSourceRef.current = eventSource;

      let messageBuffer = "";
      let imageCount = 0;

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === "done") {
            setLoading(false);
            eventSource.close();
            return;
          }

          if (data.type === "error") {
            throw new Error(data.message || "Unknown error from server");
          }

          if (data.type === "message" && data.text) {
            messageBuffer += data.text;
            setMessages((prev) => {
              const lastMsg = prev[prev.length - 1];
              if (lastMsg && lastMsg.type === "text" && !lastMsg.content.startsWith("🔍")) {
                // Update last message
                return [
                  ...prev.slice(0, -1),
                  { ...lastMsg, content: messageBuffer },
                ];
              }
              return [
                ...prev,
                {
                  id: `msg-${Date.now()}`,
                  type: "text",
                  content: messageBuffer,
                },
              ];
            });
          }

          if (data.type === "image" && data.url) {
            imageCount++;
            setMessages((prev) => [
              ...prev,
              {
                id: `img-${Date.now()}-${imageCount}`,
                type: "image",
                content: data.url,
              },
            ]);
          }
        } catch (parseErr) {
          console.error("Failed to parse event:", parseErr);
          setError("Failed to parse response from server");
        }
      };

      eventSource.onerror = (err) => {
        console.error("EventSource error:", err);
        eventSource.close();
        setLoading(false);
        if (!error) {
          setError(
            "Connection lost. The server may be unreachable at http://127.0.0.1:8000"
          );
        }
      };
    } catch (err) {
      console.error("Error:", err);
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
      setLoading(false);
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    }
  };

  return (
    <>
      <Head>
        <title>Agentic Geography Assistant</title>
        <meta name="description" content="Explore geography with AI" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className={styles.page}>
        {/* Header */}
        <header className={styles.header}>
          <div className={styles.headerContent}>
            <div>
              <h1 className={styles.title}>🌍 Geography Assistant</h1>
              <p className={styles.subtitle}>
                Explore places around the world with AI-powered insights
              </p>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className={styles.main}>
          <div className={styles.container}>
            {/* Search Section */}
            <section className={styles.searchSection}>
              <AIInput onSubmit={handleSubmit} loading={loading} />
            </section>

            {/* Error Alert */}
            {error && (
              <div className={styles.errorBanner} role="alert">
                <span>⚠️ {error}</span>
                <button
                  className={styles.closeBtn}
                  onClick={() => setError(null)}
                  aria-label="Dismiss error"
                >
                  ✕
                </button>
              </div>
            )}

            {/* Results Section */}
            {messages.length > 0 ? (
              <section className={styles.resultsSection}>
                <div className={styles.messagesList}>
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`${styles.messageItem} ${styles[`type-${msg.type}`]}`}
                    >
                      {msg.type === "text" && (
                        <div className={styles.textContent}>
                          <p>{msg.content}</p>
                        </div>
                      )}
                      {msg.type === "image" && (
                        <div className={styles.imageWrapper}>
                          <img
                            src={msg.content}
                            alt="Place"
                            className={styles.image}
                            onError={(e) => {
                              (e.target as HTMLImageElement).src =
                                "https://via.placeholder.com/400x300?text=Image+Not+Available";
                            }}
                          />
                        </div>
                      )}
                      {msg.type === "error" && (
                        <div className={styles.errorMessage}>{msg.content}</div>
                      )}
                    </div>
                  ))}

                  {loading && (
                    <div className={styles.messageItem}>
                      <div className={styles.loadingIndicator}>
                        <div className={styles.spinner}></div>
                        <span>Searching for information...</span>
                      </div>
                    </div>
                  )}

                  <div ref={messagesEndRef} />
                </div>
              </section>
            ) : (
              <section className={styles.emptyState}>
                <div className={styles.emptyContent}>
                  <h2>🏙️ Welcome</h2>
                  <p>
                    Search for any city, state, or country to discover
                    fascinating geographic facts and images powered by AI.
                  </p>
                  <div className={styles.examples}>
                    <strong>Try:</strong> Islamabad, Tokyo, Paris, Sydney
                  </div>
                </div>
              </section>
            )}
          </div>
        </main>

        {/* Footer */}
        <footer className={styles.footer}>
          <p>Agentic Geography Assistant • Powered by Paper Design & FastAPI</p>
        </footer>
      </div>
    </>
  );
}