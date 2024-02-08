import sqlite3
from os.path import isfile
from settings.config import DATABASE_FILE
from process.other import ping_admin_dm

# Проверка наличии базы и ее создание
async def create_db() -> None:
    if isfile(DATABASE_FILE):
        print("Database exists...")
        await ping_admin_dm("Database exists...")
    else:
        print("Creating Database...")
        await execute_non_query("CREATE TABLE faucetClaims (USER_ID INTEGER, ADDR TEXT, DT FLOAT);")
        print("Database created successfully")
        await ping_admin_dm("Database created successfully")

# Выполнение запроса в базе
async def execute_non_query(command) -> None:
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute(command)
    conn.commit()
    conn.close()

# Удаление из базы юзера по id
async def delete_user_from_db(user):
    await execute_non_query(f"DELETE FROM faucetClaims WHERE USER_ID = {user}")
