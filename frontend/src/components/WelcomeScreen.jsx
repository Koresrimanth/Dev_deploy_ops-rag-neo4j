function WelcomeScreen({ onSuggestion }) {
  const suggestions = [
    {
      icon: "⌕",
      text: "Find technical specifications",
    },
    {
      icon: "◇",
      text: "Find supplier relationships",
    },
    {
      icon: "✦",
      text: "Perform a multi-agent analysis",
    },
  ];

  return (
    <div className="welcome-screen">

      <div className="welcome-logo">
        ✦
      </div>

      <h2>
        How can I help you?
      </h2>

      <p>
        Ask a question and let multiple specialized
        agents work together.
      </p>

      <div className="suggestions">

        {suggestions.map((item) => (
          <button
            key={item.text}
            onClick={() =>
              onSuggestion(item.text)
            }
          >
            <span>{item.icon}</span>
            {item.text}
          </button>
        ))}

      </div>

    </div>
  );
}

export default WelcomeScreen;