"""
@Filename:   commons/databases
@Author:      三木
@Time:        2023/1/29 14:41
@Describe:    ...
"""
import json

import pymysql as MySQLdb
import psycopg2
from psycopg2.extras import NamedTupleCursor
from commons import settings



class DBServer:
    def __init__(self, *args, **kwargs):
        self.db = MySQLdb.connect(*args, **kwargs)
        self.c = self.db.cursor()  # 创建新的会话

    def execute_sql(self, sql):
        self.c.execute(sql)  # 执行sql命令

        res = self.c.fetchone()  # 返回单行结果
        # res = self.c.fetchall()  # 返回多行结果
        return res





class PostgresHandler:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            cursor_factory=NamedTupleCursor
        )
        self.cur = self.conn.cursor()

    def execute_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def close_connection(self):
        self.cur.close()
        self.conn.close()



if __name__ == '__main__':
    # mysql
    db = DBServer(
        host=settings.db_host,  # IP
        port=int(settings.db_port),  # 端口
        user=settings.db_user,  # 用户名
        password=settings.db_password,  # 密码
        database=settings.db_database,  # 库名
    )

    # pgsql
    postgres_handler = PostgresHandler("192.168.2.130", "postgres", "postgres", "123")

    query_result = postgres_handler.execute_query("""
        SELECT state
        FROM public."event"
        WHERE id=141958;
        """)
    for row in query_result:
        # 使用字段名访问值
        print(row.state)  # 替换为你的实际字段名

    postgres_handler.close_connection()


