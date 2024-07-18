from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs
from ..bot.logs import logger
from ..integrations import ReniaBackendClient
import requests, json, os
import psycopg2

class Unverify(SlashCommand):

    name = "unverify"
    description = "Usuwa weryfikację użytkownika"

    async def run(self):
        logger.info("Unverify command")
        
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        await self.run()
