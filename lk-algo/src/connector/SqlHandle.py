from dbutils.pooled_db import PooledDB
import pymysql


class SqlHandle:
    def __init__(self):
        self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='19980917', db='lk-concrete', port=3306)
        self.conn = self.pool.connection()
        self.cur = self.conn.cursor()
        self.config = {"username": "", "uid": ""}

    def login(self, username: str, password: str) -> bool:
        sql = "SELECT * from `userinfo` WHERE `username` = %s and `password` = %s"
        self.cur.execute(sql, (username, password))
        res = self.cur.fetchall()
        if len(res) == 1:
            self.config["username"] = username
            self.config["uid"] = res[0][1]
            return True
        else:
            return False

    def reset(self) -> None:
        self.config = {"username": "", "uid": ""}

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

    def get_task_type(self, cid: str, mode: str) -> str:
        if mode == "tabular":
            sql = "SELECT `tabularType` from `storageinfo` WHERE `cid` = %s"
        else:
            sql = "SELECT `imageType` from `storageinfo` WHERE `cid` = %s"
        self.cur.execute(sql, cid)
        res = self.cur.fetchall()
        return res[0][0]

    def get_cname(self, cid: str):
        sql = "SELECT `cname` from `storageinfo` WHERE `cid` = %s"
        self.cur.execute(sql, cid)
        res = self.cur.fetchall()
        return res[0][0]

    def close(self) -> None:
        self.pool.close()
