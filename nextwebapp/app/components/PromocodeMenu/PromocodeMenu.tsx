"use client";

import { useRef, useState } from "react";
import { Button } from "../SimpleComponents/Button/Button";
import { Input } from "../SimpleComponents/Input/Input";
import { PromocodeMenuProps } from "./PromocodeMenu.props";
import { Promocode, State } from "../../helpers/types";

export const PromocodeMenu: React.FC<PromocodeMenuProps> = ({
    setState,
    setDiscount,
}) => {
    const promocodeRef = useRef<HTMLInputElement>(null);
    const [code, setCode] = useState<Promocode | undefined>(undefined);

    const EnterPromocode = async () => {
        if (code === undefined || code.detail.code != 0) {
            if (promocodeRef.current?.value) {
                const formData = new FormData();
                formData.append("promo", promocodeRef.current.value);
                formData.append("chatid", "1223414423");
                const response = await fetch(
                    "https://gpt.apicluster.ru/pay/promocode/",
                    { method: "POST", body: formData }
                );
                const data: Promocode = await response.json();
                setCode(data);
            }
        } else {
            setState(State.neural);
            if (code.detail.discount) {
                setDiscount(code.detail.discount);
            }
        }
    };

    const noPromo = () => {
        setState(State.neural);
    };

    return (
        <div className="space-y-3">
            <Input placeholder="Промокод..." ref={promocodeRef} code={code} />
            <Button className="w-full text-base" color="gpt" onClick={noPromo}>
                Без промокода
            </Button>
            <Button
                color="pika"
                onClick={EnterPromocode}
                className="w-full text-base"
            >
                {code && code.detail.code == 0
                    ? "Перейти дальше"
                    : "Использовать"}
            </Button>
        </div>
    );
};
