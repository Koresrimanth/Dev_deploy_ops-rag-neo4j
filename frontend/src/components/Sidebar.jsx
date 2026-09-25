function Sidebar({
  sessions,
  activeSessionId,
  onNewChat,
  onSelectSession,
}) {
  return (
    <aside className="sidebar">

      {/* Logo */}
      <div className="brand">
        <div className="brand-icon">✦</div>
        <span>NexusAI</span>
      </div>

      {/* New Chat */}
      <button
        className="new-chat-button"
        onClick={onNewChat}
      >
        <span className="plus-icon">＋</span>
        New Chat
      </button>

      {/* Sessions */}
      <div className="sessions-section">

        <div className="sessions-title">
          RECENT CHATS
        </div>

        <div className="sessions-list">

          {sessions.length === 0 && (
            <div className="no-sessions">
              No previous chats
            </div>
          )}

          {sessions.map((session) => (
            <button
              key={session.id}
              className={`session-item ${
                activeSessionId === session.id
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                onSelectSession(session.id)
              }
            >
              <span className="chat-icon">
                ◌
              </span>

              <span className="session-title">
                {session.title}
              </span>
            </button>
          ))}

        </div>
      </div>

      {/* Agents */}
      <div className="agents-section">

        <div className="sessions-title">
          ACTIVE AGENTS
        </div>

        <div className="agent-item">
          <div className="agent-symbol planner">
            ✦
          </div>

          <div className="agent-info">
            <div>Planner</div>
            <span>Task orchestration</span>
          </div>

          <span className="agent-status"></span>
        </div>

        <div className="agent-item">
          <div className="agent-symbol rag">
            ⌕
          </div>

          <div className="agent-info">
            <div>RAG Agent</div>
            <span>Document intelligence</span>
          </div>

          <span className="agent-status"></span>
        </div>

        <div className="agent-item">
          <div className="agent-symbol graph">
            ◇
          </div>

          <div className="agent-info">
            <div>Graph Agent</div>
            <span>Knowledge graph</span>
          </div>

          <span className="agent-status"></span>
        </div>

      </div>

      {/* Bottom */}
      <div className="sidebar-bottom">
        <span className="online-dot"></span>
        All systems operational
      </div>

    </aside>
  );
}

export default Sidebar;