import os
import traceback
from core.card_detector import CardDetector
from config.settings import WAIT_BEGIN, HAS_STARTED, STARTED_RECORD_CARD, TOTAL_CARDS
from PySide6.QtCore import QObject, Signal, Slot
from config.settings import DEBUG_MODE
import time
import config.settings as settings


class CardTracker:
    def __init__(self, layout_name = None):
        # 如果没有提供布局名称，CardDetector 会自动使用第一个可用配置
        self.layout_name = layout_name
        self.card_detector = CardDetector(layout_name=layout_name)
        self.state = WAIT_BEGIN
        self.player_hand = []
        self.player_played = []
        self.opponent_left = []
        self.opponent_right = []
        self.landlord_cards = []
        self.show_left_cards = []
        self.show_right_cards = []
        self.show_self_cards = []
        self.remain_cards = TOTAL_CARDS.copy()
        self.no_target_time = time.time()

    def reset(self): # 重置记牌器
        self.state = WAIT_BEGIN
        self.player_hand = []
        self.player_played = []
        self.opponent_left = []
        self.opponent_right = []
        self.landlord_cards = []
        self.show_left_cards = []
        self.show_right_cards = []
        self.show_self_cards = []
        self.remain_cards = TOTAL_CARDS.copy()

    def __presses_one_frame(self):
        player_hand, player_played, opponent_left, opponent_right, landlord_cards = self.card_detector.detect()
        tot_len = len(landlord_cards)
        if tot_len == 0:
            return

        self.no_target_time = time.time()

        if DEBUG_MODE:
            print("------------------------------------------")
            print("player_hand: ", player_hand)
            print("opponent_left: ", opponent_left)
            print("opponent_right: ", opponent_right)
            print("landlord_cards: ", landlord_cards)



        if len(self.player_hand) >= settings.FRAME_LENGTH:
            self.player_hand = self.player_hand[1:]
            self.player_played = self.player_played[1:]
            self.opponent_left = self.opponent_left[1:]
            self.opponent_right = self.opponent_right[1:]
            self.landlord_cards = self.landlord_cards[1:]

        self.player_hand.append(player_hand)
        self.player_played.append(player_played)
        self.opponent_left.append(opponent_left)
        self.opponent_right.append(opponent_right)
        self.landlord_cards.append(landlord_cards)

    def __check_card(self, lst): # 检测连续的帧内容是否一样

        if len(lst) < settings.FRAME_LENGTH or len(lst[-1]) == 0:
            return False

        for i in range(1, len(lst)):
            if lst[i-1] != lst[i]:
                return False
        return True

    def _delete_played_cards(self, lst):
        for s in lst:
            self.remain_cards[s] -= 1

    def run_game (self):
        self.__presses_one_frame()

        if self.state == WAIT_BEGIN:
            if self.__check_card(self.landlord_cards):  # 检测到地主的补牌, 开始游戏
                self.state = HAS_STARTED


        if self.state == HAS_STARTED:
            if self.__check_card(self.player_hand): # 检测完自己的手牌, 开始记牌
                self._delete_played_cards(self.player_hand[-1])
                self.state = STARTED_RECORD_CARD



        if self.state == STARTED_RECORD_CARD:
            if self.__check_card(self.opponent_left) and (len(self.show_left_cards) == 0 or (self.opponent_left[-1] != self.show_left_cards[-1])) :
                if len(self.opponent_left[-1]) > 0:
                    self.show_left_cards.append(self.opponent_left[-1])
                self._delete_played_cards(self.opponent_left[-1])


            if self.__check_card(self.opponent_right) and (len(self.show_right_cards) == 0 or (self.opponent_right[-1] != self.show_right_cards[-1])):
                if len(self.opponent_right[-1]) > 0:
                    self.show_right_cards.append(self.opponent_right[-1])
                self._delete_played_cards(self.opponent_right[-1])


            if self.__check_card(self.player_played) and (len(self.show_self_cards) == 0 or (self.player_played[-1] != self.show_self_cards[-1])):
                if len(self.player_played[-1]) > 0:
                    self.show_self_cards.append(self.player_played[-1])




    def run(self):
        self.run_game()
        tme = time.time()
        if tme - self.no_target_time > settings.RESET_TIME:
            self.reset()
            self.no_target_time = tme
        return self.remain_cards, self.show_left_cards, self.show_right_cards, self.show_self_cards



class CardTrackerWorker(QObject):
    """
    Worker 是一个 QObject，放到 QThread 里运行。
    它暴露一个槽函数 do_run_once()，用于执行 tracker.run()。

    执行成功/失败都通过信号发回主线程。
    """

    # 成功信号：把 tracker.run() 的 4 个返回值发回去
    result_ready = Signal(dict, list, list, list)

    # 失败信号：把错误文本发回去
    error = Signal(str)

    # “本次任务结束”信号：用于主线程解除“忙碌状态”
    finished = Signal()

    def __init__(self, card_tracker: CardTracker):
        super().__init__()
        self.card_tracker = card_tracker
        self.debug_pic_id_tmp = 0

    @Slot()
    def reset(self):
        self.card_tracker.reset()

    @Slot()
    def do_run_once(self):
        """
        在后台线程执行一次 tracker.run()。
        注意：这里不要直接操作 UI，只发信号。
        """
        try:
            remain_cards, show_left, show_right, show_self = self.card_tracker.run()
            self.result_ready.emit(remain_cards, show_left, show_right, show_self)
        except Exception:
            err_text = traceback.format_exc()
            self.error.emit(err_text)
        finally:
            self.finished.emit()


if __name__ == '__main__':
    tracker = CardTracker()
    debug_pic_id = 0
    print("start")
    while True:
        remain_cards, show_left, show_right, show_self = tracker.run()
        tracker.img_tem.show()
        a = input("shuru: ")
        if tracker.flag_tem == 1:
            print("-----------------------------")
            os.makedirs("debugimg", exist_ok=True)  # 确保目录存在
            tracker.img_tem.save("debugimg/pic" + str(debug_pic_id) + ".png")
            debug_pic_id = debug_pic_id + 1
            print(debug_pic_id)
            print(remain_cards)
            print(show_left)
            print(show_right)
            print(show_self)
            print(tracker.landlord_cards[-1])
            print()
        time.sleep(0.2)
