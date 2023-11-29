import { Button } from "../SimpleComponents/Button/Button";
import { ImgButtonProps, Imgs } from "./ImgButtons.props";
import Image from "next/image";
import ChatGptIcon from "@/public/ChatGpt.svg";
import ChatGptIconWhite from "@/public/ChatGptWhite.svg";
import BankCardIcon from "@/public/bankcard.svg";
import CryptoIcon from "@/public/crypto.svg";
import DeepAiIcon from "@/public/DeepAi.svg";
import { ButtonColors } from "../SimpleComponents/Button/Button.props";

const source: {
    [key in Imgs]: { content: React.ReactNode; color: ButtonColors };
} = {
    StableChatGPT: {
        content: (
            <>
                <Image
                    src="/StableDiffusion.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
                <span className="text-lg text-center font-medium">
                    StableDiffusion + ChatGPT
                </span>
                <div className="bg-white rounded-full w-[35px] h-[35px] flex items-center justify-center">
                    <ChatGptIcon className="w-[28px] h-[28px]" />
                </div>
            </>
        ),
        color: "mj",
    },
    ChatGPT4: {
        content: (
            <>
                <Image
                    src="/StableDiffusion.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
                <span className="text-lg text-center font-medium">
                    ChatGPT 4
                </span>
                <div className="w-[35px] h-[35px] border rounded-full flex items-center justify-center">
                    <ChatGptIconWhite className="h-[25px] w-[25px]" />
                </div>
            </>
        ),
        color: "gpt",
    },
    DeepAI: {
        content: (
            <>
                <Image
                    src="/StableDiffusion.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
                <span className="text-lg text-center font-medium">DeepAI</span>
                <div className="bg-white rounded-full w-[35px] h-[35px]">
                    <DeepAiIcon className="w-[35px] h-[35px]" />
                </div>
            </>
        ),
        color: "deepai",
    },
    PikaLabs: {
        content: (
            <>
                <Image
                    src="/StableDiffusion.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
                <span className="text-lg text-center font-medium">
                    Pika Labs
                </span>
                <Image
                    src="/PikaLabs.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
            </>
        ),
        color: "pika",
    },
    Dalle3ChatGPT: {
        content: (
            <>
                <Image
                    src="/StableDiffusion.jpg"
                    alt="PikaLabs"
                    width={35}
                    height={35}
                    className="rounded-full"
                    priority
                    quality={100}
                />
                <span className="text-lg text-center font-medium">
                    Dalle 3 + GPT 4 Turbo
                </span>
                <div className="bg-white rounded-full w-[35px] h-[35px] flex items-center justify-center">
                    <ChatGptIcon className="w-[28px] h-[28px]" />
                </div>
            </>
        ),
        color: "red",
    },
    BankCard: {
        content: (
            <>
                <BankCardIcon className="h-[35px] w-[35px]" />
                <span className="text-lg text-center font-medium">
                    Банковская карта
                </span>
            </>
        ),
        color: "pika",
    },
    Crypto: {
        content: (
            <>
                <CryptoIcon className="w-[40px] h-[40px] text-white" />
                <span className="text-lg text-center font-medium">
                    Криптовалюта
                </span>
            </>
        ),
        color: "mj",
    },
};

export const ImgButton: React.FC<ImgButtonProps> = ({
    className,
    img,
    ...props
}) => {
    return (
        <Button
            className={`${className} w-full grid grid-cols-[35px_auto_35px] items-center gap-x-1`}
            {...props}
            color={source[img].color}
        >
            {source[img].content}
        </Button>
    );
};
