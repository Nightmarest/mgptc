import { State } from "../../helpers/types";

export interface PromocodeMenuProps {
    setState: React.Dispatch<React.SetStateAction<State>>;
    setDiscount: React.Dispatch<React.SetStateAction<number>>;
}
