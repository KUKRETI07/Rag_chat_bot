import React from 'react';
import { Plus, MessageSquare, Trash2 } from 'lucide-react';

const Sidebar = ({ chats, activeChatId, onSelectChat, onNewChat }) => {
    return (
        <div className="dark flex-shrink-0 bg-black md:w-[260px] md:flex-col">
            <div className="flex h-full min-h-0 flex-col ">
                <div className="scrollbar-trigger flex h-full w-full flex-1 items-start border-white/20">
                    <nav className="flex h-full flex-1 flex-col space-y-1 p-2">
                        <a
                            onClick={onNewChat}
                            className="flex py-3 px-3 items-center gap-3 rounded-md hover:bg-gray-500/10 transition-colors duration-200 text-white cursor-pointer text-sm mb-2 border border-white/20"
                        >
                            <Plus size={16} />
                            New chat
                        </a>
                        <div className="flex-col flex-1 overflow-y-auto border-b border-white/20">
                            <div className="flex flex-col gap-2 pb-2 text-gray-100 text-sm">
                                {chats.map((chat) => (
                                    <a
                                        key={chat.id}
                                        onClick={() => onSelectChat(chat.id)}
                                        className={`flex py-3 px-3 items-center gap-3 relative rounded-md hover:bg-[#2A2B32] cursor-pointer break-all hover:pr-4 group ${activeChatId === chat.id ? 'bg-[#343541]' : ''
                                            }`}
                                    >
                                        <MessageSquare size={16} />
                                        <div className="flex-1 text-ellipsis max-h-5 overflow-hidden break-all relative">
                                            {chat.title || 'New Chat'}
                                            <div className="absolute inset-y-0 right-0 w-8 z-10 bg-gradient-to-l from-gray-900 group-hover:from-[#2A2B32]"></div>
                                        </div>
                                    </a>
                                ))}
                            </div>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
