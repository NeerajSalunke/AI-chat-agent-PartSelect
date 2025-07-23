import React from "react";
import "./App.css";
import ChatWindow from "./components/ChatWindow";
import { FiZap } from "react-icons/fi";

function App() {
  return (
    <div className="App">
      <header className="hero-header">
        <div className="hero-content">

          <p className="title"><FiZap className="hero-icon" />HomeFix AI: Find & Fix Appliance Issues Fast</p>
          <p className="subtitle">
            Simply ask “What does part number PS11752778 do?” “Is this compatible with my Whirlpool fridge?” “Why is my fridge warm?”
          </p>
          <a
            href="https://partselect.com"
            target="_blank"
            rel="noopener noreferrer"
            className="cta-link"
          >
            Powered by PartSelect.com →
          </a>
          <p className="disclaimer">
            Currently supports only Dishwasher and Refrigerator parts.
            More appliance types coming soon!
          </p>
        </div>
      </header>
      <ChatWindow />
    </div>
  );
}

export default App;
