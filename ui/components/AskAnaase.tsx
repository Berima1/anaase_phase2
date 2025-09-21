import { useState } from "react";

export default function AskAnaase() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    setAnswer(null);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Failed to get an answer. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className="mt-12 max-w-xl mx-auto p-4 bg-gray-100 rounded-lg shadow-md">
      <input
        type="text"
        placeholder="Ask Anaasɛ..."
        className="w-full p-3 rounded border border-gray-300 mb-4"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button
        onClick={handleAsk}
        className="bg-gold text-black px-6 py-2 rounded font-semibold hover:bg-yellow-400"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>
      {answer && <div className="mt-4 p-4 bg-white rounded shadow">{answer}</div>}
    </div>
  );
}
