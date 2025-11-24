import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Copy, Check } from 'lucide-react';
import { useState } from 'react';

const ChatMessage = ({ message }) => {
    const isUser = message.role === 'user';
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(message.content);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className={`group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 ${isUser ? 'dark:bg-gray-800' : 'bg-gray-50 dark:bg-[#444654]'}`}>
            <div className="text-base gap-4 md:gap-6 md:max-w-2xl lg:max-w-xl xl:max-w-3xl p-4 md:py-6 flex lg:px-0 m-auto">
                <div className="w-[30px] flex flex-col relative items-end">
                    <div className={`relative h-[30px] w-[30px] p-1 rounded-sm flex items-center justify-center ${isUser ? 'bg-indigo-500' : 'bg-green-500'}`}>
                        {isUser ? <User size={20} className="text-white" /> : <Bot size={20} className="text-white" />}
                    </div>
                </div>
                <div className="relative flex-1 overflow-hidden">
                    <div className="prose dark:prose-invert max-w-none">
                        <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                </div>
                {!isUser && (
                    <div className="md:invisible group-hover:visible flex self-start">
                        <button
                            onClick={handleCopy}
                            className="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
                        >
                            {copied ? <Check size={16} /> : <Copy size={16} />}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ChatMessage;
