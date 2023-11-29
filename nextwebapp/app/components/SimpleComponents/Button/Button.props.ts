import { ButtonHTMLAttributes, DetailedHTMLProps } from "react";

export type ButtonColors =
    | "gpt"
    | "pika"
    | "mj"
    | "white"
    | "deepai"
    | "black"
    | "red";

export interface ButtonProps
    extends Omit<
        DetailedHTMLProps<
            ButtonHTMLAttributes<HTMLButtonElement>,
            HTMLButtonElement
        >,
        "onAnimationStart" | "onDragStart" | "onDragEnd" | "onDrag" | "ref"
    > {
    children: React.ReactNode;
    color: ButtonColors;
}
