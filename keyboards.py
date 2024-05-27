from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

class Markups():
    async def start():
        button = InlineKeyboardButton(text="Начать игру", callback_data='start')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def phone():
        button = InlineKeyboardButton(text="Зайти в ВекКликер", callback_data='openGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def startGame():
        button = InlineKeyboardButton(text="Начать игру", callback_data='startGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def click(coins, case):
        shop   = InlineKeyboardButton(text=f"Магазин", callback_data='shop')
        button = InlineKeyboardButton(text=f"Кликнуть {coins} {case}", callback_data='click')
        markup = InlineKeyboardBuilder().add(button).row(shop).as_markup()
        return markup
    
    async def shop(multiprice):
        multiplier = InlineKeyboardButton(text=f"Множитель ВекКоинов ({multiprice})", callback_data='multiply')
        withdraw   = InlineKeyboardButton(text= "Вывод скидки", callback_data='withdraw')
        markup     = InlineKeyboardBuilder().add(withdraw).row(multiplier).as_markup()
        return markup
    
    async def backToClicker():
        button = InlineKeyboardButton(text="Вернуться в кликер", callback_data='startGame')
        markup = InlineKeyboardBuilder().add(button).as_markup()
        return markup
    
    async def credits():
        tg     = InlineKeyboardButton(text="Telegram создателя", url="tg://user?id=1223353442")
        github = InlineKeyboardButton(text="GitHub создателя",   url="https://github.com/mbutskpy")
        markup = InlineKeyboardBuilder().add(github).row(tg).as_markup()
        return markup