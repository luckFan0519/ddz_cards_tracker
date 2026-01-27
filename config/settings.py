import os

DEBUG_MODE = True
RESET_TIME = 2.5    # 几秒识别不到扑克牌重置


# 大小王玩家出牌显示字符
LITTLE_JOKER_SHOWN = "🃟"
BIG_JOKER_SHOWN = "🃏"


# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOLO_MODEL_PATH = os.path.join(BASE_DIR, 'yolo', 'weights', 'best.pt')

# ==================== YOLO模型配置 ====================
YOLO_CONFIDENCE_THRESHOLD = 0.6
YOLO_IOU_THRESHOLD = 0.6

# ==================== YOLO类别映射配置 ====================
YOLO_TO_CARD_MAPPING = {
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10',
    'J': 'J',
    'Q': 'Q',
    'K': 'K',
    'A': 'A',
    'joker': 'jok',
    'JOKER': 'JOK'
}


# ==================== 窗口配置 ====================
DEFAULT_WINDOW_TITLES = [
    "JJ斗地主",
]


# ==================== 区域配置（相对坐标，0-1之间）====================
# 预设的不同软件布局配置
LAYOUT_PRESETS = {  # (x1, y1, x2, y2)
    # JJ斗地主布局全屏布局
    # "JJ斗地主": {
    #     'player_hand': (0.04, 0.70, 0.96, 0.85),       # 玩家手牌：窗口下方
    #     "player_played": (0.04, 0.46, 0.96, 0.57),       # 玩家已出手牌
    #     'opponent_left': (0.20, 0.25, 0.47, 0.45),     # 左侧对手：窗口左侧
    #     'opponent_right': (0.48, 0.25, 0.85, 0.45),    # 右侧对手：窗口右侧
    #     'landlord_cards': (0.37, 0, 0.55, 0.08),    # 地主底牌：窗口上方中间
    # },

    # JJ斗地主布局带控件布局
    "JJ斗地主": {
        'player_hand': (0.04, 0.70, 0.96, 0.85),  # 玩家手牌：窗口下方
        "player_played": (0.04, 0.50, 0.96, 0.6),  # 玩家已出手牌
        'opponent_left': (0.20, 0.32, 0.455, 0.49),  # 左侧对手：窗口左侧
        'opponent_right': (0.46, 0.32, 0.80, 0.49),  # 右侧对手：窗口右侧
        'landlord_cards': (0.35, 0.08, 0.45, 0.15),  # 地主底牌：窗口上方中间
    }
}

# 几个状态常数, 没必要动
WAIT_BEGIN = 0
HAS_STARTED = 1
STARTED_RECORD_CARD = 2

# 连续多少帧检测相同内容算作正确截取
FRAME_LENGTH = 3



# ==================== 卡牌配置 ====================

TOTAL_CARDS = {
    '3' : 4,
    '4' : 4,
    '5' : 4,
    '6' : 4,
    '7' : 4,
    '8' : 4,
    '9' : 4,
    '10' : 4,
    'J' : 4,
    'Q' : 4,
    'K' : 4,
    'A' : 4,
    '2' : 4,
    'jok' : 1,
    'JOK' : 1
}



