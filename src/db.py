import os
import psycopg2
import datetime

class Database:

    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None
        self.last_connected_time = 0
        self.timeout = 30 * 60  # 30分鐘超時

    def connect_to_database(self):
        host = self.config['host']
        port = self.config['port']
        db_name = self.config['db_name']
        user = self.config['user']
        password = self.config['password']
        sslmode = self.config['sslmode']   #verify-full or #verify-ca
        sslrootcert = self.config['sslrootcert'] #server-ca.pem,  # Server CA 證書路徑
        sslcert = self.config['sslcert'] #client-cert.pem,  # Client 證書路徑
        sslkey = self.config['sslkey'] #client-key.pem  # Client 私鑰路徑

        # 建立連接
        if sslmode in ['verify-full', 'verify-ca']:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port,
                sslmode=sslmode,
                sslrootcert=sslrootcert,
                sslcert=sslcert,
                sslkey=sslkey
            )
        else:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT 1")  # 用來測試連接是否成功
        assert self.cursor.fetchone()[0] == 1
        self.last_connected_time = datetime.datetime.now()

    def check_connect(self):
        if self.conn:
            if (datetime.datetime.now() - self.last_connected_time).total_seconds() > self.timeout:
                self.close_connection()
                self.connect_to_database()
        else:
            self.connect_to_database()

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()

    def query_thread(self, user_id):
        self.cursor.execute(
            """
            SELECT thread_id
            FROM user_thread_table
            WHERE user_id = %s;
            """,
            (user_id,)
        )
        result = self.cursor.fetchone()
        self.last_connected_time = datetime.datetime.now()
        return result[0] if result else None

    def save_thread(self, user_id, thread_id):
        now = datetime.datetime.utcnow()
        self.cursor.execute(
            """
            INSERT INTO user_thread_table (user_id, thread_id, created_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
            thread_id = EXCLUDED.thread_id,
            created_at = EXCLUDED.created_at;
            """,
            (user_id, thread_id, now)
        )
        self.conn.commit()
        self.last_connected_time = datetime.datetime.now()

    def delete_thread(self, user_id):
        self.cursor.execute(
            """
            DELETE FROM user_thread_table
            WHERE user_id = %s;
            """,
            (user_id,)
        )
        self.conn.commit()
        self.last_connected_time = datetime.datetime.now()
