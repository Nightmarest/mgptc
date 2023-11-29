export enum State {
    promocode,
    neural,
    ratePlan,
    payment,
}

export const neurals = [
    "StableChatGPT",
    "ChatGPT4",
    "PikaLabs",
    "DeepAI",
    "Dalle3ChatGPT",
] as const;
export type Neural = (typeof neurals)[number];

export type RatePlan =
    | "Расширенная подписка <br>~ 10$"
    | "Pro версия на 3 месяца ~ 24$"
    | "Стандартная подписка ~ 5$"
    | "Расширенная подписка на <br>3 месяца ~ 12$"
    | "Стандартная 199₽ (Месяц)"
    | "Расширенная 399₽ <br>(3 Месяца)"
    | "Стандартная DeepAI 5$"
    | "Расширенная DeepAI 10$"
    | "Стандартная ~ 5$"
    | "Расширенная ~ 10$"
    | "Pro на 3 месяца ~ 28$"
    | "50 запросов - 300₽"
    | "100 запросов - 550₽"
    | "200 запросов - 900₽";

export interface Promocode {
    detail: { code: number; reason: string; discount?: number };
}

export const ratePlans: { [key in Neural]: RatePlan[] } = {
    StableChatGPT: [
        "Стандартная ~ 5$",
        "Расширенная ~ 10$",
        "Pro версия на 3 месяца ~ 24$",
    ],
    ChatGPT4: [
        "Стандартная подписка ~ 5$",
        "Расширенная подписка на <br>3 месяца ~ 12$",
    ],
    DeepAI: ["Стандартная DeepAI 5$", "Расширенная DeepAI 10$"],
    PikaLabs: ["Стандартная 199₽ (Месяц)", "Расширенная 399₽ <br>(3 Месяца)"],
    Dalle3ChatGPT: [
        "50 запросов - 300₽",
        "100 запросов - 550₽",
        "200 запросов - 900₽",
    ],
};
