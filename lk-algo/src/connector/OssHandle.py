import os

from oss2 import *
import os.path as osp
from typing import Tuple
import yaml


class OssHandle:
    def __init__(self):
        self._init_connection()

    def _init_connection(self):
        f = open("../assets/config.yml")
        cfg = yaml.safe_load(f)["aliyun"]
        f.close()

        self.auth = Auth(access_key_id=cfg["access_key_id"],
                         access_key_secret=cfg["access_key_secret"])

        self.bucket = Bucket(self.auth, cfg["endpoint"], cfg["bucket_name"])

    def download(self, uid: str, cid: str, uname: str, cname: str) -> str:
        save_dir = osp.join("../data", uname, cname)
        if osp.exists(save_dir):
            return "文件夹已存在, 请检查并删除或直接导入"
        else:
            os.makedirs(save_dir)
            os.makedirs(osp.join(save_dir, "tabular"))
            os.makedirs(osp.join(save_dir, "image"))
        prefix = f"{uid}/{cid}"

        for obj in ObjectIterator(bucket=self.bucket, prefix=prefix):
            if obj.key[-1] == "/":
                continue
            local_file = "/".join(obj.key.split("/")[2:])
            self.bucket.get_object_to_file(obj.key, osp.join(save_dir, local_file))
        return "success"
