import { Neural, RatePlan, State } from "../../helpers/types";

export interface RatePlanProps {
    neural: Neural;
    setRatePlan: React.Dispatch<React.SetStateAction<RatePlan | null>>;
    setState: React.Dispatch<React.SetStateAction<State>>;
}
