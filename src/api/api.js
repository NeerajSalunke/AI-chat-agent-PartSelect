export const getAIMessage = async (userQuery) => {
  try {
    const response = await fetch("https://ai-chat-agent-partselect-1.onrender.com/api/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ query: userQuery })
    });

    const data = await response.json();
    console.log(data);
    console.log(data.content);

    return {
      role: "assistant",
      content: data.content || "Sorry, I didn't understand that."
    };

  } catch (error) {
    console.error("Error communicating with backend:", error);
    return {
      role: "assistant",
      content: "Oops! Something went wrong while contacting the backend."
    };
  }
};
