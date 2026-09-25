function ChatHeader({ session }) {
  return (
    <header className="chat-header">

      <div>
        <h1>
          {session?.title || "New Chat"}
        </h1>

        <p>
          Multi-agent AI assistant
        </p>
      </div>

      <div className="online-badge">
        <span className="online-dot"></span>
        Online
      </div>

    </header>
  );
}

export default ChatHeader;