from . import command_with_logs, SlashCommand
from ..bot.logs import logger
from ..integrations import ReniaBackendClient

def get_static_commands():
    from ..bot.main import static_commands
    return static_commands

class Reload(SlashCommand):
    
    name = 'reload'
    description = 'Reload commands'
    is_visible = False

    def __init__(self, manager):
        self.__manager = manager

    @command_with_logs
    async def callback(self, update, context):
        '''Reload commands from backend
        This command will fetch commands from backend and add new ones to the bot
        TO DO: This command does not remove old commands, only adds new ones
        '''
        
        list_commands = await self.__manager.get_commands()
        refreshed_from_backend = ReniaBackendClient.get_commands()
        
        static_commands = get_static_commands()
        backend_names = {cmd.name for cmd in refreshed_from_backend}
        static_names = {cmd.name for cmd in static_commands}
        local_names = set(list_commands)
        
        for i in list_commands:
            if i not in backend_names and i not in static_names:
                self.__manager.remove_command(i)
                logger.info(f"Command {i} is no longer present in backend, removing it")

        for cmd in refreshed_from_backend:
            if cmd.name not in local_names:
                self.__manager.add_command(cmd)
                logger.info(f"Command {cmd.name} added from backend")

        await update.message.reply_text("Pomyślnie przeładowano komendy")