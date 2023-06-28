from oss2 import *
import os
import os.path as osp
from typing import Tuple


class OssHandle:
    def __init__(self):
        self.auth = Auth(access_key_id="xxx",
                         access_key_secret="xxx")

        self.bucket = Bucket(self.auth, "xxx", "xxx")

    def download(self, uid: str, cid: str, uname: str, cname: str) -> Tuple[bool, str]:
        save_dir = osp.join("../data", uname, cname)
        if osp.exists(save_dir):
            return False, "文件夹已存在, 请检查并删除或直接导入"
        prefix = f"{uid}/{cid}"
        for obj in ObjectIterator(bucket=self.bucket, prefix=prefix):
            if obj.key[-1] == "/":
                continue
            local_file = obj.key.split("/")[-1]
            self.bucket.get_object_to_file(obj.key, osp.join(save_dir, local_file))
        return True, "success"
