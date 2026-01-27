import sys
from PySide6.QtWidgets import QApplication
from ui.card_ui import CardUI, load_qss  # 确保 card_ui.py 里有 load_qss


def main():
    app = QApplication(sys.argv)

    # load_qss(app, "ui.qss") # 先注释, 默认的更好看, 以后美化

    w = CardUI()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
