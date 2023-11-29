import { HTMLAttributes, DetailedHTMLProps } from "react";

export interface DividerProps
    extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    color: "white" | "black";
}
