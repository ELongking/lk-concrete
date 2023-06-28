from dbutils.pooled_db import PooledDB
import pymysql


class SqlHandle:
    def __init__(self):
        self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='xxx', db='xxx', port=3306)
        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()
        self.config = {"username": "", "uid": "", "cid": ""}

    def login(self, username: str, password: str) -> bool:
        sql = "SELECT * from `userinfo` WHERE `username` = %s and `password` = %s"
        self.cur.execute(sql, (username, password))
        res = self.cur.fetchall()
        if len(res) == 1:
            sql = "SELECT `uid` from `userinfo` WHERE `username` = %s"
            self.cur.execute(sql, username)
            res = self.cur.fetchall()
            self.config["username"] = username
            self.config["uid"] = res[0]
            return True
        else:
            return False

    def reset(self) -> None:
        self.config = {"username": "", "uid": "", "cid": ""}

    def show_all_cinfo(self) -> dict:
        d = dict()
        uid = self.config["uid"]
        sql = "SELECT `cid`, `cname` from `storageinfo` WHERE `uid` = %s"
        self.cur.execute(sql, uid)
        res = self.cur.fetchall()
        if len(res) > 0:
            for cid, cname in res:
                d[cname] = cid
        return d

    def close(self) -> None:
        self.pool.close()
