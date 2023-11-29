import { Accordion } from "../SimpleComponents/Accordion/Accordion";
import { ImgAccordionProps } from "./ImgAccordion.props";
import { Neural, RatePlan, State } from "@/app/helpers/types";
import Image from "next/image";
import ChatGptIcon from "@/public/ChatGpt.svg";
import DeepAiIcon from "@/public/DeepAi.svg";
import { Divider } from "../SimpleComponents/Divider/Divider";
import { Button } from "../SimpleComponents/Button/Button";

const source: { [key in Neural]: React.ReactNode } = {
    StableChatGPT: (
        <Image
            src="/StableDiffusion.jpg"
            width={35}
            height={35}
            alt="PikaLabs"
            priority
            quality={100}
            className="rounded-full"
        />
    ),
    ChatGPT4: (
        <div className="bg-white rounded-full w-[35px] h-[35px] flex items-center justify-center">
            <ChatGptIcon className="w-[28px] h-[28px]" />
        </div>
    ),
    PikaLabs: (
        <Image
            src="/PikaLabs.jpg"
            width={35}
            height={35}
            alt="PikaLabs"
            priority
            quality={100}
            className="rounded-full"
        />
    ),
    DeepAI: (
        <div className="bg-white rounded-full w-[35px] h-[35px] flex items-center justify-center">
            <DeepAiIcon className="w-[35px] h-[35px]" />
        </div>
    ),
    Dalle3ChatGPT: (
        <div className="bg-white rounded-full w-[35px] h-[35px] flex items-center justify-center">
            <ChatGptIcon className="w-[28px] h-[28px]" />
        </div>
    ),
};

type RatePlanInfo = {
    [key in RatePlan]?: {
        content: React.ReactNode;
        color: "one" | "three" | "four" | "six" | "two";
    };
};

const ratePlansInfo: { [key in Neural]: RatePlanInfo } = {
    ChatGPT4: {
        "Стандартная подписка ~ 5$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>Безлимит запросов</li>
                    <li>GPT Voice</li>
                </ul>
            ),
            color: "one",
        },
        "Расширенная подписка на <br>3 месяца ~ 12$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>Безлимит запросов</li>
                    <li>GPT Voice</li>
                </ul>
            ),
            color: "two",
        },
    },
    DeepAI: {
        "Стандартная DeepAI 5$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>250 генераций</li>
                </ul>
            ),
            color: "one",
        },
        "Расширенная DeepAI 10$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>500 генераций</li>
                </ul>
            ),
            color: "two",
        },
    },
    PikaLabs: {
        "Стандартная 199₽ (Месяц)": {
            content: (
                <>
                    <ul className="list-disc pl-4 space-y-1">
                        <li>Полный безлимит генераций</li>
                    </ul>
                    <Divider color="white" />
                    <p>* Твори сколько угодно видео контента</p>
                </>
            ),
            color: "one",
        },
        "Расширенная 399₽ <br>(3 Месяца)": {
            content: (
                <>
                    <ul className="list-disc pl-4 space-y-1">
                        <li>Полный безлимит генераций</li>
                    </ul>
                    <Divider color="white" />
                    <p>* Твори сколько угодно контента и сэкономь деньги</p>
                </>
            ),
            color: "four",
        },
    },
    StableChatGPT: {
        "Стандартная ~ 5$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>350 генераций в месяц</li>
                    <li>ChatGPT 200 генераций</li>
                    <li>Быстрые генерации</li>
                    <li>Высокое качество</li>
                    <li>Различные модули и функции</li>
                    <li>Доступ к закрытому сообществу</li>
                </ul>
            ),
            color: "one",
        },
        "Расширенная ~ 10$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>Безлимит генераций SD</li>
                    <li>Безлимит ChatGPT</li>
                    <li>Быстрые генерации</li>
                    <li>Высокое качество</li>
                    <li>Различные модули и функции</li>
                    <li>Готовые промты</li>
                    <li>Доступ к закрытому сообществу</li>
                    <li>Отсутствие цензурны 18+</li>
                </ul>
            ),
            color: "two",
        },
        "Pro версия на 3 месяца ~ 24$": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>Полный безлимит генераций </li>
                    <li>Быстрые генерации</li>
                    <li>Безлимит ChatGPT</li>
                    <li>Высокое качество</li>
                    <li>Различные модули и функции</li>
                    <li>Готовые промты</li>
                    <li>Доступ к закрытому сообществу</li>
                    <li>Мини курс по Stable Diffusion</li>
                </ul>
            ),
            color: "four",
        },
    },
    Dalle3ChatGPT: {
        "50 запросов - 300₽": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>
                        50 токенов на использование ChatGPT 4 Turbo + Dalle 3
                    </li>
                </ul>
            ),
            color: "one",
        },
        "100 запросов - 550₽": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>
                        100 токенов на использование ChatGPT 4 Turbo + Dalle 3
                    </li>
                </ul>
            ),
            color: "two",
        },
        "200 запросов - 900₽": {
            content: (
                <ul className="list-disc pl-4 space-y-1">
                    <li>
                        200 токенов на использование ChatGPT 4 Turbo + Dalle 3
                    </li>
                </ul>
            ),
            color: "four",
        },
    },
};

export const ImgAccordion: React.FC<ImgAccordionProps> = ({
    className,
    setOpened,
    setRatePlan,
    setState,
    disabled,
    opened,
    title,
    neural,
}) => {
    const Img = source[neural];

    const chooseRatePlan = () => {
        if (setRatePlan && setState && setOpened) {
            setRatePlan(title);
            setState(State.payment);
            setOpened(null);
        }
    };

    if (ratePlansInfo[neural][title]) {
        return (
            <Accordion
                color={ratePlansInfo[neural][title]?.color}
                title={title}
                className={`${className}`}
                setOpened={setOpened}
                opened={opened}
                setState={setState}
                disabled={disabled}
            >
                <div className="grid grid-cols-[35px_auto] items-center gap-x-2 w-full ">
                    {Img}
                    <h2
                        className="text-lg text-left"
                        dangerouslySetInnerHTML={{ __html: title }}
                    ></h2>
                </div>
                <div>
                    <div className="px-3 py-2 text-base space-y-2">
                        <h3>Вы получите:</h3>
                        {ratePlansInfo[neural][title]?.content}
                    </div>
                    <Button
                        color="black"
                        className="w-full"
                        onClick={chooseRatePlan}
                    >
                        Выбрать
                    </Button>
                </div>
            </Accordion>
        );
    }
};
