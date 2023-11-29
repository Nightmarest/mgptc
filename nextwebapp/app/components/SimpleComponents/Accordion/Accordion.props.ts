import { DetailedHTMLProps, HTMLAttributes } from "react";
import { Neural, RatePlan, State } from "../../../helpers/types";

export interface AccordionProps
    extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    color?: "one" | "three" | "four" | "six" | "two";
    children: React.ReactNode[];
    title: RatePlan;
    opened?: string | null;
    setOpened?: React.Dispatch<React.SetStateAction<string | null>>;
    setState?: React.Dispatch<React.SetStateAction<State>>;
    disabled?: boolean;
}
