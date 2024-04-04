from typing import List, Dict
from telegram.ext import Application, CommandHandler, MessageHandler
from . import BaseCommand

class CommandManager:

    def __init__(self, app: Application) -> None:
        self.handlers: Dict[str, List[CommandHandler, MessageHandler]] = dict()
        self.descriptions: Dict[str, str] = {}
        self.__app = app

    def setup(self, commands: List[BaseCommand]):
        for command in commands:
            if command.name == "zdjecia":
                self.handlers[command.name] = command.get_handler_MessageHandler()
            else:
                self.handlers[command.name] = command.get_handler_CommandHandler()
            self.descriptions[command.name] = command.description
            self.__app.add_handler(self.handlers[command.name])

    def add_command(self, command: BaseCommand):
        '''Dodanie/modyfikacja komendy'''
        if command.name == "zdjecia":
            handler = command.get_handler_MessageHandler()
        else:
            handler = command.get_handler_CommandHandler()
        self.handlers[command.name] = handler
        self.descriptions[command.name] = command.description
        self.__app.add_handler(handler)
            
    def remove_command(self, name: str):
        '''Ununięcie komendy'''
        self.__app.remove_handler(self.handlers[name])
        self.handlers.pop(name)
        self.descriptions.pop(name)