from speech_robot.db_op.sqlite_op import *
from speech_robot.db_op.common_schema import TokenType

def test_insert_user():
    print(create_new_user("test_user_6"))

def test_search_user():
    search_user("test_user_3")

def test_search_user_token():
    print(search_user_token("test_user_3", TokenType.KIMI))

def test_update_user_token():
    update_user_token("test_user_3", 60, TokenType.KIMI)


def run():
    # test_insert_user()
    # update_user_token()
    # test_search_user()
    # test_search_user_token()
    test_update_user_token()


if __name__ == "__main__":
    run()