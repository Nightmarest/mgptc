import { useState } from "react";
import { RatePlanProps } from "./RatePlanMenu.props";
import { ImgAccordion } from "../ImgAccordion/ImgAccordion";
import { ratePlans } from "@/app/helpers/types";

export const RatePlanMenu: React.FC<RatePlanProps> = ({
    neural,
    setRatePlan,
    setState,
}) => {
    const [opened, setOpened] = useState<string | null>(null);

    return (
        <div className="space-y-3">
            {ratePlans[neural].map((title) => {
                return (
                    <ImgAccordion
                        key={title}
                        title={title}
                        setOpened={setOpened}
                        opened={opened}
                        setRatePlan={setRatePlan}
                        setState={setState}
                        neural={neural}
                    />
                );
            })}
        </div>
    );
};
