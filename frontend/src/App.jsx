import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatHeader from "./components/ChatHeader";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import WelcomeScreen from "./components/WelcomeScreen";

import { sendMessage } from "./services/api";

function App() {

  /*
   * Each session contains:
   *
   * {
   *   id,
   *   title,
   *   messages
   * }
   */

  const [sessions, setSessions] = useState([]);

  const [activeSessionId, setActiveSessionId] =
    useState(null);

  const [loading, setLoading] = useState(false);


  // Get current session
  const activeSession = sessions.find(
    (session) =>
      session.id === activeSessionId
  );


  // Create a new chat
  function createNewChat() {

    const newSession = {
      id: crypto.randomUUID(),
      title: "New Chat",
      messages: [],
    };

    setSessions((prev) => [
      newSession,
      ...prev,
    ]);

    setActiveSessionId(newSession.id);
  }


  // Select old session
  function selectSession(sessionId) {
    setActiveSessionId(sessionId);
  }


  // Send message
  async function handleSend(query) {

    let sessionId = activeSessionId;

    /*
     * If user sends a message without
     * creating a chat first, create one.
     */
    if (!sessionId) {

      const newSession = {
        id: crypto.randomUUID(),
        title: query.slice(0, 35),
        messages: [],
      };

      sessionId = newSession.id;

      setSessions((prev) => [
        newSession,
        ...prev,
      ]);

      setActiveSessionId(sessionId);
    }


    // Add user message
    const userMessage = {
      role: "user",
      content: query,
    };

    setSessions((prev) =>
      prev.map((session) => {

        if (session.id !== sessionId) {
          return session;
        }

        return {
          ...session,

          title:
            session.messages.length === 0
              ? query.slice(0, 35)
              : session.title,

          messages: [
            ...session.messages,
            userMessage,
          ],
        };
      })
    );


    setLoading(true);


    try {

      const data = await sendMessage(query);

      const assistantMessage = {
        role: "assistant",
        content: data.answer,
        plan: data.plan,
        agent_results: data.agent_results,
      };


      setSessions((prev) =>
        prev.map((session) => {

          if (session.id !== sessionId) {
            return session;
          }

          return {
            ...session,
            messages: [
              ...session.messages,
              assistantMessage,
            ],
          };

        })
      );

    } catch (error) {

      const errorMessage = {
        role: "assistant",
        content:
          "Sorry, something went wrong: " +
          error.message,
      };

      setSessions((prev) =>
        prev.map((session) => {

          if (session.id !== sessionId) {
            return session;
          }

          return {
            ...session,
            messages: [
              ...session.messages,
              errorMessage,
            ],
          };

        })
      );

    } finally {

      setLoading(false);

    }
  }


  return (
    <div className="app">

      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onNewChat={createNewChat}
        onSelectSession={selectSession}
      />


      <main className="main">

        <ChatHeader
          session={activeSession}
        />


        <div className="messages">

          {!activeSession ||
          activeSession.messages.length === 0 ? (

            <WelcomeScreen
              onSuggestion={handleSend}
            />

          ) : (

            <>
              {activeSession.messages.map(
                (message, index) => (
                  <ChatMessage
                    key={index}
                    message={message}
                  />
                )
              )}

              {loading && (
                <div className="thinking-message">

                  <div className="avatar assistant-avatar">
                    ✦
                  </div>

                  <div>
                    <div className="message-name">
                      NexusAI
                    </div>

                    <div className="thinking">
                      <span></span>
                      <span></span>
                      <span></span>

                      <label>
                        Agents are working...
                      </label>
                    </div>
                  </div>

                </div>
              )}
            </>

          )}

        </div>


        <ChatInput
          onSend={handleSend}
          loading={loading}
        />

      </main>

    </div>
  );
}

export default App;