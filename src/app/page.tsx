import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-05 bg-white">
      <div id="chat-container">
        <div id="chat-display">
        </div>
        <form className="bg-green-100 p-5 m-2.5 fixed bottom-0 left-0 w-screen p-0">
          <input className="w-4/5 h-full p-2" type="text" id="user-input" />
          <button className="bg-green-900 text-white w-1/5 p-2.5" type="submit">Send</button>
        </form>
      </div>
    </main>
  );
}
