import { CardProps } from "./Card.props";

export const Card: React.FC<CardProps> = ({
    className,
    children,
    title,
    ...props
}) => {
    return (
        <div
            className={`${className} bg-white p-4 rounded-2xl shadow-lg`}
            {...props}
        >
            <h2
                dangerouslySetInnerHTML={{ __html: title }}
                className={`font-medium text-lg ${children && "mb-3"}`}
            ></h2>
            {children}
        </div>
    );
};
