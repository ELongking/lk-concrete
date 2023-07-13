import json
import os
import os.path as osp


def check_case_directory(dirname) -> str:
    tree = os.listdir(dirname)

    if tree != ["config.json", "image", "tabular"]:
        return "文件目录结构错误, 缺少必要文件或文件夹"
    if not osp.isdir(osp.join(dirname, "tabular")):
        return "Tabular 不是文件夹"
    if not osp.isdir(osp.join(dirname, "image")):
        return "Image 不是文件夹"

    return "success"


def import_json_info(dirpath: str) -> list:
    filepath = dirpath + r"/config.json"
    f = open(filepath, "r+", encoding='utf-8')
    data = json.load(f)
    f.close()
    new_data = sorted(data, key=lambda x: x["fileType"] == "image")
    return new_data
