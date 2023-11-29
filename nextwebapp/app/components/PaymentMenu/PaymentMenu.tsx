import { payConfig } from "@/app/helpers/pay_config";
import { PaymentMenuProps } from "./PaymentMenu.props";
import { ImgButton } from "../ImgButton/ImgButtons";

export const PaymentMenu: React.FC<PaymentMenuProps> = ({
    neural,
    ratePlan,
    discount,
}) => {
    const handlePay = async (method: "bankCard" | "crypto") => {
        if (ratePlan && neural) {
            const formData = new FormData();
            const payInfo = payConfig.find((payment) => {
                if (payment.title == ratePlan && payment.neural == neural) {
                    return true;
                }
            });
            formData.append(
                "chatid",
                String(window.Telegram.WebApp.initDataUnsafe.user.id)
            );
            if (payInfo) {
                formData.append(
                    "amount",
                    String(Math.round(payInfo.amount * (1 - discount * 0.01)))
                );
                formData.append("buytype", String(payInfo.buytype));
            }
            const url = `https://gpt.apicluster.ru/pay/checkout/${
                method == "bankCard" ? "standart" : "crypto"
            }`;
            const response = await fetch(url, {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            window.location.assign(data.detail.url);
        }
    };

    return (
        <div className="flex flex-col space-y-3">
            <ImgButton onClick={() => handlePay("bankCard")} img="BankCard" />
            <ImgButton onClick={() => handlePay("crypto")} img="Crypto" />
        </div>
    );
};
