import React, { useState } from "react";
import "./App.css";
import ChatWindow from "./components/ChatWindow";

function App() {

  return (
    <div className="App">
      <div className="heading">
        AI-powered Appliance Part Assistant for&nbsp;<a href="https://partselect.com" target="_blank">partselect.com</a> 
      </div>
        <ChatWindow/>
    </div>
  );
}

export default App;
