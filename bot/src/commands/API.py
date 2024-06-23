from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs
from ..bot.logs import logger
from ..integrations import ReniaBackendClient
import jwt, base64, json

class API(SlashCommand):
    '''
    Komenda ustawiana poprzes UI Administratorskie
    '''
    name = "api"

    currentToken = ""
    errors = 0
    def markError(self): 
        self.errors += 1
        if self.errors > 3:
            self.currentToken = ""

    async def connect(self):
        try:
            token = ReniaBackendClient.login_to_foxcons()
            logger.error(token)
            # verify it using https://pyjwt.readthedocs.io/en/latest/usage.html    OIDC part at the end of page
            tokenPart = token.split(".")[0]
            # alg = base64.b64decode(tokenPart).decode()
            # a = jwt.decode(token, algorithms = json.loads(alg)["alg"], verify = False, verify_signature = False)
            
            self.currentToken = token
            self.errors = 0
        except Exception:
            self.markEerror()
            logger.exception("Renia napotkała błąd podczas logowania się do Foxcons!")      
      
    def isWorking(self):
        return self.errors == 0 and self.currentToken != ""
    
    async def prepareConnection(self):
        if self.currentToken == "":   
            return await self.connect()
        
        if self.errors > 0:
            await self.connect()
        
        if self.errors > 3:
            raise Exception("Nie można połączyć się z Foxcons")
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        try:
            await self.prepareConnection()
            await update.message.reply_text(context.args[0])
            '''
                1. User podał /api <token foxconsów>
                    zapisujemy sobie token do pamięci i przechodzimy kroku VERIFY
                2. User podał /api ale bez tokenu (conversation handler)
                    przechodzimy do proszenia usera o wklejenie tokenu
                    przyjmujemy jego token i zapisujemy i przechodzi do kroku VERIFY

                VERIFY. 
                    wysyłamy na {url}/app/event/*/bot/link/telegram [PUT] info o userze {token, name, id}, token to wysłany token przez usera, name to @ usera, id to id usera w tg
                    foxcons odpowie <id> - id usera w foxcons

                FETCH USER DATA.
                    wysyłamy na {url}/app/event/*/bot/profile/<id> [GET]
                    foxcons odpowie: (tymczasowo tylko tyle - potem jeszcze dodatkowe dane - jak np stan płatności etc)
                    {
                        id: number;
                    }
            '''
        except Exception:
            self.markEerror()
            logger.exception("Renia napotkała błąd podczas pracy!")