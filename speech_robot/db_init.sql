CREATE TABLE user(
    id             INTEGER primary key autoincrement not null,
    name           varchar(50)    UNIQUE NOT NULL,
    uuid           varchar(36)    NOT NULL,
    create_time    varchar(19)    NOT NULL,
    create_time_real    real        NOT NULL
);

-- TOKEN 当前状态
CREATE TABLE user_token(
    id             INTEGER primary key autoincrement not null,
    user_id        INTEGER  NOT NULL,
    token          INTEGER  NOT NULL,
    type           varchar(10)     NOT NULL,
    create_time    varchar(19)    NOT NULL,
    create_time_real    real        NOT NULL,
    update_time    varchar(19)     NOT NULL,
    update_time_real    real        NOT NULL
);

-- TOKEN 消耗，购买历史记录
CREATE TABLE user_token_history (
    id             INTEGER primary key autoincrement not null,
    user_id        INTEGER  NOT NULL,
    token          INTEGER  NOT NULL,
    type           varchar(10)     NOT NULL,
    create_time    varchar(19)     NOT NULL,
    create_time_real    real        NOT NULL
);

-- 角色模板
CREATE TABLE ai_role_template (
    id              INTEGER primary key autoincrement not null,
    name            nvarchar(100)     NOT NULL,
    content         TEXT     NOT NULL,
    create_time    varchar(19)    NOT NULL,
    create_time_real    real        NOT NULL,
    update_time    varchar(19)     NOT NULL,
    update_time_real    real        NOT NULL
)

-- 用户历史记录
CREATE TABLE user_history (
    id              INTEGER primary key autoincrement not null,
    role            varchar(10)     NOT NULL,
    content         TEXT     NOT NULL,
    create_time    varchar(19)    NOT NULL,
    create_time_real    real        NOT NULL,
    update_time    varchar(19)     NOT NULL,
    update_time_real    real        NOT NULL
);