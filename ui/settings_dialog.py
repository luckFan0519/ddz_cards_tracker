# -*- coding: utf-8 -*-

"""
设置对话框模块
提供应用程序的设置界面，包括基本设置和高级设置
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QTabWidget
)


class SettingsDialog(QDialog):
    """
    设置对话框
    提供基本设置和高级设置两个标签页，用于配置应用程序的各种参数
    """

    def __init__(self, parent=None, on_reset_callback=None, on_interval_change_callback=None, on_layout_change_callback=None, on_device_change_callback=None, on_reset_time_change_callback=None, on_frame_length_change_callback=None, on_always_on_top_change_callback=None, on_show_played_cards_change_callback=None, on_debug_mode_change_callback=None):
        """
        初始化设置对话框

        参数:
            parent: 父窗口
            on_reset_callback: 重置回调函数
            on_interval_change_callback: 检测间隔改变回调函数
            on_layout_change_callback: 布局配置改变回调函数
            on_device_change_callback: 设备选择改变回调函数
            on_reset_time_change_callback: 重置时间改变回调函数
            on_frame_length_change_callback: 帧长度改变回调函数
            on_always_on_top_change_callback: 是否显示在最上层改变回调函数
            on_show_played_cards_change_callback: 是否显示玩家所出的牌改变回调函数
            on_debug_mode_change_callback: 调试模式改变回调函数
        """
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumSize(600, 400)

        self.on_reset_callback = on_reset_callback
        self.on_interval_change_callback = on_interval_change_callback
        self.on_layout_change_callback = on_layout_change_callback
        self.on_device_change_callback = on_device_change_callback
        self.on_reset_time_change_callback = on_reset_time_change_callback
        self.on_frame_length_change_callback = on_frame_length_change_callback
        self.on_always_on_top_change_callback = on_always_on_top_change_callback
        self.on_show_played_cards_change_callback = on_show_played_cards_change_callback
        self.on_debug_mode_change_callback = on_debug_mode_change_callback

        # 创建标签页控件
        self.tab_widget = QTabWidget(self)

        # 创建标签页
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # 添加标签页
        self.tab_widget.addTab(self.tab1, "基本设置")
        self.tab_widget.addTab(self.tab2, "高级设置")
        self.tab_widget.addTab(self.tab3, "关于")

        # 创建布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)

        # 在基本设置标签页中添加控件
        self._setup_basic_settings()

        # 在高级设置标签页中添加控件
        self._setup_advanced_settings()

        # 在关于标签页中添加控件
        self._setup_about_settings()

    def _setup_basic_settings(self):
        """
        在基本设置标签页中添加控件
        包括：重置按钮、布局配置、设备选择、显示在最上层、显示出牌
        """
        # 创建基本设置页面的布局
        basic_layout = QVBoxLayout(self.tab1)
        basic_layout.setContentsMargins(20, 20, 20, 20)
        basic_layout.setSpacing(20)

        # 第一行：重置按钮
        reset_layout = QHBoxLayout()
        self.btn_reset = QPushButton("重置记牌器")
        self.btn_reset.setObjectName("BtnReset")
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        reset_layout.addWidget(self.btn_reset)
        reset_layout.addStretch()
        basic_layout.addLayout(reset_layout)

        # 第二行：布局配置设置
        layout_config_layout = QHBoxLayout()
        layout_label = QLabel("布局配置：")
        layout_label.setMinimumWidth(80)
        self.combo_layout = QComboBox()
        self.combo_layout.setObjectName("LayoutCombo")
        # 注意：在添加选项和设置初始索引前不要连接信号，
        # 否则构造对话框时会触发回调，导致主窗口的布局被重置
        # 加载布局配置选项
        from config.settings import WINDOW_LAYOUTS
        layout_names = list(WINDOW_LAYOUTS.keys())
        # 在填充和初始化索引时屏蔽信号，避免在构造时触发 on_layout_change 回调
        self.combo_layout.blockSignals(True)
        self.combo_layout.addItems(layout_names)
        if layout_names:
            self.combo_layout.setCurrentIndex(0)
        self.combo_layout.blockSignals(False)
        # 现在再连接信号，用户交互时才会触发回调
        self.combo_layout.currentIndexChanged.connect(self._on_layout_changed)

        layout_config_layout.addWidget(layout_label)
        layout_config_layout.addWidget(self.combo_layout)
        layout_config_layout.addStretch()
        basic_layout.addLayout(layout_config_layout)

        # 第三行：设备选择设置
        device_layout = QHBoxLayout()
        device_label = QLabel("设备选择(重启生效)：")
        device_label.setMinimumWidth(80)
        self.combo_device = QComboBox()
        self.combo_device.setObjectName("DeviceCombo")
        self.combo_device.addItems(["CPU", "GPU"])
        self.combo_device.currentIndexChanged.connect(self._on_device_changed)
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.combo_device)
        device_layout.addStretch()
        basic_layout.addLayout(device_layout)

        # 第四行：是否显示在最上层
        always_on_top_layout = QHBoxLayout()
        always_on_top_label = QLabel("显示在最上层：")
        always_on_top_label.setMinimumWidth(80)
        self.combo_always_on_top = QComboBox()
        self.combo_always_on_top.setObjectName("AlwaysOnTopCombo")
        self.combo_always_on_top.addItems(["否", "是"])
        self.combo_always_on_top.currentIndexChanged.connect(self._on_always_on_top_changed)
        always_on_top_layout.addWidget(always_on_top_label)
        always_on_top_layout.addWidget(self.combo_always_on_top)
        always_on_top_layout.addStretch()
        basic_layout.addLayout(always_on_top_layout)

        # 第五行：是否显示玩家所出的牌
        show_played_cards_layout = QHBoxLayout()
        show_played_cards_label = QLabel("显示出牌：")
        show_played_cards_label.setMinimumWidth(80)
        self.combo_show_played_cards = QComboBox()
        self.combo_show_played_cards.setObjectName("ShowPlayedCardsCombo")
        self.combo_show_played_cards.addItems(["否", "是"])
        self.combo_show_played_cards.currentIndexChanged.connect(self._on_show_played_cards_changed)
        show_played_cards_layout.addWidget(show_played_cards_label)
        show_played_cards_layout.addWidget(self.combo_show_played_cards)
        show_played_cards_layout.addStretch()
        basic_layout.addLayout(show_played_cards_layout)

        # 第六行：调试模式
        debug_mode_layout = QHBoxLayout()
        debug_mode_label = QLabel("调试模式：")
        debug_mode_label.setMinimumWidth(80)
        self.combo_debug_mode = QComboBox()
        self.combo_debug_mode.setObjectName("DebugModeCombo")
        self.combo_debug_mode.addItems(["否", "是"])
        self.combo_debug_mode.currentIndexChanged.connect(self._on_debug_mode_changed)
        debug_mode_layout.addWidget(debug_mode_label)
        debug_mode_layout.addWidget(self.combo_debug_mode)
        debug_mode_layout.addStretch()
        basic_layout.addLayout(debug_mode_layout)

        # 添加弹性空间
        basic_layout.addStretch()

    def _setup_advanced_settings(self):
        """
        在高级设置标签页中添加控件
        包括：检测间隔、重置时间、帧长度
        """
        # 创建高级设置页面的布局
        advanced_layout = QVBoxLayout(self.tab2)
        advanced_layout.setContentsMargins(20, 20, 20, 20)
        advanced_layout.setSpacing(20)

        # 第一行：检测间隔设置
        interval_layout = QHBoxLayout()
        interval_label = QLabel("检测间隔：")
        interval_label.setMinimumWidth(80)
        self.combo_interval = QComboBox()
        self.combo_interval.setObjectName("IntervalCombo")
        self.combo_interval.addItems(["0.1秒", "0.15秒", "0.2秒", "0.25秒", "0.3秒", "0.35秒", "0.4秒", "0.45秒", "0.5秒"])
        self.combo_interval.setCurrentIndex(1)
        self.combo_interval.currentIndexChanged.connect(self._on_interval_changed)
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.combo_interval)
        interval_layout.addStretch()
        advanced_layout.addLayout(interval_layout)

        # 检测间隔说明
        interval_desc_layout = QHBoxLayout()
        interval_desc_label = QLabel("每次检测屏幕的时间间隔，越小检测越快，但占用资源越多")
        interval_desc_label.setStyleSheet("color: #666; font-size: 11px;")
        interval_desc_layout.addSpacing(80)
        interval_desc_layout.addWidget(interval_desc_label)
        advanced_layout.addLayout(interval_desc_layout)

        # 第二行：重置时间设置
        reset_time_layout = QHBoxLayout()
        reset_time_label = QLabel("重置时间：")
        reset_time_label.setMinimumWidth(80)
        self.combo_reset_time = QComboBox()
        self.combo_reset_time.setObjectName("ResetTimeCombo")
        self.combo_reset_time.addItems(["1.0秒", "1.5秒", "2.0秒", "2.5秒", "3.0秒", "3.5秒", "4.0秒", "4.5秒", "5.0秒"])
        self.combo_reset_time.currentIndexChanged.connect(self._on_reset_time_changed)
        reset_time_layout.addWidget(reset_time_label)
        reset_time_layout.addWidget(self.combo_reset_time)
        reset_time_layout.addStretch()
        advanced_layout.addLayout(reset_time_layout)

        # 重置时间说明
        reset_time_desc_layout = QHBoxLayout()
        reset_time_desc_label = QLabel("多久没有检测到地主底牌，就自动重置计牌器")
        reset_time_desc_label.setStyleSheet("color: #666; font-size: 11px;")
        reset_time_desc_layout.addSpacing(80)
        reset_time_desc_layout.addWidget(reset_time_desc_label)
        advanced_layout.addLayout(reset_time_desc_layout)

        # 第三行：帧长度设置
        frame_length_layout = QHBoxLayout()
        frame_length_label = QLabel("帧长度：")
        frame_length_label.setMinimumWidth(80)
        self.combo_frame_length = QComboBox()
        self.combo_frame_length.setObjectName("FrameLengthCombo")
        self.combo_frame_length.addItems(["1", "2", "3", "4", "5", "6"])
        self.combo_frame_length.currentIndexChanged.connect(self._on_frame_length_changed)
        frame_length_layout.addWidget(frame_length_label)
        frame_length_layout.addWidget(self.combo_frame_length)
        frame_length_layout.addStretch()
        advanced_layout.addLayout(frame_length_layout)

        # 帧长度说明
        frame_length_desc_layout = QHBoxLayout()
        frame_length_desc_label = QLabel("连续多少帧检测相同内容才确认，避免误检")
        frame_length_desc_label.setStyleSheet("color: #666; font-size: 11px;")
        frame_length_desc_layout.addSpacing(80)
        frame_length_desc_layout.addWidget(frame_length_desc_label)
        advanced_layout.addLayout(frame_length_desc_layout)

        # 添加弹性空间
        advanced_layout.addStretch()

    def _on_reset_clicked(self):
        """
        重置按钮点击事件
        """
        if self.on_reset_callback:
            self.on_reset_callback()

    def _on_interval_changed(self, index):
        """
        检测间隔改变事件

        参数:
            index: 选择的索引
        """
        if self.on_interval_change_callback:
            self.on_interval_change_callback(index)

    def _on_layout_changed(self, index):
        """
        布局配置改变事件

        参数:
            index: 选择的索引
        """
        if self.on_layout_change_callback:
            self.on_layout_change_callback(index)

    def _on_device_changed(self, index):
        """
        设备选择改变事件

        参数:
            index: 选择的索引
        """
        if self.on_device_change_callback:
            self.on_device_change_callback(index)

    def _on_reset_time_changed(self, index):
        """
        重置时间改变事件

        参数:
            index: 选择的索引
        """
        if self.on_reset_time_change_callback:
            self.on_reset_time_change_callback(index)

    def _on_frame_length_changed(self, index):
        """
        帧长度改变事件

        参数:
            index: 选择的索引
        """
        if self.on_frame_length_change_callback:
            self.on_frame_length_change_callback(index)

    def _on_always_on_top_changed(self, index):
        """
        是否显示在最上层改变事件

        参数:
            index: 选择的索引
        """
        if self.on_always_on_top_change_callback:
            self.on_always_on_top_change_callback(index)

    def _on_show_played_cards_changed(self, index):
        """
        是否显示玩家所出的牌改变事件

        参数:
            index: 选择的索引
        """
        if self.on_show_played_cards_change_callback:
            self.on_show_played_cards_change_callback(index)

    def _on_debug_mode_changed(self, index):
        """
        调试模式改变事件

        参数:
            index: 选择的索引
        """
        if self.on_debug_mode_change_callback:
            self.on_debug_mode_change_callback(index)

    def set_current_interval(self, interval_text):
        """
        设置当前检测间隔

        参数:
            interval_text: 检测间隔文本（如 "0.2秒"）
        """
        index = self.combo_interval.findText(interval_text)
        if index >= 0:
            self.combo_interval.blockSignals(True)
            self.combo_interval.setCurrentIndex(index)
            self.combo_interval.blockSignals(False)

    def set_current_layout(self, layout_name):
        """
        设置当前布局配置

        参数:
            layout_name: 布局配置名称
        """
        index = self.combo_layout.findText(layout_name)
        if index >= 0:
            self.combo_layout.blockSignals(True)
            self.combo_layout.setCurrentIndex(index)
            self.combo_layout.blockSignals(False)

    def set_current_device(self, device_choice):
        """
        设置当前设备选择

        参数:
            device_choice: 设备选择（"cpu" 或 "cuda"）
        """
        device_map = {"cpu": "CPU", "cuda": "GPU"}
        device_text = device_map.get(device_choice, "CPU")
        index = self.combo_device.findText(device_text)
        if index >= 0:
            self.combo_device.blockSignals(True)
            self.combo_device.setCurrentIndex(index)
            self.combo_device.blockSignals(False)

    def set_current_reset_time(self, reset_time):
        """
        设置当前重置时间

        参数:
            reset_time: 重置时间（秒）
        """
        reset_time_text = f"{reset_time}秒"
        index = self.combo_reset_time.findText(reset_time_text)
        if index >= 0:
            self.combo_reset_time.blockSignals(True)
            self.combo_reset_time.setCurrentIndex(index)
            self.combo_reset_time.blockSignals(False)

    def set_current_frame_length(self, frame_length):
        """
        设置当前帧长度

        参数:
            frame_length: 帧长度
        """
        frame_length_text = str(frame_length)
        index = self.combo_frame_length.findText(frame_length_text)
        if index >= 0:
            self.combo_frame_length.blockSignals(True)
            self.combo_frame_length.setCurrentIndex(index)
            self.combo_frame_length.blockSignals(False)

    def set_current_always_on_top(self, always_on_top):
        """
        设置当前是否显示在最上层

        参数:
            always_on_top: 是否显示在最上层（True/False）
        """
        always_on_top_text = "是" if always_on_top else "否"
        index = self.combo_always_on_top.findText(always_on_top_text)
        if index >= 0:
            self.combo_always_on_top.blockSignals(True)
            self.combo_always_on_top.setCurrentIndex(index)
            self.combo_always_on_top.blockSignals(False)

    def set_current_show_played_cards(self, show_played_cards):
        """
        设置当前是否显示玩家所出的牌

        参数:
            show_played_cards: 是否显示玩家所出的牌（True/False）
        """
        show_played_cards_text = "是" if show_played_cards else "否"
        index = self.combo_show_played_cards.findText(show_played_cards_text)
        if index >= 0:
            self.combo_show_played_cards.blockSignals(True)
            self.combo_show_played_cards.setCurrentIndex(index)
            self.combo_show_played_cards.blockSignals(False)

    def set_current_debug_mode(self, debug_mode):
        """
        设置当前调试模式

        参数:
            debug_mode: 是否开启调试模式（True/False）
        """
        debug_mode_text = "是" if debug_mode else "否"
        index = self.combo_debug_mode.findText(debug_mode_text)
        if index >= 0:
            self.combo_debug_mode.blockSignals(True)
            self.combo_debug_mode.setCurrentIndex(index)
            self.combo_debug_mode.blockSignals(False)

    def _setup_about_settings(self):
        """
        在关于标签页中添加控件
        """
        # 创建关于页面的布局
        about_layout = QVBoxLayout(self.tab3)
        about_layout.setContentsMargins(20, 20, 20, 20)
        about_layout.setSpacing(15)

        # 添加标题
        title_label = QLabel("关于 Han 记牌器")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        about_layout.addWidget(title_label)

        # 添加描述文字
        description_label = QLabel()
        description_label.setText("Han 记牌器是一款扑克牌斗地主的棋牌软件。基于 YOLO V11识别。通常不需要繁琐的配置。仅通过识别点数进行统计，不是作弊，也不是外挂，仅提供正常的娱乐使用。")
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 12px;")
        about_layout.addWidget(description_label)

        # 添加弹性空间
        about_layout.addStretch()
