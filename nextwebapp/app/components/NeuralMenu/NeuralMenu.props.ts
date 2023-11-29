import { Neural, State } from "../../helpers/types";

export interface NeuralMenuProps {
    setState: React.Dispatch<React.SetStateAction<State>>;
    setNeural: React.Dispatch<React.SetStateAction<Neural | null>>;
}
