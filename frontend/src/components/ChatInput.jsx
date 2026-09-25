import { useState } from "react";

function ChatInput({ onSend, loading }) {
  const [query, setQuery] = useState("");

  function handleSend() {
    if (!query.trim() || loading) {
      return;
    }

    onSend(query);
    setQuery("");
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="input-container">

      <div className="input-box">

        <input
          value={query}
          onChange={(event) =>
            setQuery(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder="Ask NexusAI anything..."
          disabled={loading}
        />

        <button
          className="send-button"
          onClick={handleSend}
          disabled={
            loading || !query.trim()
          }
        >
          ↑
        </button>

      </div>

      <div className="input-hint">
        Press Enter to send
      </div>

    </div>
  );
}

export default ChatInput;