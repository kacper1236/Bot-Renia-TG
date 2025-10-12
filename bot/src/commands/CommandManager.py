from typing import List, Dict
from telegram.ext import Application, BaseHandler
from . import BaseCommand
from ..bot.logs import logger

class CommandManager:

    def __init__(self, app: Application) -> None:
        self.handlers: Dict[str, BaseHandler] = dict()
        self.descriptions: Dict[str, str] = {}
        self.is_visible: Dict[str, bool] = {}
        self.__app = app

    def setup(self, commands: List[BaseCommand]):
        for command in commands:
            try:
                self.handlers[command.name] = command.get_handler()
                self.descriptions[command.name] = command.description
                self.is_visible[command.name] = command.is_visible
                self.__app.add_handler(self.handlers[command.name])
            except AttributeError:
                for a in command:
                    self.handlers[a.name] = a.get_handler()
                    self.descriptions[a.name] = a.description
                    self.is_visible[a.name] = a.is_visible
                    self.__app.add_handler(self.handlers[a.name])

    def add_command(self, command: BaseCommand):
        '''Dodanie/modyfikacja komendy'''
        handler = command.get_handler()
        self.handlers[command.name] = handler
        self.descriptions[command.name] = command.description
        self.is_visible[command.name] = command.is_visible
        self.__app.add_handler(handler)
            
    def remove_command(self, name: str):
        '''Usunięcie komendy'''
        try:
            self.__app.remove_handler(self.handlers[name])
            self.handlers.pop(name)
            self.descriptions.pop(name)
            self.is_visible.pop(name)
        except KeyError:
            logger.info(f"Nie można usunąć komendy {name}, nie istnieje")
        
    async def get_commands(self) -> List[str]:
        '''Zwraca listę nazw komend które bot obsługuje aktualnie'''
        return [cmd.command for cmd in await self.__app.bot.get_my_commands()]
        