import { Neural, RatePlan } from "@/app/helpers/types";

export interface PaymentMenuProps {
    neural: Neural;
    ratePlan: RatePlan;
    discount: number;
}
