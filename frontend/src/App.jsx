import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './components/Sidebar';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import { sendMessage, getHistory, getChatMessages, startNewChat } from './api';
import { Menu } from 'lucide-react';

function App() {
    const [chats, setChats] = useState([]);
    const [activeChatId, setActiveChatId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    useEffect(() => {
        loadChats();
    }, []);

    useEffect(() => {
        if (activeChatId) {
            loadMessages(activeChatId);
        } else {
            setMessages([]);
        }
    }, [activeChatId]);

    const loadChats = async () => {
        try {
            const history = await getHistory();
            setChats(history);
        } catch (error) {
            console.error("Failed to load history", error);
        }
    };

    const loadMessages = async (chatId) => {
        try {
            const msgs = await getChatMessages(chatId);
            setMessages(msgs);
        } catch (error) {
            console.error("Failed to load messages", error);
        }
    };

    const handleNewChat = async () => {
        try {
            const result = await startNewChat();
            setActiveChatId(result.chat_id);
            await loadChats();
            setSidebarOpen(false); // Close sidebar on mobile
        } catch (error) {
            console.error("Failed to start new chat", error);
        }
    };

    const handleSend = async (text) => {
        if (!text.trim()) return;

        // Optimistic update
        const newMessage = { role: 'user', content: text };
        setMessages((prev) => [...prev, newMessage]);
        setLoading(true);

        try {
            const response = await sendMessage(text, activeChatId);

            // Update chat ID if it was a new chat
            if (!activeChatId && response.chat_id) {
                setActiveChatId(response.chat_id);
                await loadChats(); // Refresh list to show new title
            }

            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: response.response },
            ]);
        } catch (error) {
            console.error("Failed to send message", error);
            setMessages((prev) => [
                ...prev,
                { role: 'assistant', content: "Error: Failed to get response from server." },
            ]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="overflow-hidden w-full h-full relative flex z-0">
            {/* Mobile Sidebar Overlay */}
            {sidebarOpen && (
                <div
                    className="fixed inset-0 bg-gray-600 bg-opacity-75 z-40 md:hidden"
                    onClick={() => setSidebarOpen(false)}
                ></div>
            )}

            {/* Sidebar */}
            <div className={`fixed inset-y-0 left-0 z-50 w-[260px] transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} bg-black`}>
                <Sidebar
                    chats={chats}
                    activeChatId={activeChatId}
                    onSelectChat={(id) => { setActiveChatId(id); setSidebarOpen(false); }}
                    onNewChat={handleNewChat}
                />
            </div>

            {/* Main Content */}
            <div className="relative flex h-full max-w-full flex-1 overflow-hidden">
                <div className="flex h-full max-w-full flex-1 flex-col">
                    {/* Mobile Header */}
                    <div className="sticky top-0 z-10 flex items-center border-b border-white/20 bg-gray-800 p-2 text-gray-200 md:hidden">
                        <button
                            type="button"
                            className="-ml-0.5 -mt-0.5 inline-flex h-10 w-10 items-center justify-center rounded-md hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                            onClick={() => setSidebarOpen(true)}
                        >
                            <span className="sr-only">Open sidebar</span>
                            <Menu size={24} />
                        </button>
                        <h1 className="flex-1 text-center text-base font-normal">RAG Chatbot</h1>
                        <button type="button" className="px-3" onClick={handleNewChat}>
                            <PlusIcon />
                        </button>
                    </div>

                    <main className="relative h-full w-full transition-width flex flex-col overflow-hidden items-stretch flex-1">
                        <div className="flex-1 overflow-hidden">
                            <div className="h-full dark:bg-gray-800">
                                <div className="h-full overflow-y-auto">
                                    <div className="flex flex-col items-center text-sm dark:bg-gray-800">
                                        {messages.length === 0 && (
                                            <div className="flex flex-col items-center justify-center h-[50vh] text-gray-800 dark:text-gray-100">
                                                <h1 className="text-4xl font-semibold mb-8">RAG Chatbot</h1>
                                                <div className="bg-gray-50 dark:bg-white/5 p-4 rounded-md max-w-md text-center">
                                                    <p>Ask questions about your handbook PDF.</p>
                                                </div>
                                            </div>
                                        )}

                                        {messages.map((msg, index) => (
                                            <ChatMessage key={index} message={msg} />
                                        ))}

                                        {loading && (
                                            <div className="w-full md:max-w-2xl lg:max-w-xl xl:max-w-3xl p-4 md:py-6 flex gap-4 m-auto">
                                                <div className="w-[30px] flex flex-col relative items-end">
                                                    <div className="relative h-[30px] w-[30px] p-1 rounded-sm bg-green-500 flex items-center justify-center">
                                                        <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                                                    </div>
                                                </div>
                                                <div className="flex items-center">
                                                    <span className="animate-pulse text-gray-500">Thinking...</span>
                                                </div>
                                            </div>
                                        )}

                                        <div className="w-full h-32 md:h-48 flex-shrink-0"></div>
                                        <div ref={messagesEndRef} />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <ChatInput onSend={handleSend} disabled={loading} />
                    </main>
                </div>
            </div>
        </div>
    );
}

const PlusIcon = () => (
    <svg stroke="currentColor" fill="none" strokeWidth="2" viewBox="0 0 24 24" strokeLinecap="round" strokeLinejoin="round" className="h-6 w-6" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
);

export default App;
