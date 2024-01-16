# tag/tag_client.py

import pymysql

class TagClient:
    def __init__(self, host='127.0.0.1', port=3721, user='root', password='vetec3721', database='ems'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_data(self):
        query = ("SELECT t.tagname, tp.is_usage, tp.calc_type "
                 "FROM tags t "
                 "LEFT JOIN tag_packages tp ON tp.tag_package_id = t.tag_package_id "
                 "WHERE CAST(REGEXP_REPLACE(t.tagname, '[^0-9]', '') AS UNSIGNED) < 900 "
                 "and tp.is_usage = 1")
        rows = self.execute_query(query)
        return [self._format_result(row) for row in rows]

    @staticmethod
    def _format_result(row):
        tagname, is_usage, calc_type = row
        return {
            "tagname": tagname,
            "isUsage": bool(is_usage),
            "calcType": calc_type
        }