import { Neural } from "@/app/helpers/types";
import { HTMLAttributes, DetailedHTMLProps } from "react";

export interface NeuralInfoProps
    extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    neural: Neural;
}
