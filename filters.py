from aiogram.filters import BaseFilter
from aiogram import types
from db import getIDs

# Фильтр для проверки есть ли пользователь в игре
class InGame(BaseFilter):
    async def __call__(self, message: types.Message):
        return message.from_user.id in getIDs()

# Фильтр для проверки есть ли пользователь в игре
class NotInGame(BaseFilter):
    async def __call__(self, message: types.Message):
        return not message.from_user.id in getIDs()
    