from typing import List
from telegram.ext import Application
from . import TestCommand, BaseCommand

class CommandManager:

    def __init__(self, app: Application) -> None:
        self.handlers = {}
        self.__app = app

        commands: List[BaseCommand] = [TestCommand()]

        for command in commands:
            self.handlers[command.name] = command.get_handler()
        
        self.__app.add_handlers(self.handlers.values())
    
    def add_command(self, command: BaseCommand):
        '''Dodanie/modyfikacja komendy'''
        handler = command.get_handler()
        self.handlers[command.name] = handler
        self.__app.add_handler(handler)
            
    def remove_command(self, name: str):
        '''Ununięcie komendy'''
        self.__app.remove_handler(self.handlers[name])