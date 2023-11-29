import { motion } from "framer-motion";
import { ButtonProps } from "./Button.props";

const colors = {
    gpt: "bg-gradient-to-r from-Gpt1 to-Gpt2 text-white",
    pika: "bg-gradient-to-r from-Pika1 to-Pika2 text-white ",
    black: "bg-blackBtn active:bg-purpleBtnHover text-white ",
    mj: "bg-gradient-to-r from-Mj1 to-Mj2 text-white ",
    white: "bg-white active:bg-whiteBtnHover text-black",
    deepai: "bg-gradient-to-r from-DeepAi1 to-DeepAi2 text-white",
    red: "bg-gradient-to-r from-red1 to-red2 text-white",
};

export const Button: React.FC<ButtonProps> = ({
    className,
    children,
    color,
    disabled,
    ...props
}) => {
    const styleColor = colors[color];
    if (disabled) {
        return (
            <button
                className={`${className} ${styleColor} rounded-full p-2 transition-all shadow-xl`}
                disabled
            >
                {children}
            </button>
        );
    } else {
        return (
            <motion.button
                className={`${className} ${styleColor} rounded-full p-2 transition-all shadow-xl`}
                whileTap={!disabled && { scale: 0.95 }}
                {...props}
            >
                {children}
            </motion.button>
        );
    }
};
