from . import command_with_logs, SlashCommand
from ..bot.logs import logger
import requests, os

class Report(SlashCommand):
    
    name = 'report'
    description = 'Zgłoś wiadomość użytkownika'
    is_visible = False
    
    @command_with_logs
    async def callback(self, update, context):
        if not update.message.reply_to_message:
            return await update.message.reply_text("Aby zgłosić wiadomość, musisz na nią odpowiedzieć")

        json = {
            'user': f"@{update.message.reply_to_message.from_user.username}",
            'message': (
                update.message.reply_to_message.text
                or "Wiadomość nie jest tekstem, należy zobaczyć"
            ),
            'link': update.message.reply_to_message.link,
            'reason': {
                'text': " ".join(context.args) if context.args else "Brak powodu",
                'user': update.message.from_user.username
            },
        }
        
        #logger.info(json)
        response = requests.post(os.environ.get('REPORT_RENIA'), json = json)
        if response.status_code == 200:
            return await update.message.reply_to_message.reply_text('Zgłoszenie zostało wysłane')
        else: 
            logger.info(response.text)
            return await update.message.reply_to_message.reply_text('Zgłoszenie nie zostało wysłane, skontaktuj się z administratorem')
        
        