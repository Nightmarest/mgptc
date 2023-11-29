"use client";

import { useEffect, useState } from "react";
import { Neural, RatePlan, State } from "./helpers/types";
import { AnimatePresence, motion } from "framer-motion";
import Image from "next/image";
import { Card } from "./components/SimpleComponents/Card/Card";
import { Button } from "./components/SimpleComponents/Button/Button";
import { PromocodeMenu } from "./components/PromocodeMenu/PromocodeMenu";
import { NeuralMenu } from "./components/NeuralMenu/NeuralMenu";
import { RatePlanMenu } from "./components/RatePlanMenu/RatePlanMenu";
import { ImgButton } from "./components/ImgButton/ImgButtons";
import { ImgAccordion } from "./components/ImgAccordion/ImgAccordion";
import { NeuralInfo } from "./components/NeuralInfo/NeuralInfo";
import { Divider } from "./components/SimpleComponents/Divider/Divider";
import { PaymentMenu } from "./components/PaymentMenu/PaymentMenu";

const titles = {
    0: "Введите промокод на покупку, <br> если он имеется",
    1: "Выберите нейросеть",
    2: "Выберите ваш тарифный план",
    3: "Выберите метод оплаты",
};

export default function Home() {
    const [state, setState] = useState<State>(State.promocode);
    const [discount, setDiscount] = useState<number>(0);
    const [neural, setNeural] = useState<Neural | null>(null);
    const [ratePlan, setRatePlan] = useState<RatePlan | null>(null);

    const comeBack = () => {
        setState(state - 1);
    };

    useEffect(() => {
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    });

    return (
        <div className="min-h-screen p-5 overflow-hidden">
            <div className="h-screen w-screen fixed top-0 left-0 -z-50">
                <Image
                    src="/bg.jpg"
                    alt="background"
                    fill
                    priority
                    quality={100}
                    style={{ objectFit: "cover" }}
                />
            </div>
            <motion.div
                className="grid w-[calc(200vw-40px)] mb-4 grid-cols-[calc(100vw-40px)_calc(100vw-40px)] gap-x-10"
                initial={{ x: 0 }}
                animate={
                    state === State.ratePlan || state === State.payment
                        ? { x: "-100vw" }
                        : { x: "0" }
                }
                transition={{ duration: 0.7, type: "spring" }}
            >
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                    <Button
                        className="text-lg font-medium w-fit px-4"
                        color="mj"
                        disabled
                    >
                        Покупка подписки
                    </Button>
                </motion.div>
                <Button
                    color="mj"
                    onClick={comeBack}
                    className="font-medium text-lg w-fit px-4"
                >
                    Вернуться назад
                </Button>
            </motion.div>
            <AnimatePresence>
                {state == State.promocode && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute w-[calc(100vw-40px)]"
                    >
                        <Card
                            className="text-sm font-medium"
                            title={titles[state]}
                        >
                            <PromocodeMenu
                                setState={setState}
                                setDiscount={setDiscount}
                            />
                        </Card>
                    </motion.div>
                )}
            </AnimatePresence>
            <AnimatePresence>
                {state == State.neural && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute w-[calc(100vw-40px)]"
                    >
                        <Card
                            className="text-sm font-medium"
                            title={titles[state]}
                        >
                            <NeuralMenu
                                setState={setState}
                                setNeural={setNeural}
                            />
                        </Card>
                    </motion.div>
                )}
            </AnimatePresence>
            <AnimatePresence>
                {state == State.ratePlan && neural && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute w-[calc(100vw-40px)]"
                    >
                        <Card
                            className="text-sm font-medium mb-4 "
                            title={
                                neural !== "Dalle3ChatGPT"
                                    ? "Выберите ваш тарифный план"
                                    : "Единоразовая  покупка запросов"
                            }
                        >
                            <RatePlanMenu
                                neural={neural}
                                setRatePlan={setRatePlan}
                                setState={setState}
                            />
                        </Card>
                        <NeuralInfo neural={neural} />
                    </motion.div>
                )}
            </AnimatePresence>
            <AnimatePresence>
                {state === State.payment && ratePlan && neural && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute w-[calc(100vw-40px)]"
                    >
                        <Card
                            className="text-sm font-medium mb-4 "
                            title={titles[state]}
                        >
                            <PaymentMenu
                                neural={neural}
                                ratePlan={ratePlan}
                                discount={discount}
                            />
                        </Card>
                        <Card
                            title="Выбранная нейросеть:"
                            className="space-y-3"
                        >
                            <ImgButton disabled img={neural}></ImgButton>
                            <Divider color="black" />
                            <h4 className="font-medium text-lg">
                                Выбранный тарифный план:
                            </h4>
                            <ImgAccordion
                                title={ratePlan}
                                neural={neural}
                                disabled
                            />
                        </Card>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
