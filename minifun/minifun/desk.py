import random
import copy

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
        self.flag = False
        self.rank = 0

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
        self.pod_info.inplay.clear()
        self.pod_info.pokes = [0, 0, 0, 0, 0]
        poke0 = -1         #初始化并标记poke0与poke1
        poke1 = -1
        self.pod_info.inplay = random.sample(range(1,52),5) #五张公牌
        for seat in self.user_info:
            if seat.user_name != '':         #该座位有人
                while poke0 in self.pod_info.inplay or poke0 == -1:
                    poke0 = random.randint(1,52)
                self.pod_info.inplay.append(poke0)
                while poke1 in self.pod_info.inplay or poke1 == -1:
                    poke1 = random.randint(1,52)
                self.pod_info.inplay.append(poke1)
                seat.hand_pokes = [poke0,poke1]
        return
        

    def round_end(self):
        # dealer first
        self.pod_info.curr_id = self.pod_info.dealer + 1
        # deals flop, turn and river
        if self.pod_info.term == 1:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], 0, 0]
        elif self.pod_info.term == 2:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], 0]
        elif self.pod_info.term == 3:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], self.pod_info.inplay[4]]
        
        for seat in self.user_info:
            self.pod_info.pod_chip_cnt += seat.chip_cnt
            seat.chip_cnt = 0
            seat.flag = False
        self.pod_info.term += 1
        if self.pod_info.term == 4:
            # self.compare()
            self.assign_chips()
            self.prepare_new_game()
            self.pod_info.term = 0

    def create_room(self, private, room_name, game_kind, creator_name):
        self.room_name = room_name

    class pod_infoClass(object):
        def __init__(self) -> None:
            self.playing = False
            # id is 1~8
            self.curr_id = 0
            self.bookmarker_id = 0 # is dealer + 1
            self.term = 0
            self.pod_chip_cnt = 0
            self.pokes = [0, 0, 0, 0, 0]
            self.inplay = []
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

    def action(self, user_id, action_type, raise_num):
        # self.pod_info.curr_id = user_id 
        self.last_info.user_id = user_id
        self.last_info.action_type = action_type
        self.last_info.raise_num = raise_num
        # pass
        # pod_info.curr_id=user_name
        # self.last_action.user_id=user_name
        # self.last_action.action_type=action_type
        # self.last_action.raise_num=raise_num

    def get_user_seat_id(self, user_name):
        i = 0
        while i < MAX_PLAYER_NUM:
            if self.user_info[i].user_name == user_name:
                return i + 1
            i += 1
        return 1
    
    def get_player_info(self,username):
        resp = []
        for u in self.user_info:
            if username != u.user_name:
                hand = copy.deepcopy(u.hand_pokes)
                # u.hand_pokes=[0,0]  #stupid code....
                u.hand_pokes=[0,0]
                resp.append(u.to_dict())
                u.hand_pokes=copy.deepcopy(hand)
            else:
                resp.append(u.to_dict())
        return resp
    
    # passively called when player less than 2.
    def end_game(self):
        self.pod_info.playing=False
    
    def get_prev_player_index(self,index):
        ret = (index-1+MAX_PLAYER_NUM)%MAX_PLAYER_NUM
        while self.user_info[ret].user_name=='':
            ret = (ret-1+MAX_PLAYER_NUM)%MAX_PLAYER_NUM
        return ret
    
    def get_next_player_index(self,index):
        ret = (index+1)%MAX_PLAYER_NUM
        while self.user_info[ret].user_name=='':
            ret = (ret+1)%MAX_PLAYER_NUM
        return ret
    
    # a demo function. an arbitary player gets the pot.
    def assign_chips(self):
        winner_index = self.pod_info.dealer
        while self.user_info[winner_index].folded == True:
            winner_index=self.get_next_player_index(winner_index)
        self.user_info[winner_index].stack_cnt += self.pod_info.pod_chip_cnt
        self.pod_info.pod_chip_cnt=0

    # show hands, distribute chips, then call this func.
    def prepare_new_game(self):
        # clear all stack_cnt<=1 players, reset other players folded = false
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
            else:
                self.user_info[i].folded = False
            i += 1
        print("players reset")    
        # check if the game ends
        if self.get_player_num() < 2:
            print("too less players. game ends")
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
        print("blinds determined")
        # assign blinds
        self.user_info[self.pod_info.big_blind].stack_cnt-=2
        self.user_info[self.pod_info.big_blind].chip_cnt+=2
        self.user_info[self.pod_info.small_blind].stack_cnt-=1
        self.user_info[self.pod_info.small_blind].chip_cnt+=1

        # determine first active player
        self.pod_info.curr_id=self.get_next_player_index(self.pod_info.big_blind)+1

        # deal_cards
        self.deal_cards()
        print("cards dealed")
        # alert front-end to synchronize desk info
        self.action(self.pod_info.big_blind, 3, 2)
        # TODO:
        # self.last_info.user_id = winner

        def determine_winner(self):
            rank = 1
            for seat in self.user_info:
                if seat.user_name != '':
                    seat.rank = rank
                    rank += 1
        
desks = dict()
