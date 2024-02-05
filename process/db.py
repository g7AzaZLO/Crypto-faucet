import sqlite3
from os.path import isfile
from settings.config import DATABASE_FILE
from process.other import ping_admin_dm


async def create_db() -> None:
    if isfile(DATABASE_FILE):
        print("Database exists...")
        await ping_admin_dm("Database exists...")
    else:
        print("Creating Database...")
        execute_non_query("CREATE TABLE faucetClaims (USER_ID INTEGER, ADDR TEXT, DT FLOAT);")
        print("Database created successfully")
        await ping_admin_dm("Database created successfully")


def execute_non_query(command) -> None:
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute(command)
    conn.commit()
    conn.close()

