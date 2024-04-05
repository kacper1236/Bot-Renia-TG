from typing import List, Dict
from telegram.ext import Application, BaseHandler, MessageHandler
from . import BaseCommand

class CommandManager:

    def __init__(self, app: Application) -> None:
        self.handlers: Dict[str, BaseHandler] = dict()
        self.descriptions: Dict[str, str] = {}
        self.__app = app

    def setup(self, commands: List[BaseCommand]):
        for command in commands:
            self.handlers[command.name] = command.get_handler()
            self.descriptions[command.name] = command.description
            self.__app.add_handler(self.handlers[command.name])

    def add_command(self, command: BaseCommand):
        '''Dodanie/modyfikacja komendy'''
        handler = command.get_handler()
        self.handlers[command.name] = handler
        self.descriptions[command.name] = command.description
        self.__app.add_handler(handler)
            
    def remove_command(self, name: str):
        '''Ununięcie komendy'''
        self.__app.remove_handler(self.handlers[name])
        self.handlers.pop(name)
        self.descriptions.pop(name)