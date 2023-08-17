import os
import os.path as osp
from random import randint

import cv2.config


def remove_some_images(delete_ratio=0.4):
    path = r"D:\Chrome_Download\dogs\image"
    for batch in os.listdir(path):
        file_list = os.listdir(osp.join(path, batch))
        n = len(file_list)
        for _ in range(int(delete_ratio * n)):
            ans_len = len(file_list)
            remove_name = file_list.pop(randint(0, ans_len - 1))
            os.remove(osp.join(path, batch, remove_name))


def main():
    remove_some_images()
    path = r"D:\Chrome_Download\dogs\image"
    f = open(r"D:\Chrome_Download\dogs\annotation\labels.txt", "w", encoding='utf-8')
    for batch in os.listdir(path):
        for filename in os.listdir(osp.join(path, batch)):
            f.write(f"{filename} {batch}\n")
    f.close()


if __name__ == '__main__':
    print(cv2.config.BINARIES_PATHS)
