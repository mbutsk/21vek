from config import *
import logging
import asyncio
from aiogram.enums import ParseMode
import sys
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters.command import Command
from aiogram.methods.delete_webhook import DeleteWebhook
from aiogram.client.bot import DefaultBotProperties
from aiogram.utils.markdown import hbold, hlink, hitalic
from keyboards import Markups
from db import addToGame, getData, updateData, deleteFromGame
from filters import InGame, NotInGame
from math import floor

# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(f"Привет! Это игра-кликер, сделанная на конкурс от {hlink('Алгоритмики', 'https://algoritmika.by/ru')} и {hlink('Магазина 21 vek', 'https://www.21vek.by/')}",
                         link_preview_options=types.LinkPreviewOptions(is_disabled=True),
                         reply_markup=await Markups.start())

@dp.callback_query(F.data == 'start')
async def startGame(callback: types.CallbackQuery):
    await callback.answer("Игра начата")
    message = callback.message
    if await addToGame(callback.from_user.id):
        await message.answer(hitalic("*Вы включили телевизор*"))
        await asyncio.sleep(4)
        await message.answer_sticker("CAACAgIAAxkBAAEMKpBmTiQndvioqWTw9D_GYBxXGq-Q5AACjFEAAulkcErMY_sKG_lOlzUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Хэй! Меня зовут Нонстоппер и я - новый талисман Магазина 21 vek!')
        await asyncio.sleep(9)
        await message.answer_sticker("CAACAgIAAxkBAAEMKpBmTiQndvioqWTw9D_GYBxXGq-Q5AACjFEAAulkcErMY_sKG_lOlzUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Совсем недавно мы запустили акцию: В нашем приложении на телефоне Вы можете найти раздел {hbold("VekClicker")}')
        await asyncio.sleep(6)
        await message.answer_sticker("CAACAgIAAxkBAAEMKpBmTiQndvioqWTw9D_GYBxXGq-Q5AACjFEAAulkcErMY_sKG_lOlzUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Играя в ВекКликер Вы можете зарабатывать баллы. Баллы можно обменивать на скидку. Каждые 50 баллов = 1%. {hbold("Более 25% скидку получить нельзя")}')
        await asyncio.sleep(10)
        await message.answer_sticker("CAACAgIAAxkBAAEMKpBmTiQndvioqWTw9D_GYBxXGq-Q5AACjFEAAulkcErMY_sKG_lOlzUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: {hitalic("*Быстро озвучивает условия акции. Вы ничего не поняли*")}')
        await asyncio.sleep(8)
        await message.answer(hitalic("*Вы посмотрели на свой 20-летний телевизор*"))
        await asyncio.sleep(6)
        await message.answer(f'{hbold("В мыслях")}: {hitalic("Интересная акция... Надо накопить на новый телевизор...")}',
                            reply_markup=await Markups.phone())
    else:
        await message.answer(hitalic("*Вы включили телевизор*"))
        await asyncio.sleep(4)
        await message.answer_sticker("CAACAgIAAxkBAAEMKpBmTiQndvioqWTw9D_GYBxXGq-Q5AACjFEAAulkcErMY_sKG_lOlzUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: В нашу игру нельзя заходить несколько раз, представляясь разными личностями!')

@dp.callback_query(InGame(), F.data == 'openGame')
async def openGame(callback: types.CallbackQuery):
    await callback.answer("Игра в телефоне начата")
    message = callback.message
    await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
    await message.answer(f'{hbold("Нонстоппер")} {hitalic("*В телефоне*")}: Хэй! Меня зовут Нонстоппер! Помнишь меня? Мы уже виделись в телевизоре!')
    await asyncio.sleep(6)
    await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
    await message.answer(f'{hbold("Нонстоппер")} {hitalic("*В телефоне*")}: За клики на кнопку ты можешь получать особые монетки: {hbold("ВекКоины")}')
    await asyncio.sleep(6)
    await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
    await message.answer(f'{hbold("Нонстоппер")} {hitalic("*В телефоне*")}: За ВекКоины можно получать улучшения. Также их можно обменять на скидку в Магазине {hbold("7 ВекКоинов = 1%. Скидку более 50% получить нельзя")}',
                         reply_markup=await Markups.startGame())
    
@dp.callback_query(InGame(), F.data == 'startGame')
async def startGame(callback: types.CallbackQuery):
    await callback.answer("Игра открыта")
    message = callback.message
    coins = getData(callback.from_user.id, 'coins')
    match int(str(coins)[-1]) + 1:
        case 1:
            case = "ВекКоин"
        case 2 | 3 | 4:
            case = "ВекКоина"
        case _:
            case = "ВекКоинов"
    await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
    await message.answer(f"ВекКликер\n{hbold(f'{coins} ВекКоинов')}",
                         reply_markup=await Markups.click(coins, case))

@dp.callback_query(InGame(), F.data == 'click')
async def click(callback: types.CallbackQuery):
    await callback.answer("Кликнуто")
    message = callback.message
    multis = int(getData(callback.from_user.id, 'multis'))
    coins = int(getData(callback.from_user.id, 'coins'))
    if len(str(coins + 1)) == 1 or str(coins + 1)[-2] != '1':
        match int(str(coins)[-1]) + 1:
            case 1:
                case = "ВекКоин"
            case 2 | 3 | 4:
                case = "ВекКоина"
            case _:
                case = "ВекКоинов"
    else:
        case = "ВекКоинов"
    updateData(callback.from_user.id, 'coins', coins + multis)
    coins+=multis
    await message.edit_text(f"ВекКликер\n{hbold(f'{coins} {case}')}",
                            reply_markup=await Markups.click(coins, case))

@dp.callback_query(InGame(), F.data == 'shop')
async def shop(callback: types.CallbackQuery):
    await callback.answer("Магазин")
    message = callback.message
    coins = int(getData(callback.from_user.id, 'coins'))
    multiprice = int(getData(callback.from_user.id, 'multiprice'))
    await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
    await message.answer(f"{hbold(f'Нонстоппер')}: Что же ты купишь в нашем скромном магазинчике?\n"
                         f"У Вас {hbold(f'{coins} ВекКоинов')}",
                         reply_markup=await Markups.shop(multiprice))

@dp.callback_query(InGame(), F.data == 'multiply')
async def multiply(callback: types.CallbackQuery):
    await callback.answer("Покупка множителя")
    message = callback.message
    coins = int(getData(callback.from_user.id, 'coins'))
    price = int(getData(callback.from_user.id, 'multiprice'))
    if coins >= price:
        multis = int(getData(callback.from_user.id, 'multis'))
        updateData(callback.from_user.id, 'multiprice', price + 30)
        updateData(callback.from_user.id, 'multis', multis + 1)
        updateData(callback.from_user.id, 'coins', coins - price)
        await message.answer("Множитель ВекКоинов успешно куплен!",
                             reply_markup=await Markups.backToClicker())
    else:
        await message.answer_sticker("CAACAgIAAxkBAAEMK7BmTyFlf4fvwknFsEQB5yIgzHSxGwACxVIAAoHBeUrvSqVQlhMRLDUE")
        await message.answer(f"{hbold(f'Нонстоппер')}: У тебя не хватает ВекКоинов.\n"
                             f"Тебе нужно {f'{price} ВекКоинов'}. У тебя {f'{coins} ВекКоинов'}",
                             reply_markup=await Markups.backToClicker())

@dp.callback_query(InGame(), F.data == 'withdraw')
async def withdraw(callback: types.CallbackQuery):
    await callback.answer("Вывод денег")
    message = callback.message
    coins = int(getData(callback.from_user.id, 'coins'))
    if coins >= 350:
        await message.answer(hitalic('Вы зашли в раздел "Каталог" Магазина 21 vek'))
        await asyncio.sleep(5)
        await message.answer(hitalic('Вы заказали новый телевизор со скидкой'))
        await asyncio.sleep(5)
        await message.answer(hitalic('Спустя 3 дня телевизор пришел к Вам'))
        await asyncio.sleep(5)
        await message.answer(hitalic("*Вы включили телевизор*"))
        await asyncio.sleep(4)
        await message.answer_sticker("CAACAgIAAxkBAAEMMRdmUH-sjxT8B7f1SIRxh2H7zd28ZQAC-E0AAhBkgEqGAekRRXcUazUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Хэй! Меня зовут Нонстоппер и я - новый талисман Магазина 21 vek!')
        await asyncio.sleep(9)
        await message.answer_sticker("CAACAgIAAxkBAAEMMRdmUH-sjxT8B7f1SIRxh2H7zd28ZQAC-E0AAhBkgEqGAekRRXcUazUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Совсем недавно мы запустили акцию: В нашем приложении на телефоне Вы можете найти раздел {hbold("VekClicker")}')
        await asyncio.sleep(6)
        await message.answer_sticker("CAACAgIAAxkBAAEMMRdmUH-sjxT8B7f1SIRxh2H7zd28ZQAC-E0AAhBkgEqGAekRRXcUazUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: Играя в ВекКликер Вы можете зарабатывать баллы. Баллы можно обменивать на скидку. Каждые 50 баллов = 1%. {hbold("Более 25% скидку получить нельзя")}')
        await asyncio.sleep(10)
        await message.answer_sticker("CAACAgIAAxkBAAEMMRdmUH-sjxT8B7f1SIRxh2H7zd28ZQAC-E0AAhBkgEqGAekRRXcUazUE")
        await message.answer(f'{hbold("Нонстоппер")} {hitalic("*По телевизору*")}: {hitalic("*Быстро озвучивает условия акции. Вы ничего не поняли*")}')
        await asyncio.sleep(8)
        await deleteFromGame(callback.from_user.id)
        await message.answer("Поздравляем! Игра пройдена!",
                             reply_markup=await Markups.credits())
        
    else:
        percents = floor(coins / 7)
        await message.answer(f'{hbold("В мыслях")}: {hitalic(f"Нет... Скидки {percents}% мне не хватит Лучше накоплю скидку еще. Мне надо 350 ВекКоинов")}',
                            reply_markup=await Markups.backToClicker())

@dp.message(NotInGame())
async def notInGameMSG(message: types.Message):
    await message.answer("Вы не в игре!",
                         reply_markup=await Markups.start())

@dp.callback_query(NotInGame())
async def notInGameCB(callback: types.CallbackQuery):
    await callback.answer("Вы не в игре!")
    message = callback.message
    await message.answer("Вы не в игре!",
                         reply_markup=await Markups.start())

async def main() -> None:
# And the run events dispatching
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())