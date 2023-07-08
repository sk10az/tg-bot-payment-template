import config
import logging

import handlers.keyboard as keyboard

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType


print(config.TOKEN)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
PRICE = types.LabeledPrice(label='Subscribe', amount=24499*100) 

@dp.message_handler(commands=["buy"])
async def buy(message: types.Message):
    if config.PAYMENTS_TOKEN.split(':')[1] == 'Test':
        await bot.send_message(message.chat.id, 'Test payment')

    await bot.send_invoice(
        message.chat.id,
        title='subscribe',
        description='Simple description',
        provider_token=config.PAYMENTS_TOKEN,
        currency='rub',
        photo_url='https://roliki-magazin.ru/wp-content/uploads/5/0/0/500fb1144b76f6a1a0c7e9af9353f6b6.jpeg',
        photo_height=400,
        photo_width=400,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload='test-invoice-payload'
    )

    



@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print('Successful payment:')
    payment_info = message.successful_payment.to_python()
    for key, value in payment_info.items():
        print(f"{key} = {value}")

    await bot.send_message(message.chat.id, f"Payment for the amount {message.successful_payment.total_amount // 100} {message.successful_payment.currency} passed successfuly!")


async def start(message: types.Message):
    try:
        await message.answer('Бот работает!', reply_markup=keyboard.mainmenu)
    except Exception as e:
        print(e)


async def keyboard_handler(message: types.Message):
    try:
        match message.text:
            case "Помощь":
                await message.reply('Какая тебе нужна помощь, друг?', reply_markup=keyboard.help)
            case "О нас":
                await message.reply('Этот бот сделан для обучения библиотеки Aiogram')
            case _:
                await message.answer('Такой команды не существует!')
    except Exception as e:
        print(e)


async def inline_help_buttons_handler(call: types.CallbackQuery):
    match call.data:
        case "helpfinance":
            await call.message.answer("Финансовая помощь не доступна!")
            await bot.answer_callback_query(callback_query_id=call.id)
        case "helpphysically":
            await call.message.answer("Физическая помощь не доступна!")
            await bot.answer_callback_query(callback_query_id=call.id)


def register_client():
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(keyboard_handler, state=None)
    dp.register_callback_query_handler(inline_help_buttons_handler)




if __name__ == '__main__':
    register_client()
    executor.start_polling(dp, skip_updates=False)