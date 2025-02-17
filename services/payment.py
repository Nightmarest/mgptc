import json
import random
import traceback

from config_data.config import config
from config_data.config_load import pay_list
from utils.func import report
import logging as lg
import aiohttp
from datetime import datetime
from dateutil.relativedelta import relativedelta
from handlers.client import buy_handler
from aiogram.types import CallbackQuery
from config_data.create_bot import db
from pyCryptomusAPI import pyCryptomusAPI
from yookassa import Payment, Configuration


class promo:
    async def checkpromo(chat_id, promo):
        promocode = db.admin_request(f"SELECT * FROM promo WHERE name = '{str(promo)}'")
        prinfo = ""
        # promocode = db.readpromo(promo)
        lg.info(f"Попытка задействовать промокод {promocode}")
        if promocode is None:
            code = 2
            reason = "Promocode not Found!"
            discount = None
        else:
            try:
                if int(promocode[0][2]) > int(promocode[0][1]):
                    code = 1
                    reason = "The promo code has run out of activations"
                    discount = None
                else:
                    code = 0
                    reason = f"Promocode activated"
                    discount = promocode[0][3]
            except Exception as e:
                code = 2
                reason = "Promocode not Found!"
                discount = None

        return code, reason, discount

class cloudpay_api:
    async def create_payment(track_id, chat_id, sum, buytype):
        try:

            Configuration.account_id = config['YOOKASSA_ID']
            Configuration.secret_key = config['YOOKASSA_TOKEN']
            payment = Payment.create({
                "amount": {
                    "value": str(sum) + ".00",
                    "currency": "RUB"
                },
                "payment_method_data": {
                    "type": "bank_card"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://google.com"
                },
                "receipt": {
                    "customer": {
                        "email": "git@afedko.ru",
                    },
                    "items": [
                        {

                            "description": f"Оплата подписки {buytype} для ЛК {chat_id}",
                            "quantity": "1",
                            "amount": {
                                "value": str(sum) + ".00",
                                "currency": "RUB",
                            },
                            "vat_code": "1"

                        },
                    ]

                },

                "capture": True,
                "description": chat_id
            })
            payment_data = json.loads(payment.json())
            payment_id = payment_data['id']
            payment_url = (payment_data['confirmation'])['confirmation_url']
            payment = json.loads((Payment.find_one(payment_id)).json())

            code = 0
            reason = "Successfully created!"
            return payment_url, code, reason
        except Exception:
            code = 1
            reason = "Unexpected Error! Please ask admin for details"
            payurl = None
            lg.error(traceback.format_exc())
            return payurl, code, reason

    async def check(track_id, chatid, buy_type=None):
        url = 'https://api.cloudpayments.ru/payments/get'
        headers = { 'content-type': 'application/json' }
        session = aiohttp.ClientSession()
        checkpay = {
            "TransactionId": track_id,
        }
        lg.error(track_id)

        async with session.post(
                url, data = json.dumps(checkpay), headers = headers,
                auth = aiohttp.BasicAuth(config['CPID'], config['CPKEY'])
                ) as resp:
            response = await resp.json(content_type = None)
            resp.close()
            await session.close()
            lg.info(f"STEP-1, {buy_type}",)
            if buy_type is not None:

                if response['Success'] is True:
                        if pay_list[buy_type]["autosub"] is True:
                            # if db.read(chatid, "subid") is not None:
                            #     subid = db.read(chatid, "subid")
                            #     url = 'https://api.cloudpayments.ru/subscriptions/cancel'
                            #     headers = {'content-type': 'application/json'}
                            #     session = aiohttp.ClientSession()
                            #     subcancel = {
                            #         "Id": subid,
                            #     }
                            #
                            #     async with session.post(
                            #             url, data=json.dumps(subcancel), headers=headers,
                            #             auth=aiohttp.BasicAuth(
                            #                 config['CPID'],
                            #                 config['CPKEY']
                            #             )
                            #     ) as resp:
                            #         response = await resp.json(content_type=None)
                            #
                            #         resp.close()
                            #         await session.close()
                            db.update(chatid, "subid", None)
                            now = datetime.today() + relativedelta(months=pay_list[buy_type]["period"])

                            url = 'https://api.cloudpayments.ru/subscriptions/create'
                            headers = { 'content-type': 'application/json' }
                            session = aiohttp.ClientSession()
                            create_sub = {
                                "token": response['Model']['Token'],
                                "accountId": response['Model']['AccountId'],
                                "InvoiceId": response['Model']['InvoiceId'],
                                "description": "Ежемесячная подписка на сервис Midjourney",
                                "email": "user@example.com",
                                "amount": pay_list[buy_type]['amount'],
                                "currency": "RUB",
                                "StartDate": str(now),
                                "requireConfirmation": False,
                                "interval": "Month",
                                "period": str(pay_list[buy_type]["period"])
                            }

                            async with session.post(
                                    url, data = json.dumps(create_sub), headers = headers,
                                    auth = aiohttp.BasicAuth(
                                        config['CPID'],
                                        config['CPKEY']
                                        )
                                    ) as resp:
                                subinfo = await resp.json(content_type = None)
                                resp.close()
                                await session.close()
                            lg.info(f"{response}\n\n\n\n\n {subinfo}")
                            await buy_handler.accrual_requests(buy_type, chatid, response['Model']['Token'], response['Model']['InvoiceId'], subinfo['Model']['Id'])

                        elif pay_list[buy_type]["autosub"] is False:
                            await buy_handler.accrual_requests(buy_type, chatid)
            else:
                    lg.info("STEP-2")
                    buy_type = db.read(chatid, "premium_type")
                    if buy_type is None:
                        buy_type = 0
                    if buy_type == "":
                        buy_type = 0
                    if buy_type == 0:
                        if response['Model']['Amount'] == 480:
                            buy_type = "buy-0"
                        elif response['Model']['Amount'] == 980:
                            buy_type = "buy-1"
                        elif response['Model']['Amount'] == 2440:
                            buy_type = "buy-2"
                        elif response['Model']['Amount'] == 1440:
                            buy_type = "buy-8"

                        await buy_handler.accrual_requests(buy_type, chatid)
                    else:
                        pass

    async def subcancel(subid):
        url = 'https://api.cloudpayments.ru/subscriptions/cancel'
        headers = { 'content-type': 'application/json' }
        session = aiohttp.ClientSession()
        subcancel = {
            "Id": subid,
        }

        async with session.post(
                url, data = json.dumps(subcancel), headers = headers,
                auth = aiohttp.BasicAuth(
                    config['CPID'],
                    config['CPKEY']
                    )
                ) as resp:
            response = await resp.json(content_type = None)

            resp.close()
            await session.close()
        return response['Success']


class cryptobot_api:


    async def create_payment(chat_id, amount, buytype):
            client = pyCryptomusAPI(
                "6b3fe033-9cd6-4dfc-8882-c144e9437144",  # Merchand UUID
                payment_api_key="addjXjjNW0yiOndvfUdVmnjDu7E4Dt3eNZYkPkHouFNqEZvn9nkqcITT1XTei8Chkx1aWBC2U4MOkULihcuKZR873YHf1X3n8JqtkBVmVQposPBDC1ifh05rYKkh3DwS",
                # Payment API key (for payment methods)
                payout_api_key="2RAn5RAVLhxdWUs7rIvXuhcb3WtFqKDomIcmKxoFvbjcgBO9QZYj0FuSdjuCapM9GoKMthHu69FemtxKExYWSpvqsRDpHDvkjgHJOi1RPrkX1gRKEWQt1Xt61sCcJmS5")  # Payout API key (for payout methods)

            ordid = f"{chat_id}_{random.randint(111111,999999)}"
            payout = client.create_invoice(amount=amount, currency="RUB", order_id=ordid,
                                           url_callback="https://gpt.apicluster.ru/pay/success/crypto",
                                           additional_data=(buytype))
            lg.info(payout)
            code = 0
            reason = "Successfully created!"
            return payout.__dict__['url'], code, reason
        # except:
        #     code = 1
        #     reason = "Unexpected Error! Please ask @langley_reddle for details"
        #     return code, reason


    async def check(orderid, buytype):
        chatid = orderid.split("_")[0]

        await buy_handler.accrual_requests(buytype, chatid)
        return 200
