'use client'
import React from "react";
import Image from 'next/image'


export default function Home() {

  const URL = process.env.NEXT_PUBLIC_VERCEL_URL
  ? `https://${process.env.NEXT_PUBLIC_VERCEL_URL}/api/response`
  : "http://localhost:3000/api/response";

  // const [prompt, setPrompt] = React.useState(""); // State to store user input

  const [prompt, setPrompt] = React.useState(""); // State to store user input
  const [responseMessage, setResponseMessage] = React.useState(""); // State to store response message

  const handleResponse = async (prompt: string) => {
    try {
      const response = await fetch(`${URL}?prompt=${encodeURIComponent(prompt)}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.text();
      console.log(data)
      // Set the response message to be displayed
      setResponseMessage(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-05 bg-white">
      <div className="w-screen h-screen"  id="chat-container">
        <div className="bg-image w-screen h-screen" id="chat-display">
          {/* Display response message here */}
          <p className="bg-green-100 rounded-lg p-5 m-5 text-center text-justify">{responseMessage}</p>
        </div>
        <form className="bg-green-100 p-5 m-2.5 fixed bottom-0 left-0 w-screen p-0">
          <input
            className="w-4/5 h-full p-2"
            type="text"
            id="user-input"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)} // Update prompt state on input change
          />
          <button
            className="bg-green-900 text-white w-1/5 p-2.5"
            type="button" // Change type to button to prevent form submission
            onClick={() => handleResponse(prompt)}
          >
            Submit
          </button>
        </form>
      </div>
    </main>
  );
}