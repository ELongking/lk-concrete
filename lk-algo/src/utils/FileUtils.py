import os
import os.path as osp


def check_case_directory(dirname):
    exist_json, exist_dir = False, False

    for file in os.listdir(dirname):
        if file.endswith("json"):
            exist_json = True
        if osp.isdir(file) and file in ["tabular", "image"]:
            exist_dir = True
    return exist_dir and exist_json
