import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import CardUI
from ui.styles import load_qss
from config.settings import BASE_DIR

def main():
    app = QApplication(sys.argv)
    dir_path = BASE_DIR + "\\ui\\ui.qss"
    # print(dir_path)
    load_qss(app, dir_path) # 先注释, 默认的更好看, 以后美化

    w = CardUI()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
