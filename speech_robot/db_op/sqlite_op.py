import sqlite3, json, expandvars, os, uuid
from os.path import expanduser
from dotenv import load_dotenv
from handy_tool.time_utils import get_curtime_info
from loguru import logger
from common.schema import Left, Right
import traceback
from typing import Union, List
from speech_robot.db_op.common_schema import TokenType

def get_dbfile():
    load_dotenv("../.env.template")
    db_dir = os.getenv("DB_DIR")
    return f"{db_dir}\\speech_db"

db_file = get_dbfile()

def execute_sql(sql: str, data: List) -> Union[Left, Right]:
    conn = None
    cursor = None

    if data and len(data) == 0:
        logger.info(f"no data on {sql}")
        return Right()

    execute_flag = True
    execute_res = []
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        if not data:
            cursor.execute(sql)
        elif len(data) == 1:
            cursor.execute(sql, data[0])
        else:
            cursor.executemany(sql, data)
        conn.commit()

        if sql.startswith("select"):
            execute_res = cursor.fetchall()

    except Exception as e:
        execute_flag = False
        logger.error(f"{str(e)}: {sql}")
        traceback.print_exc()
    finally:
        if conn:
            cursor.close()
        if conn:
            conn.close()
    return (Left(res=execute_res) if execute_flag else Right())

def handle_exec_re(either: Union[Left, Right], faild_msg: str) -> List:
    match either:
        case Left(res=res):
            return res
        case Right(msg=msg):
            logger.error(f"handle_exec_re by '{msg}': {faild_msg}")
            return []
        case _:
            return []

# 创建用户
def create_new_user(name: str) -> List:
    user_uuid = str(uuid.uuid1())
    current_time_info = get_curtime_info()
    data = [
        (name, user_uuid, current_time_info[0], current_time_info[1]),
    ]
    sql = 'insert into user (name, uuid, create_time, create_time_real) values (?, ?, ?, ?)'
    return handle_exec_re(execute_sql(sql, data), f"execute sql failed: create_new_user({name})")

# 查看用户
def search_user(name: str):
    sql = 'select * from user where name = ?'
    return handle_exec_re(execute_sql(sql, [(name, )]), f"execute sql failed: search_user({name})")

# 查看用户 token
def search_user_token(name: str, type: TokenType):
    sql = "select * from user_token where user_id = (select id from user where name = (?)) and type=(?)"
    return handle_exec_re(execute_sql(sql, [(name, type.value, )]), f"execute sql failed: search_user_token({name})")

# 更新用户当前token状态
def update_user_token(name: str, token: int, type: TokenType):
    user_record = search_user(name)

    if len(user_record) == 0:
        return Right("update t failed: no user found by name")

    # 判断是否有用户记录
    token_res = search_user_token(name, type)

    user_id = user_record[0][0]
    user_name = user_record[0][1]
    current_time_info = get_curtime_info()

    if len(token_res) == 0:

        sql = f"""
        insert into user_token (user_id, token, type, create_time, create_time_real, update_time, update_time_real)
        select id, {token}, "{type.value}", "{current_time_info[0]}", {current_time_info[1]}, "{current_time_info[0]}", {current_time_info[1]}
        from user where name="{user_name}"
        """
        handle_exec_re(execute_sql(sql, None), f"execute sql failed: update_user_token({name}, {token}, {type.name})")

        # TODO: verity 应该改为最大查询最大id
        verify_sql = f"select * from user_token where user_id = {user_id}"

        insert_res = handle_exec_re(execute_sql(verify_sql, None),
                       f"execute sql failed: update_user_token insert verify_sql({user_id})")
        return insert_res
    else:
        sql = f"""
        update user_token 
        set token = {token}, update_time="{current_time_info[0]}", update_time_real={current_time_info[1]} 
        where type = "{type.value}" and user_id = {user_id}
        """

        # 先记录之前的值
        insert_user_token_history(user_id)
        handle_exec_re(execute_sql(sql, None), f"execute sql failed: update_user_token({name}, {token}, {type.name})")

        # TODO: verity 更新的记录该怎么做？
        verify_sql = f"select * from user_token where user_id = {user_id}"
        update_res = handle_exec_re(execute_sql(verify_sql, None),
                                    f"execute sql failed: update_user_token update verify_sql({user_id})")
        return update_res

# 插入用户token更新历史
def insert_user_token_history(user_id: int):
    current_time_info = get_curtime_info()
    data = [ (user_id, ) ]
    sql = f"""
        insert into user_token_history (user_id, token, type, create_time, create_time_real) 
        select user_id, token, type, "{current_time_info[0]}", {current_time_info[1]} 
        from user_token where user_id = (?)
    """
    return handle_exec_re(execute_sql(sql, data), f"execute sql failed: insert_user_token_history({user_id})")

def run():
    pass

if __name__ == "__main__":
    run()