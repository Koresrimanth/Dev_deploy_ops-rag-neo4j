function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`message-row ${
        isUser ? "user-message" : "assistant-message"
      }`}
    >

      {!isUser && (
        <div className="avatar assistant-avatar">
          ✦
        </div>
      )}

      <div className="message-wrapper">

        <div className="message-name">
          {isUser ? "You" : "NexusAI"}
        </div>

        <div className="message-bubble">
          {message.content}

          {/* Execution plan */}
          {message.plan && (
            <details className="execution-plan">

              <summary>
                ✦ View execution plan
              </summary>

              <div className="plan-content">

                {message.plan.tasks?.map(
                  (task, index) => (
                    <div
                      className="plan-task"
                      key={task.id || index}
                    >

                      <div className="task-number">
                        {index + 1}
                      </div>

                      <div>
                        <strong>
                          {task.agent}
                        </strong>

                        <p>
                          {task.instruction}
                        </p>
                      </div>

                    </div>
                  )
                )}

              </div>

            </details>
          )}

        </div>

      </div>

      {isUser && (
        <div className="avatar user-avatar">
          U
        </div>
      )}

    </div>
  );
}

export default ChatMessage;