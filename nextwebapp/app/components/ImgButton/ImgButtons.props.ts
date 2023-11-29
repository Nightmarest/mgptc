import { Neural } from "@/app/helpers/types";
import { ButtonProps } from "../SimpleComponents/Button/Button.props";

export type Imgs = Neural | "BankCard" | "Crypto";

export interface ImgButtonProps
    extends Omit<ButtonProps, "children" | "color"> {
    img: Imgs;
}
