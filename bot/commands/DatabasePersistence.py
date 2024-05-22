from telegram.ext import BasePersistence, PersistenceInput
import json
from logs import logger

class DatabasePersistence(BasePersistence):

    def __init__(self) -> None:
        super(DatabasePersistence, self).__init__(store_data=PersistenceInput(bot_data=True, chat_data=True, user_data=True, callback_data=True))
        self.bot_data: dict = {}
        self.callback_data = {}
        self.chat_data: dict = {}
        self.user_data: dict = {}
        self.conversations = {}

    async def drop_chat_data(self, chat_id: int):
        if chat_id in self.chat_data:
            del self.chat_data[chat_id]
            logger.info("usunięty czat")

    async def drop_user_data(self, user_id: int):
        if user_id in self.user_data:
            del self.user_data[user_id]
            logger.info("usunięty użytkownik")

    async def flush(self):
        pass

    async def get_bot_data(self) -> dict:
        return self.bot_data

    async def get_callback_data(self) -> dict:
        return self.callback_data

    async def get_chat_data(self) -> dict:
        return self.chat_data

    async def get_conversations(self, name: str) -> dict:
        logger.info("get_conversations")
        logger.info(name)
        return self.conversations.get(name, {})

    async def get_user_data(self) -> dict:
        return self.user_data

    async def refresh_bot_data(self, bot_data: any):
        logger.info("refresh_bot_data")
        logger.info(bot_data)
        self.bot_data = bot_data

    async def refresh_chat_data(self, chat_id: int, chat_data: any):
        logger.info("refresh_chat_data")
        logger.info(chat_id)
        logger.info(chat_id)
        self.chat_data[chat_id] = chat_data

    async def refresh_user_data(self, user_id: int, user_data: any):
        logger.info("refresh_user_data")
        logger.info(user_id)
        logger.info(user_data)
        self.user_data[user_id] = user_data

    async def update_bot_data(self, bot_data: any):
        self.bot_data = bot_data

    async def update_callback_data(self, callback_data: any):
        self.callback_data = callback_data

    async def update_chat_data(self, chat_id: int, chat_data: any):
        self.chat_data[chat_id] = chat_data

    async def update_conversation(self, name: str, key: str, new_state: any):
        if name not in self.conversations:
            self.conversations[name] = {}
        self.conversations[name][key] = new_state

    async def update_user_data(self, user_id: int, user_data: any):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id].update(user_data)

