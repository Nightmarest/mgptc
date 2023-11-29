import { HTMLAttributes, DetailedHTMLProps } from "react";

export interface CardProps
    extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    children?: React.ReactNode;
    title: string;
}
