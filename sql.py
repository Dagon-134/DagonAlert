import psycopg


class Repo:
    
    def __init__(self, connect):
        if connect is None:
            raise ValueError("Переменная окружения TABLE не задана!")
        self.connect = psycopg.connect(connect)
    
    def isUserExist(self, tg_id: int) -> bool:
        with self.connect.cursor() as cursor:
            try:
                cursor.execute("""SELECT tg_id FROM users WHERE tg_id = %s""", (tg_id,))
                id = cursor.fetchall()
                if id[0] is None:
                    return False
                return True
            except IndexError:
                return False
            
    
    def addUser(self, tg_id: int):
        with self.connect.cursor() as cursor:
            cursor.execute("""INSERT INTO users(tg_id) VALUES(%s)""", (tg_id,))
            print('kom')
            self.connect.commit()
            print('kom1')
            cursor.execute("""SELECT user_id FROM users WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchall()
            if user_id[0] is None:
                print('айди пуст')
            with self.connect.cursor() as cursor2:
                cursor2.execute("""INSERT INTO customization(user_id) VALUES(%s)""", (user_id[0]))
                self.connect.commit()
            
            
    def getTgId(self):
        with self.connect.cursor() as cursor:
            cursor.execute("""SELECT tg_id FROM users""")
            tg_id_all_users = cursor.fetchall()
            list_og_tgid = []
            for i in tg_id_all_users:
                list_og_tgid.append(i[0])
            
            return list_og_tgid
        
    def getTimerInformation(self, tg_id: int):
        with self.connect.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM users WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchall()
            if user_id[0] is None:
                pass
            with self.connect.cursor() as cursor2:
                cursor2.execute("""SELECT timer FROM customization WHERE user_id = %s""", (user_id[0],))
                
    def changeTimerImformation(self, new_cust, tg_id):
        with self.connect.cursor() as cursor:
            cursor.execute("""SELECT user_id FROM users WHERE tg_id = %s""", (tg_id,))
            user_id = cursor.fetchall()
            print(user_id[0][0])
            if user_id[0] is None:
                pass
            with self.connect.cursor() as cursor2:
                cursor2.execute("""UPDATE customization SET timer = %s WHERE user_id = %s""", (new_cust, user_id[0][0]))
                self.connect.commit()