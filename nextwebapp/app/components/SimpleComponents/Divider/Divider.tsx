import { DividerProps } from "./Divider.props";

export const Divider: React.FC<DividerProps> = ({
    className,
    color,
    ...props
}) => {
    return (
        <div
            className={`${color == "black" && "bg-black"} ${
                color == "white" && "bg-white"
            } h-[1px] rounded-full ${className}`}
            {...props}
        ></div>
    );
};
