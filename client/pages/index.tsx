import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { useCallback, useState } from "react";

import {
  Avatar,
  ChatContainer,
  ConversationHeader,
  Message,
  MessageInput,
  MessageList,
} from "@chatscope/chat-ui-kit-react";
import Head from "next/head";

interface Message {
  role: "user" | "agent";
  text?: string;
  image?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = useCallback(
    async (_innerHTML: string, _textContent: string, innerText: string) => {
      const message: Message = { role: "user", text: innerText };
      const newMessages = [...messages, message];
      setMessages(newMessages);

      const response = await fetch("http://localhost:8000/api/input", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages.slice(-10) }),
      });

      if (!response.ok) {
        return;
        throw new Error(response.statusText);
      }

      const data = await response.json()

      setMessages(data.messages);
    },
    [messages]
  );

  return (
    <>
      <Head>
        <title>Smol-Data</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="flex flex-col items-center justify-center h-full w-full bg-slate-400">
        <main className="h-full w-full lg:h-5/6 lg:w-1/2">
          <ChatContainer>
            <ConversationHeader>
              <Avatar src="/logo.png" name="Smol-Data" />
              <ConversationHeader.Content
                userName="Smol Data"
                info="How can I help you?"
              />
            </ConversationHeader>

            <MessageList>
              {messages.map((message, index) => (
                <Message
                  key={index}
                  model={{
                    message: message.text,
                    direction:
                      message.role === "user" ? "outgoing" : "incoming",
                    position: "single",
                  }}
                />
              ))}
            </MessageList>
            <MessageInput
              placeholder="Type message here"
              attachButton={false}
              onSend={handleSend}
              sendDisabled={loading}
            />
          </ChatContainer>
        </main>
      </div>
    </>
  );
}
