import os
import yaml

# ==================== 路径配置 ====================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'config.yaml')
YOLO_MODEL_PATH = os.path.join(BASE_DIR, 'yolo', 'weights', 'best.pt')

# 加载配置文件
def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        # 返回默认配置作为 fallback
        return {
            'reset_time': 3.5,
            'detect_interval_sec': 0.2,
            'little_joker_shown': "🃟",
            'big_joker_shown': "🃏",
            'yolo_confidence_threshold': 0.6,
            'yolo_iou_threshold': 0.45,
            'yolo_to_card_mapping': {
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
            },
            'window_layouts': {
                "JJ斗地主": {
                    "window_title": "JJ斗地主",
                    "layout": {
                        'player_hand': (0.04, 0.70, 0.96, 0.85),
                        "player_played": (0.04, 0.50, 0.96, 0.6),
                        'opponent_left': (0.20, 0.32, 0.455, 0.49),
                        'opponent_right': (0.46, 0.32, 0.80, 0.49),
                        'landlord_cards': (0.35, 0.08, 0.45, 0.15),
                    }
                }
            },
            'frame_length': 3,
            'device_choice': 'cuda',
            'debug_mode': True
        }

# 加载配置
config = load_config()

# ==================== 基本配置 ====================
RESET_TIME = config.get('reset_time', 3.5)    # 几秒识别不到扑克牌重置
DETECT_INTERVAL_SEC = config.get('detect_interval_sec', 0.2)  # 检测间隔秒数

# 大小王玩家出牌显示字符
LITTLE_JOKER_SHOWN = config.get('little_joker_shown', "🃟")
BIG_JOKER_SHOWN = config.get('big_joker_shown', "🃏")

# ==================== YOLO模型配置 ====================
YOLO_CONFIDENCE_THRESHOLD = config.get('yolo_confidence_threshold', 0.6)
YOLO_IOU_THRESHOLD = config.get('yolo_iou_threshold', 0.45)

# ==================== YOLO类别映射配置 ====================
YOLO_TO_CARD_MAPPING = config.get('yolo_to_card_mapping', {
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
})

# ==================== 窗口和布局配置 ====================
# 预设的不同软件窗口和布局配置
# 结构: {配置名称: {"window_title": "窗口标题", "layout": {区域配置}}}
WINDOW_LAYOUTS = config.get('window_layouts', {
    "JJ斗地主": {
        "window_title": "JJ斗地主",
        "layout": {
            'player_hand': (0.04, 0.70, 0.96, 0.85),
            "player_played": (0.04, 0.50, 0.96, 0.6),
            'opponent_left': (0.20, 0.32, 0.455, 0.49),
            'opponent_right': (0.46, 0.32, 0.80, 0.49),
            'landlord_cards': (0.35, 0.08, 0.45, 0.15),
        }
    }
})

# 连续多少帧检测相同内容算作正确截取
FRAME_LENGTH = config.get('frame_length', 3)


DEBUG_MODE = config.get('debug_mode', True)

# ==================== 设备选择配置 ====================
# 设备选择选项: "cpu" (使用CPU), "cuda" (使用GPU)
DEVICE_CHOICE = config.get('device_choice', 'cuda')

# ==================== 窗口显示配置 ====================
# 是否显示在最上层
ALWAYS_ON_TOP = config.get('always_on_top', False)

# 是否显示玩家所出的牌
SHOW_PLAYED_CARDS = config.get('show_played_cards', True)

def save_device_choice(device_choice):
    """
    保存设备选择到config.yaml文件
    device_choice: "cpu" 或 "cuda"
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['device_choice'] = device_choice
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"设备选择已保存到文件: {device_choice}")
        print(f"请重启程序以应用更改")
    except Exception as e:
        print(f"保存设备选择失败: {e}")

def save_reset_time(reset_time):
    """
    保存重置时间到config.yaml文件
    reset_time: 重置时间（秒）
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['reset_time'] = reset_time
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"重置时间已保存到文件: {reset_time}秒")
    except Exception as e:
        print(f"保存重置时间失败: {e}")

def save_frame_length(frame_length):
    """
    保存帧长度到config.yaml文件
    frame_length: 帧长度
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['frame_length'] = frame_length
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"帧长度已保存到文件: {frame_length}")
    except Exception as e:
        print(f"保存帧长度失败: {e}")

def save_detect_interval(detect_interval):
    """
    保存检测间隔到config.yaml文件
    detect_interval: 检测间隔（秒）
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['detect_interval_sec'] = detect_interval
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"检测间隔已保存到文件: {detect_interval}秒")
    except Exception as e:
        print(f"保存检测间隔失败: {e}")

def save_always_on_top(always_on_top):
    """
    保存是否显示在最上层到config.yaml文件
    always_on_top: 是否显示在最上层（True/False）
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['always_on_top'] = always_on_top
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"是否显示在最上层已保存到文件: {always_on_top}")
    except Exception as e:
        print(f"保存是否显示在最上层失败: {e}")

def save_show_played_cards(show_played_cards):
    """
    保存是否显示玩家所出的牌到config.yaml文件
    show_played_cards: 是否显示玩家所出的牌（True/False）
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['show_played_cards'] = show_played_cards
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"是否显示玩家所出的牌已保存到文件: {show_played_cards}")
    except Exception as e:
        print(f"保存是否显示玩家所出的牌失败: {e}")

def save_debug_mode(debug_mode):
    """
    保存调试模式到config.yaml文件
    debug_mode: 是否开启调试模式（True/False）
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        config['debug_mode'] = debug_mode
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        print(f"调试模式已保存到文件: {debug_mode}")
    except Exception as e:
        print(f"保存调试模式失败: {e}")

# ==================== 路径配置 ====================
# 注意：BASE_DIR 和 YOLO_MODEL_PATH 已在文件开头定义


# 几个状态常数, 没必要动
WAIT_BEGIN = 0
HAS_STARTED = 1
STARTED_RECORD_CARD = 2


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



