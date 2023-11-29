import { Neural, RatePlan } from "../../helpers/types";
import { AccordionProps } from "../SimpleComponents/Accordion/Accordion.props";

export interface ImgAccordionProps
    extends Omit<AccordionProps, "children" | "color" | "neural"> {
    title: RatePlan;
    neural: Neural;
    setRatePlan?: React.Dispatch<React.SetStateAction<RatePlan | null>>;
}
