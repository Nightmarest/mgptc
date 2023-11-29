import { Neural } from "@/app/helpers/types";
import { Card } from "../SimpleComponents/Card/Card";
import { ImgButton } from "../ImgButton/ImgButtons";
import { NeuralInfoProps } from "./NeuralInfo.props";
import { Divider } from "../SimpleComponents/Divider/Divider";

const NeuralDescription: { [key in Neural]: React.ReactNode } = {
    StableChatGPT: (
        <div className="space-y-3">
            <p>
                Stable diffusion - нейросеть следующего поколения, которая
                превращает ваш текстовый запрос в произведения искусства.
            </p>
            <p>
                Chatgpt - нейросеть и универсальный текстовый помощник, решает
                любые задачи, стоит лишь спросить.
            </p>
        </div>
    ),
    ChatGPT4: (
        <p>
            Chatgpt - нейросеть и универсальный текстовый помощник, решает любые
            задачи, стоит лишь спросить.
        </p>
    ),
    DeepAI: (
        <p>
            Deep AI это - нейросеть улучшает качество изображения в 16 раз,
            выдаёт невообразимые результаты.
        </p>
    ),
    PikaLabs: (
        <p>
            Pika Labs - нейросеть превращает ваш текстовый запрос в видео
            длинную в 3 секунды.
        </p>
    ),
    Dalle3ChatGPT: (
        <div className="space-y-3">
            <p>
                Новейший CHATGPT 4 Turbo - это чат бот с искусственным
                интеллектом, подробные возможности читайте в разделе
                «Информация» и нашумевшая нейросеть для рисования Dalle 3 от
                компании Open AI.
            </p>
            <p>
                *краткий обзор на{" "}
                <a
                    href="https://youtu.be/90DXZ5AKdYo?si=i6K9L2QJPnFNeydW"
                    className="underline"
                >
                    ютубе
                </a>
            </p>
        </div>
    ),
};

export const NeuralInfo: React.FC<NeuralInfoProps> = ({
    className,
    neural,
    ...props
}) => {
    return (
        <Card
            title="Выбранная нейросеть:"
            className={`${className} space-y-3`}
            {...props}
        >
            <ImgButton disabled img={neural} />
            <Divider color="black" />
            <div className="font-medium">{NeuralDescription[neural]}</div>
        </Card>
    );
};
