import { ForwardedRef, forwardRef } from "react";
import { InputProps } from "./Input.props";
import PromoIcon from "./promocode.svg";
import { AnimatePresence, motion } from "framer-motion";

const InputComponent = (
    { className, code, ...props }: InputProps,
    ref: ForwardedRef<HTMLInputElement>
) => {
    return (
        <div className={`relative ${className}`}>
            <input
                className={`border-2 ${!code && "border-input"} ${
                    code && code.detail.code == 0 && "border-green"
                } ${
                    code &&
                    (code.detail.code == 1 || code.detail.code == 2) &&
                    "border-red"
                } rounded-lg text-base w-full px-8 py-2 placeholder:text-center text-center mb-2 transition-all`}
                ref={ref}
                disabled={code && code.detail.code == 0}
                {...props}
            />
            <AnimatePresence>
                {code && (
                    <motion.div
                        initial={{ height: 0 }}
                        animate={{ height: "auto" }}
                    >
                        {code.detail.code == 0 && (
                            <span className="text-green">
                                Промокод активирован! Скидка:{" "}
                                {code.detail.discount} %
                            </span>
                        )}
                        {code.detail.code == 1 && (
                            <span className="text-red">
                                Активации промокода закончились!
                            </span>
                        )}
                        {code.detail.code == 2 && (
                            <span className="text-red">
                                Такого промокода не существует!
                            </span>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
            <PromoIcon className="absolute top-1 left-2" />
        </div>
    );
};

export const Input = forwardRef(InputComponent);
