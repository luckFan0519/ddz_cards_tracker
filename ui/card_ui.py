# ui.py
# -*- coding: utf-8 -*-

"""
UI 入口：斗地主记牌器（两行：牌名 + 剩余数量）
================================================

1) UI 极简：第一行牌名，第二行剩余数量；
2) 后台线程识别，不阻塞 UI；
"""

import os
from PySide6.QtCore import Qt, QThread, QTimer, Slot
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout
)
from core.card_tracker import CardTracker, CardTrackerWorker  # 按你的实际路径改
from config.settings import TOTAL_CARDS
from utils.trans_yolo_names_to_string import trans_yolo_names_to_string


def load_qss(app: QApplication, qss_path: str) -> None:
    """
    加载 QSS 并应用到整个 QApplication。

    为什么这样做：
    - QSS 单独存放，UI 代码干净；
    - 统一应用到 app，上层组件都能继承样式。

    参数：
    - app: QApplication 实例
    - qss_path: QSS 文件路径（例如 ./style.qss）
    """
    # 为了更稳：兼容相对路径（以当前 ui.py 所在目录为基准）
    if not os.path.isabs(qss_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        qss_path = os.path.join(base_dir, qss_path)

    # 文件不存在时不报错，避免影响主程序运行（只提示）
    if not os.path.exists(qss_path):
        print(f"[QSS] File not found: {qss_path}")
        return

    # 读取 QSS 并应用
    with open(qss_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())




class CardUI(QWidget):
    """
    两行记牌器主窗口：
    - 第 0 行：牌名
    - 第 1 行：剩余数量

    特点：
    - 使用 QGridLayout：每张牌占一列，结构最清晰；
    - 使用后台线程 worker：避免 UI 卡顿；
    - 定时器触发 worker 识别（按你的原逻辑：80ms 一次）；
    - busy 防抖：上一轮未结束不触发下一轮。
    """

    def __init__(self):
        super().__init__()

        # -------------------------
        # 窗口基础设置（保持你原设置）
        # -------------------------
        self.setWindowTitle("斗地主记牌器")
        self.setMinimumWidth(700) # 最小宽度

        self.played_cards = {
            "left": "",
            "right": "",
            "self": "",
        }

        # -------------------------
        # 牌序：按 TOTAL_CARDS 的 key 顺序 的逆序
        # （如果你想固定顺序，可以改 TOTAL_CARDS 或在这里写死 list）
        # -------------------------
        self.card_order = list(TOTAL_CARDS.keys())
        self.card_order.reverse()

        # -------------------------
        # UI 结构：根布局 + 网格布局（两行）
        # -------------------------
        root = QVBoxLayout(self) # 创建一个垂直布局（QVBoxLayout）
        root.setContentsMargins(12, 12, 12, 12) # 内边距（布局边缘到窗口边缘的距离），四个数值分别对应：左、上、右、下（单位：像素）。
        root.setSpacing(10)          #设置布局内子控件之间的间距（单位：像素）。



        self.grid = QGridLayout() # 创建一个网格布局对象（QGridLayout）
        self.grid.setHorizontalSpacing(6) # 列与列之间的水平间距（单位：像素）。
        self.grid.setVerticalSpacing(6) #行与行之间的垂直间距（单位：像素）。
        # root.addLayout(self.grid)

        # -------------------------
        # 顶部工具栏（把“重置”放到右上角）
        # -------------------------
        # topbar = QHBoxLayout()
        # topbar.setContentsMargins(0, 0, 0, 0)
        # topbar.setSpacing(6)
        #
        # topbar.addStretch(1)  # 左侧弹簧，把按钮顶到最右


        # -------------------------
        # 重置按钮：点击后重置记牌器
        # -------------------------
        self.btn_reset = QPushButton("重置")
        self.btn_reset.setObjectName("BtnReset")  # 可选：用于 QSS
        self.btn_reset.clicked.connect(self.on_reset_clicked)
        root.addWidget(self.btn_reset)


        # root.addLayout(topbar)

        # grid 放在下面
        root.addLayout(self.grid)

        # -------------------------
        # 额外三行文本（跨整行）
        # -------------------------
        self.self_played_cards_label = QLabel(self.played_cards["self"])
        self.left_played_cards_label = QLabel(self.played_cards["left"])
        self.right_played_cards_label = QLabel(self.played_cards["right"])

        for lbl in (self.self_played_cards_label, self.left_played_cards_label, self.right_played_cards_label):
            lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lbl.setObjectName("InfoLabel")  # 方便 QSS

        col_count = len(self.card_order)

        self.grid.addWidget(self.left_played_cards_label, 2, 0, 1, col_count)
        self.grid.addWidget(self.self_played_cards_label, 3, 0, 1, col_count)
        self.grid.addWidget(self.right_played_cards_label, 4, 0, 1, col_count)

        # -------------------------
        # 保存 label 引用：后续更新用（保持你原逻辑）
        # name_labels：牌名 QLabel
        # count_labels：数量 QLabel
        # -------------------------
        self.name_labels: dict[str, QLabel] = {}
        self.count_labels: dict[str, QLabel] = {}

        # -------------------------
        # 创建两行：
        # row 0：牌名
        # row 1：数量
        # -------------------------
        for col, card in enumerate(self.card_order):
            # --- 牌名 ---
            name = QLabel(str(card))
            name.setAlignment(Qt.AlignCenter)

            # 给 QLabel 设置 objectName，方便 QSS 精准匹配
            # （QSS 中使用 #CardNameLabel 来选中）
            name.setObjectName("CardNameLabel")

            # 牌名也需要区分“已用完”状态（v<=0 时变灰）
            # 用 dynamicProperty：depleted=True/False，让 QSS 控制颜色
            name.setProperty("depleted", False)

            self.grid.addWidget(name, 0, col)
            self.name_labels[card] = name

            # --- 数量 ---
            cnt = QLabel(str(TOTAL_CARDS.get(card, 0)))
            cnt.setAlignment(Qt.AlignCenter)

            # 数量 label 同样设置 objectName，QSS 中用 #CardCountLabel
            cnt.setObjectName("CardCountLabel")
            cnt.setProperty("depleted", False)

            self.grid.addWidget(cnt, 1, col)
            self.count_labels[card] = cnt

        # -------------------------
        # 后台线程/worker（保持你原逻辑）
        # -------------------------
        self.card_tracker = CardTracker()

        # QThread：worker 的执行线程
        self.worker_thread = QThread(self)

        # 你的 worker：执行一次识别，然后 emit result_ready / finished
        self.worker = CardTrackerWorker(self.card_tracker)

        # 把 worker 移动到线程中（关键：让耗时任务不在主线程跑）
        self.worker.moveToThread(self.worker_thread)

        # 信号连接（保持你原逻辑）
        self.worker.result_ready.connect(self.on_result_ready)
        self.worker.error.connect(self.on_worker_error)
        self.worker.finished.connect(self.on_worker_finished)

        # 启动线程
        self.worker_thread.start()

        # -------------------------
        # 定时器触发 worker 跑一次（保持你原逻辑）
        # -------------------------
        self._busy = False  # busy 防抖：上一轮没结束，不触发新一轮

        self.timer = QTimer(self)
        self.timer.setInterval(200)  # 设置定时器的 “触发间隔” 为 200 毫秒（ms）。
        self.timer.timeout.connect(self.request_one_update) # 定义的 request_one_update 方法绑定。
        self.timer.start() # 启动

    @Slot()
    def request_one_update(self):
        """
        定时触发一次后台识别（保持你原逻辑）：
        - busy 防抖：上一轮没结束就 return
        - QTimer.singleShot(0, ...)：
          把调用投递到事件队列，让它在 worker 所在线程执行 do_run_once
        """
        if self._busy:
            return
        self._busy = True

        # 这里保持你的写法：singleShot(0, worker.do_run_once)
        # 意图：让函数在事件循环中异步触发（不堵 UI）
        QTimer.singleShot(0, self.worker.do_run_once)

    @Slot(dict, list, list, list)
    def on_result_ready(self, remain_cards: dict, show_left: list, show_right: list, show_self: list):
        """
        收到 worker 的识别结果（保持你原逻辑）：
        - 只更新“剩余牌数量”
        - v <= 0 时样式变灰
        - v > 0 时样式恢复正常

        注意：
        - 你原代码是在这里直接 setStyleSheet 覆盖样式
        - 现在改为设置 dynamicProperty(depleted) 并强制刷新样式
          这样 QSS 仍然可以做到同样效果，但样式集中在 style.qss
        """
        for card in self.card_order:
            v = remain_cards.get(card, 0)

            # 1) 更新数量文字
            self.count_labels[card].setText(str(v)) # .setText(...)：修改标签内容



            # 更新出牌
            self.self_played_cards_label.setText("本家  " + trans_yolo_names_to_string(show_self))
            self.left_played_cards_label.setText("上家  " + trans_yolo_names_to_string(show_left))
            self.right_played_cards_label.setText("下家  " + trans_yolo_names_to_string(show_right))


            # 2) 设置 depleted 属性：True/False
            depleted = (v <= 0)
            self.name_labels[card].setProperty("depleted", depleted)
            self.count_labels[card].setProperty("depleted", depleted)

            # 3) 强制刷新样式（Qt 对动态属性的 QSS，需要触发重新 polish）
            #    不改变任何逻辑，只是让 QSS 能立即生效
            self.name_labels[card].style().unpolish(self.name_labels[card])
            self.name_labels[card].style().polish(self.name_labels[card])

            self.count_labels[card].style().unpolish(self.count_labels[card])
            self.count_labels[card].style().polish(self.count_labels[card])


    def _reset_ui_to_total(self):
        """
        把 UI 的显示重置为 TOTAL_CARDS：
        - 数量恢复成总数
        - depleted 属性恢复 False
        - 强制刷新 QSS
        """
        for card in self.card_order:
            v = TOTAL_CARDS.get(card, 0)
            self.count_labels[card].setText(str(v))

            self.name_labels[card].setProperty("depleted", False)
            self.count_labels[card].setProperty("depleted", False)

            # 强制刷新样式（让 QSS 立即响应 depleted 变化）
            self.name_labels[card].style().unpolish(self.name_labels[card])
            self.name_labels[card].style().polish(self.name_labels[card])

            self.count_labels[card].style().unpolish(self.count_labels[card])
            self.count_labels[card].style().polish(self.count_labels[card])

    @Slot()
    def on_reset_clicked(self):
        """
        点击“重置”按钮（强制操作，不受 busy 影响）
        """
        # 1) 强制停止定时器，阻断后续识别
        self.timer.stop()

        # 2) 强制解锁 busy（即使当前在识别，也当它结束了）
        self._busy = False

        # 3) 立刻重置 UI（用户马上看到）
        self._reset_ui_to_total()

        # 4) 把 reset 投递到 worker 所在线程执行
        QTimer.singleShot(0, self.worker.reset)

        # 5) 重新启动定时器
        self.timer.start()





    @Slot(str)
    def on_worker_error(self, err_text: str):
        """
        worker 报错（保持你原逻辑）：
        - 不弹窗、不打扰：直接 print
        """
        print("Worker error:\n", err_text)

    @Slot()
    def on_worker_finished(self):
        """
        worker 一轮结束（保持你原逻辑）：
        - 解除 busy，允许下一轮定时触发
        """
        self._busy = False

    def closeEvent(self, event):
        """
        窗口关闭时清理（保持你原逻辑）：
        - 停止 timer
        - 退出线程并等待（最多 1500ms）
        """
        self.timer.stop()
        self.worker_thread.quit()
        self.worker_thread.wait(1500)
        super().closeEvent(event)
