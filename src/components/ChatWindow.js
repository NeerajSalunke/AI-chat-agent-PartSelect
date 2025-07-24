import React, { useState, useEffect, useRef } from "react";
import "./ChatWindow.css";
import { getAIMessage } from "../api/api";
import { marked } from "marked";
import { FiSend } from "react-icons/fi";

function ChatWindow() {

  const defaultMessage = [{
    role: "assistant",
    content: "Hi, how can I help you today?"
  }];

  const [messages,setMessages] = useState(defaultMessage)
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
      scrollToBottom();
  }, [messages]);

  const handleSend = async (input) => {
    setLoading(true);
    if (input.trim() !== "") {
     
      setMessages(prevMessages => [...prevMessages, { role: "user", content: input }]);
      setInput("");

    
      const newMessage = await getAIMessage(input);
      setMessages(prevMessages => [...prevMessages, newMessage]);
    }
    setLoading(false);
  };

  return (
      <div className="messages-container">
          {messages.map((message, index) => (
              <div key={index} className={`${message.role}-message-container`}>
                  {message.content && (
                      <div className={`message ${message.role}-message`}>
                          <div dangerouslySetInnerHTML={{__html: marked(message.content).replace(/<p>|<\/p>/g, "")}}></div>
                      </div>
                  )}
              </div>
          ))}
          <div ref={messagesEndRef} />
          <div className="input-area">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={loading ? "Thinking..." : "Ask about a part..."}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  handleSend(input);
                  e.preventDefault();
                }
              }}
              disabled={loading} 
            />
            <button onClick={handleSend} title="Send message" disabled={loading}>
              {
                loading ? (
                  <div className="spinner"/>
                ) : (
                  <FiSend size={18} />
                )
              }
            </button>
          </div>
      </div>
);
}

export default ChatWindow;
