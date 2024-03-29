import { Promocode } from "@/app/helpers/types";
import { InputHTMLAttributes, DetailedHTMLProps } from "react";

export interface InputProps
    extends DetailedHTMLProps<
        InputHTMLAttributes<HTMLInputElement>,
        HTMLInputElement
    > {
    code?: Promocode;
}
