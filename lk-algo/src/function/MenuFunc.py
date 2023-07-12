from PyQt5.QtWidgets import QFileDialog

from src.ProcessWindow import ProcessWindow
from src.component.MsgBox import ProcessBox, WarningBox
from src.utils.FileUtils import *
from src.utils.ThreadUtils import CustomThread


def download_file(parent: ProcessWindow, cname: str) -> None:
    cid = parent.cid_cname.get(cname)
    _thread = CustomThread(func=parent.oss_handle.download,
                           uid=parent.sql_handle.config["uid"],
                           cid=cid,
                           uname=parent.sql_handle.config["username"],
                           cname=cname)

    ProcessBox(parent, title="提示", text="正在下载中...", thread=_thread).exec()


def directory_import(parent: ProcessWindow):
    folder_path = QFileDialog.getExistingDirectory(parent, '选择需要读取的案例文件夹', "../data")
    if folder_path:
        flag = check_case_directory(folder_path)
        if flag == "success":
            now_cname = folder_path.split('/')[-1]
            parent.cname_label.setText(f" 批次 -> {now_cname} ")
            parent.now_cname = now_cname
            parent.config = import_json_info(folder_path)
            parent.is_import.value = True
        else:
            parent.is_import.value = False
            WarningBox(parent, "出错", flag)
    else:
        WarningBox(parent, "出错", "请选择文件夹")
