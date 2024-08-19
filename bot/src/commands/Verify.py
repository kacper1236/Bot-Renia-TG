from telegram import Update
from telegram.ext import CallbackContext
from . import SlashCommand, command_with_logs
from ..bot.logs import logger
from ..integrations import ReniaBackendClient
import jwt, base64, requests, json, os
import jwcrypto.jwk as jwk
import psycopg2

class Verify(SlashCommand):
    '''
    Komenda ustawiana poprzez UI Administratorskie
    '''
    name = "verify"

    link: str = os.environ.get("LINK")

    currentToken = ""
    errors = 0
    idUser = None
    telegramUserID = 0
    conn = psycopg2.connect("postgresql://my_user:my_password@postgres/my_database") #na pewno się przyda
    curr = conn.cursor()
    def markError(self): 
        self.errors += 1
        if self.errors > 3:
            self.currentToken = ""

    async def downloadJwkKeys(self, issuser: str):
        keys = requests.get(issuser)
        return keys.json()
    
    def checkIfIssIsAllowed(self, issuser: str):
        ISS: str = os.environ.get("ISS")
        if issuser != ISS:
            return False
        return True

    async def connect(self):
        logger.info("pobieranie tokenu")
        try:
            token = ReniaBackendClient.login_to_foxcons()
            tokenPart = token.split(".")[1]
            missingPadding = len(tokenPart) % 4
            payload = json.loads(base64.b64decode(tokenPart + missingPadding * "=").decode("utf-8")) #musi zawierać odpowiedni link
            if self.checkIfIssIsAllowed(payload["iss"]) == False:
                raise Exception("Nieautoryzowany dostęp lub błędny ISS w env")
            keys = await self.downloadJwkKeys(payload["iss"])
            isFailure = True
            for i in keys["keys"]:
                try:
                    key = jwk.JWK.from_json(json.dumps(i))
                    jwt.decode(token, jwk.JWK.export_to_pem(key), algorithms = "ES512", audience = "seti", issuer = payload["iss"])
                    isFailure = False
                    break
                except (jwt.exceptions.InvalidTokenError,
                        jwt.exceptions.ExpiredSignatureError,
                        jwt.exceptions.DecodeError,
                        jwt.exceptions.ImmatureSignatureError) as e:
                    raise Exception(e)
                except Exception as e:
                    logger.info(repr(e))
            if not isFailure:
                self.currentToken = token
                self.errors = 0
            else:
                raise Exception("Nie można zweryfikować tokenu (signature not verify or expired)")
        except Exception as e:
            logger.info(e)
            logger.info(f"Renia napotkała błąd podczas logowania się do Foxcons! {e}")  
            self.markError()
            raise Exception(e)
    
    def isWorking(self):
        return self.errors == 0 and self.currentToken != ""
    
    async def prepareConnection(self):
        if self.currentToken == "":   
            return await self.connect()
        
        if self.errors > 0:
            await self.connect()
        
        if self.errors > 3:
            raise Exception("Nie można połączyć się z Foxcons")

    async def fetchUserData(self, ID):
        if ID.__class__ == dict:
            return self.matchErrrorsInResponse()
        try:
            logger.info("Pobieranie danych")
            
            data = requests.get(f"{self.link}/app/event/*/bot/profile/{ID}", 
                                headers = {"Authorization": f"Bearer {self.currentToken}"}).json()
            try:
                if data.status_code != 200:
                    raise Exception("Błąd podczas pobierania danych")
            except:
                pass
            logger.info(data)
            try:
                username = data['displayName']
                id_username = ID
                is_verified = True
                room = data['room'].get("selected") if isinstance(data['room'], dict) else False
                plan_id = data['plan'].get("id") if isinstance(data['plan'], dict) else False
                plan_selected = data['plan'].get("selected") if isinstance(data['plan'], dict) else False
                plan_paid = data['plan'].get("paid") if isinstance(data['plan'], dict) else False
                self.curr.execute(f"""INSERT INTO verified_users (id, username, id_username, is_verified, room, plan_id, plan_selected, plan_paid) 
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                  ON CONFLICT (id_username) DO UPDATE
                                  SET id = %s, username = %s, id_username = %s, is_verified = %s, room = %s, plan_id = %s, plan_selected = %s, plan_paid = %s""", 
                                  (self.telegramUserID, username, id_username, is_verified, room, plan_id, plan_selected, plan_paid, #INSERT
                                   self.telegramUserID, username, id_username, is_verified, room, plan_id, plan_selected, plan_paid,)) #UPDATE

                self.conn.commit()
                
                logger.info("Dane zostały dodane do bazy")
            except Exception as e:
                raise Exception(f"Błąd podczas dodawania danych do bazy: {e}")
        except Exception as e:
            logger.info("Nie można pobrać danych")
            logger.info(e)
            raise Exception(e)

    def matchErrrorsInResponse(self):
        match self.idUser["statusCode"]:
            case 409:
                raise Exception("Potrzebne jest wygenerowanie nowego tokenu")
            case 404:
                raise Exception("Token nieznany, wygeneruj nowy")
            case 403:
                raise Exception("Brak dostępu do tej funkcji") #spróbuj się ponownie zalogować jako bot, albo wyłącz funkcjonalność
            case 401:
                raise Exception("Brak autoryzacji")
            case 400:
                raise Exception("Błędnie podane dane")
            case 500:
                raise Exception("Błąd serwera")
            case 503:
                raise Exception("Strona chwilowo niedostępna")
            case 410:
                raise Exception("Foncons maintance mode off")
            case _:
                raise Exception(f"Nieznany błąd {self.idUser['statusCode']}")

    async def verify(self, token, name, ID):
        try:
            self.idUser = requests.post(f"{self.link}/app/event/*/bot/verify/telegram", 
                              json = {"token": token, "name": name, "id": ID}, 
                              headers = {"Authorization": f"Bearer {self.currentToken}"}).json()
            if self.idUser.__class__ == int:
                return
            else:
                self.matchErrrorsInResponse()
        except Exception as e:
            logger.info("Nie można zweryfikować tokenu")
            logger.info(e)
            raise Exception(e)
    
    @command_with_logs
    async def callback(self, update: Update, context: CallbackContext):
        try:
            logger.info(context.args[0])
            self.telegramUserID = update.message.from_user.id
            await self.prepareConnection()
            await update.message.reply_text(self.currentToken)
            await self.verify(context.args[0], update.message.from_user.name, update.message.from_user.id)
            await self.fetchUserData(self.idUser)
            '''
                1. User podał /api <token foxconsów>
                    zapisujemy sobie token do pamięci i przechodzimy kroku VERIFY
                2. User podał /api ale bez tokenu (conversation handler)
                    przechodzimy do proszenia usera o wklejenie tokenu
                    przyjmujemy jego token i zapisujemy i przechodzi do kroku VERIFY

                VERIFY. 
                    wysyłamy na {url}/app/event/*/bot/verify/telegram [PUT] info o userze {token, name, id}, token to wysłany token przez usera, name to @ usera, id to id usera w tg
                    foxcons odpowie <id> - id usera w foxcons

                FETCH USER DATA.
                    wysyłamy na {url}/app/event/*/bot/profile/<id> [GET]
                    foxcons odpowie: (tymczasowo tylko tyle - potem jeszcze dodatkowe dane - jak np stan płatności etc)
                    {
                        id: number;
                    }
            '''
        except Exception as e:
            self.markEerror()
            logger.info(f"Renia napotkała błąd podczas pracy! {e}")