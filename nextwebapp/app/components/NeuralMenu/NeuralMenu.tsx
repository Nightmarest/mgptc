import { Neural, State, neurals } from "../../helpers/types";

import { ImgButton } from "../ImgButton/ImgButtons";
import { NeuralMenuProps } from "./NeuralMenu.props";

export const NeuralMenu: React.FC<NeuralMenuProps> = ({
    setState,
    setNeural,
}) => {
    const EnterNeural = (neural: Neural) => {
        setNeural(neural);
        setState(State.ratePlan);
    };

    return (
        <div className="space-y-3">
            {neurals.map((n) => {
                return (
                    <ImgButton
                        img={n}
                        key={n}
                        className="text-base"
                        onClick={() => EnterNeural(n)}
                    />
                );
            })}
        </div>
    );
};
