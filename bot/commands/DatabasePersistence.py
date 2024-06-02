from telegram.ext import BasePersistence, PersistenceInput
import json
from logs import logger

class DatabasePersistence(BasePersistence):

    path = "./commands/DatabasePersistenceJson/conversation.json"

    def __init__(self) -> None:
        super(DatabasePersistence, self).__init__(store_data=PersistenceInput(bot_data=True, chat_data=True, user_data=True, callback_data=True), update_interval=1)
        self.bot_data: dict = {}
        self.callback_data = {}
        self.chat_data: dict = {}
        self.user_data: dict = {}
        self.conversations: dict = {}

    async def drop_chat_data(self, chat_id: int):
        if chat_id in self.chat_data:
            del self.chat_data[chat_id]

    async def drop_user_data(self, user_id: int):
        if user_id in self.user_data:
            del self.user_data[user_id]

    async def flush(self):
        data_seriazable = {}
        for k, v in self.conversations.items():
            for i, j in v.items():
                data_seriazable[k] = {str(i): j}
        print(data_seriazable)
        try:
            with open(self.path, "w") as f:
                json.dump(data_seriazable, f)
        except Exception as e:
            logger.info(e)
        logger.info("Flushed")

    async def get_bot_data(self) -> dict:
        return self.bot_data

    async def get_callback_data(self) -> dict:
        return self.callback_data

    async def get_chat_data(self) -> dict:
        return self.chat_data

    async def get_conversations(self, name: str) -> dict:
        try:
            with open(self.path, "r") as f:
                self.conversations = json.load(f)
                for k, v in self.conversations.items():
                    for i, j in v.items():
                        self.conversations[k] = {eval(i): j}
        except Exception as e:
            logger.info(e)
        return self.conversations.get(name, {})

    async def get_user_data(self) -> dict:
        return self.user_data

    async def refresh_bot_data(self, bot_data: any):
        self.bot_data = bot_data

    async def refresh_chat_data(self, chat_id: int, chat_data: any):
        if chat_data == {}:
            await self.drop_chat_data(chat_id)
        self.chat_data[chat_id] = chat_data

    async def refresh_user_data(self, user_id: int, user_data: any):
        if user_data == {}:
            await self.drop_user_data(user_id)
        self.user_data[user_id] = user_data

    async def update_bot_data(self, bot_data: any):
        self.bot_data = bot_data

    async def update_callback_data(self, callback_data: any):
        self.callback_data = callback_data

    async def update_chat_data(self, chat_id: int, chat_data: any):
        self.chat_data[chat_id] = chat_data

    async def delete_conversation(self, name: str, key: str, new_state: any):
        del self.conversations[name][key]
        with open(self.path, "w") as f:
            data_seriazable = json.load(f)
            for k, v in self.conversations.items():
                for i, j in v.items():
                    data_seriazable[k] = {eval(i): j}
        return

    async def update_conversation(self, name: str, key: str, new_state: any):
        if new_state == None and name == "zdjecia":
            await self.delete_conversation(name, key, new_state)
        if name not in self.conversations:
            self.conversations[name] = {}
        self.conversations[name][key] = new_state
        data_seriazable = {}
        for k, v in self.conversations.items():
            for i, j in v.items():
                data_seriazable[k] = {str(i): j}
        with open("./commands/DatabasePersistenceJson/conversation.json", "w") as f:
            json.dump(data_seriazable, f)

    async def update_user_data(self, user_id: int, user_data: any):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id].update(user_data)
