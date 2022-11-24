import json
import random

MAX_PLAYER_NUM=8

class player(object):
    def __init__(self, seat) -> None:
        self.user_name = ""
        self.seat_id = seat
        self.stack_cnt = -1
        self.chip_cnt = 0
        self.folded = True
        self.last_action = -1
        self.hand_pokes = [0, 0]

    def to_dict(self):
        dict = {}
        dict["user_name"] = self.user_name
        dict["seat_id"] = self.seat_id
        dict["stack_cnt"] = self.stack_cnt
        dict["chip_cnt"] = self.chip_cnt
        dict["folded"] = self.folded
        dict["last_action"] = self.last_action
        dict["hand_pokes"] = self.hand_pokes
        return dict

class desk(object):
    def __init__(self) -> None:
        self.user_info=[]
        i = 1
        while i < 9:
            self.user_info.append(player(i))
            i += 1
        self.pod_info=self.pod_infoClass()
        self.last_info=self.last_actionClass()

    #发牌
    def deal_cards(self):
        inplay = []        #记录已经使用的牌
        poke0 = -1         #初始化并标记poke0与poke1
        poke1 = -1
        self.pod_info.pokes = random.sample(range(1.52),5) #五张公牌
        inplay.extend(self.pod_info.pokes)
        for seat in self.user_info:
            if seat.user_name != '':         #该座位有人
                while poke0 in inplay or poke0 == -1:
                    poke0 = random(range(1,52))
                inplay.extend(poke0)
                while poke1 in inplay or poke1 == -1:
                    poke1 = random(range(1,52))
                inplay.extend(poke1)
                seat.hand_pokes = [poke0,poke1]
        return
        

    def create_room(self, private, room_name, game_kind, creator_name):
        self.room_name = room_name

    class pod_infoClass(object):
        def __init__(self) -> None:
            self.playing = False
            # id is 1~8
            self.curr_id = 0
            self.bookmarker_id = 0
            self.term = 0
            self.pod_chip_cnt = 0
            self.pokes = [0, 0, 0]
            # blind player is not seat_id, is user_list index.
            # index is 0~7
            self.small_blind = 0
            self.big_blind = 1
            self.dealer = 0

    class last_actionClass(object):
        def __init__(self) -> None:
            self.user_id = 0
            self.action_type = 0
            self.raise_num = 0
    
    def get_player_num(self):
        i = 0
        num = 0
        while i < MAX_PLAYER_NUM :
            if self.user_info[i].user_name != '':
                num += 1
            i += 1
        return num
    
    def sit(self, room_id, user_name, stack_cnt):
        i = 0
        while i < MAX_PLAYER_NUM:
            seat = self.user_info[i]
            if seat.user_name == '':
                seat.user_name = user_name
                seat.stack_cnt = stack_cnt
                return seat.seat_id
            i += 1

    # call prepare_new_game(), dealing cards and assign blinds.
    def start_game(self, room_id):
        self.pod_info.playing = True
        self.prepare_new_game()
        # pass
        # pod_info.playing=True

    def stand(self, room_id, user_name):
        for seat in self.user_info:
            if seat.user_name == user_name:
                seat.user_name = ''
                # 用户名为‘’表示该座位无人
                # 恢复初始化状态
                seat.stack_cnt = -1
                # need to add chip_cnt to pot. otherwise player can escape losing chips by standing up
                self.pod_info.pod_chip_cnt += seat.chip_cnt
                seat.chip_cnt = 0
                seat.folded = True
                seat.last_action = 0
                seat.hand_poke0 = 0
                seat.hand_poke1 = 0
                return True
        return False

    def action(self, user_name, action_type, raise_num):
        self.pod_infoClass.curr_id = user_name
        self.last_actionClass.user_id = user_name
        self.last_actionClass.action_type = action_type
        self.last_actionClass.raise_num = raise_num
        # pass
        # pod_info.curr_id=user_name
        # last_action.user_id=user_name
        # last_action.action_type=action_type
        # last_action.raise_num=raise_num

    def get_user_seat_id(self, user_name):
        i = 0
        while i < MAX_PLAYER_NUM:
            if self.user_info[i].user_name == user_name:
                return i + 1
            i += 1
        return 1
    
    def get_player_info(self):
        resp = []
        for u in self.user_info:
            resp.append(u.to_dict())
        return resp
    
    # passively called when player less than 2.
    def end_game(self):
        self.pod_info.playing=False
    
    def get_prev_player_index(self,index):
        ret = (index-1+MAX_PLAYER_NUM)%MAX_PLAYER_NUM
        while self.user_info[ret].user_name=='':
            ret = (index-1+MAX_PLAYER_NUM)%MAX_PLAYER_NUM
        return ret
    
    def get_next_player_index(self,index):
        ret = (index+1)%MAX_PLAYER_NUM
        while self.user_info[ret].user_name=='':
            ret = (index+1)%MAX_PLAYER_NUM
        return ret
    
    # show hands, distribute chips, then call this func.
    def prepare_new_game(self):
        # clear all stack_cnt<=1 players
        i = 0
        while i < MAX_PLAYER_NUM :
            if self.user_info[i].stack_cnt<=1:
                self.user_info[i].user_name = ''
                # 用户名为‘’表示该座位无人
                # 恢复初始化状态
                self.user_info[i].stack_cnt = -1
                self.user_info[i].chip_cnt = 0
                self.user_info[i].folded = True
                self.user_info[i].last_action = 0
                self.user_info[i].hand_poke0 = 0
                self.user_info[i].hand_poke1 = 0
            i += 1
        # check if the game ends
        if self.get_player_num() < 2:
            self.end_game()
        # Switch BB. 
        bb = self.get_next_player_index(self.pod_info.big_blind)
        self.pod_info.big_blind=bb       
        # Determine SB and dealer. SB is prev player of BB, dealer is prev player of SB(when 2 players, it is SB)
        self.pod_info.small_blind = self.get_prev_player_index(self.pod_info.big_blind)
        if self.get_player_num() == 2:
            self.pod_info.dealer = self.pod_info.small_blind
        else:
            self.pod_info.dealer = self.get_prev_player_index(self.pod_info.small_blind)
        
        # assign blinds
        self.user_info[self.pod_info.big_blind].stack_cnt-=2
        self.user_info[self.pod_info.big_blind].chip_cnt+=2
        self.user_info[self.pod_info.small_blind].stack_cnt-=1
        self.user_info[self.pod_info.small_blind].chip_cnt+=1

        # determine first active player
        self.pod_info.curr_id=self.get_next_player_index(self.pod_info.big_blind)+1

        # deal_cards
        self.deal_cards()

        # alert front-end to synchronize desk info
        self.last_info.action_type=4
        self.last_info.raise_num=0
        # TODO:
        # self.last_info.user_id = winner

desks = dict()