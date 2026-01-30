# -*- coding: utf-8 -*-

"""
UI 入口：斗地主记牌器（两行：牌名 + 剩余数量）
================================================

1) UI 极简：第一行牌名，第二行剩余数量；
2) 后台线程识别，不阻塞 UI；
"""

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import CardUI
from ui.styles import load_qss
from config.settings import BASE_DIR


def main():
    """
    主函数：启动应用程序
    """
    app = QApplication(sys.argv)
    dir_path = BASE_DIR + "\\ui\\ui.qss"
    # print(dir_path)
    load_qss(app, dir_path) # 先注释, 默认的更好看, 以后美化

    w = CardUI()
    w.show()
    sys.exit(app.exec())

#
# if __name__ == "__main__":
#     main()
