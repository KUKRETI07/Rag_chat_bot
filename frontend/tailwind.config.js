/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'gpt-dark': '#343541',
                'gpt-gray': '#444654',
                'gpt-light': '#ECECF1',
            }
        },
    },
    plugins: [],
}
