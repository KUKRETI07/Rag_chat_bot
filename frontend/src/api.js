import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message, chatId) => {
    const response = await api.post('/ask', { message, chat_id: chatId });
    return response.data;
};

export const getHistory = async () => {
    const response = await api.get('/history');
    return response.data;
};

export const getChatMessages = async (chatId) => {
    const response = await api.get(`/history/${chatId}`);
    return response.data;
};

export const startNewChat = async () => {
    const response = await api.post('/new');
    return response.data;
};

export default api;
