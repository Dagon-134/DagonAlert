from dotenv import load_dotenv
import os

import psycopg

load_dotenv()
db_url = os.getenv('TABLE')
if db_url is None:
    raise ValueError("Переменная окружения TABLE не задана!")
connection = psycopg.connect(db_url)

class Repo:
    
    def isUserExist(self, tg_id) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT tg_id FROM users WHERE tg_id = %s""", (tg_id,))
            id = cursor.fetchall()
            if id[0] is not None:
                return True
            return False
    
    def addUser(self, tg_id: int):
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO users(tg_id) VALUES(%s)""", (tg_id,))
            connection.commit()