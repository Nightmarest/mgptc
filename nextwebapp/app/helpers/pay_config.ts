import { Neural, RatePlan } from "./types";

type PayConfig = {
    neural: Neural;
    title: RatePlan;
    amount: number;
    buytype: string;
};

export const payConfig: PayConfig[] = [
    {
        neural: "StableChatGPT",
        title: "Стандартная ~ 5$",
        amount: 480,

        buytype: "buy-0",
    },
    {
        neural: "StableChatGPT",
        title: "Расширенная ~ 10$",
        amount: 980,
        buytype: "buy-1",
    },
    {
        neural: "StableChatGPT",
        title: "Pro версия на 3 месяца ~ 24$",
        amount: 2440,
        buytype: "buy-2",
    },
    {
        neural: "PikaLabs",
        title: "Стандартная 199₽ (Месяц)",
        amount: 199,
        buytype: "buy-4",
    },
    {
        neural: "PikaLabs",
        title: "Расширенная 399₽ <br>(3 Месяца)",
        amount: 399,
        buytype: "buy-5",
    },
    {
        neural: "DeepAI",
        title: "Стандартная DeepAI 5$",
        amount: 500,
        buytype: "buy-9",
    },
    {
        neural: "DeepAI",
        title: "Расширенная DeepAI 10$",
        amount: 1000,
        buytype: "buy-10",
    },
    {
        neural: "ChatGPT4",
        title: "Стандартная подписка ~ 5$",
        amount: 480,
        buytype: "buy-6",
    },
    {
        neural: "ChatGPT4",
        title: "Расширенная подписка на <br>3 месяца ~ 12$",
        amount: 1440,
        buytype: "buy-6",
    },
    {
        neural: "Dalle3ChatGPT",
        title: "50 запросов - 300₽",
        amount: 300,
        buytype: "buy-11",
    },
    {
        neural: "Dalle3ChatGPT",
        title: "100 запросов - 550₽",
        amount: 550,
        buytype: "buy-12",
    },
    {
        neural: "Dalle3ChatGPT",
        title: "200 запросов - 900₽",
        amount: 900,
        buytype: "buy-13",
    },
];
