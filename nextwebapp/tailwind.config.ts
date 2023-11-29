import type { Config } from "tailwindcss";
//
const config: Config = {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        colors: {
            transparent: "transparent",
            current: "currentColor",
            white: "#FFFFFF",
            black: "#000000",
            input: "#7D7D7D",
            blackBtn: "#2D2D2D",
            blackBtnHover: "#262626",
            red: "#FC836D",
            Pika1: "#74ebd5",
            Pika2: "#acb6e5",
            Gpt1: "#f2994a",
            Gpt2: "#48b1bf",
            Mj1: "#bcd3c7",
            Mj2: "#2c3e50",
            DeepAi1: "#642b73",
            DeepAi2: "#3a6186",
            red1: "#ff4b1f",
            red2: "#2b1a3d",
            green: "#0EA982",
        },
        extend: {
            backgroundImage: {
                img: "url(../public/bg.png)",
            },
        },
    },
    plugins: [],
};
export default config;
