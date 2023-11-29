import { AccordionProps } from "./Accordion.props";
import { AnimatePresence, motion } from "framer-motion";

const colors = {
    one: "bg-gradient-to-r from-Pika1 to-Pika2",
    three: "bg-gradient-to-r from-Mj1 to-Mj2",
    four: "bg-gradient-to-r from-DeepAi1 to-DeepAi2",
    six: "bg-gradient-to-r from-red1 to-red2",
    two: "bg-gradient-to-r from-Gpt1 to-Gpt2",
};

const variants = {
    opened: {
        height: "auto",
        opacity: 1,
    },
    closed: {
        height: 0,
        opacity: 0,
    },
};

export const Accordion: React.FC<AccordionProps> = ({
    className,
    color,
    title,
    opened,
    setOpened,
    disabled,
    children,
}) => {
    const styleColor = color
        ? colors[color]
        : "bg-gradient-to-r from-DeepAi1 to-DeepAi2";

    const setIsOpened = () => {
        if (setOpened) {
            if (opened === title) {
                setOpened(null);
            } else {
                setOpened(title);
            }
        }
    };

    return (
        <div
            className={`${className} ${styleColor} text-white font-medium rounded-3xl p-2 shadow-xl`}
        >
            <button className="w-full flex items-center" onClick={setIsOpened}>
                {children[0]}
            </button>
            <AnimatePresence>
                {opened === title && !disabled && (
                    <motion.div
                        variants={variants}
                        initial="closed"
                        animate={opened === title ? "opened" : "closed"}
                        exit={variants.closed}
                        className="overflow-hidden"
                    >
                        {children[1]}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
