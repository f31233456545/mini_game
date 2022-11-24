import json
import random

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
        

    def round_end(self):
        for seat in self.user_info:
            self.pod_info.pod_chip_cnt += seat.chip_cnt
            seat.chip_cnt = 0
        self.pod_info.term += 1
        if self.pod_info.term == 4:
            self.pod_info.term = 0

    def create_room(self, private, room_name, game_kind, creator_name):
        self.room_name = room_name

    class pod_infoClass(object):
        def __init__(self) -> None:
            self.playing = False
            self.curr_id = 0
            self.bookmarker_id = 0
            self.term = 0
            self.pod_chip_cnt = 0
            self.pokes = [0, 0, 0]
            self.small_blind = 0
            self.big_blind = 1

    class last_actionClass(object):
        def __init__(self) -> None:
            self.user_id = 0
            self.action_type = 0
            self.raise_num = 0
            
    def sit(self, room_id, user_name, chip_cnt):
        i = 0
        while i < 8:
            seat = self.user_info[i]
            if seat.user_name == '':
                seat.user_name = user_name
                seat.chip_cnt = chip_cnt
                return seat.seat_id
            i += 1

    def start_game(self, room_id):
        self.pod_info.playing = True
        # pass
        # pod_info.playing=True

    def stand(self, room_id, user_name):
        for seat in self.user_info:
            if seat.user_name == user_name:
                seat.user_name = ''
                # 用户名为‘’表示该座位无人
                # 恢复初始化状态
                seat.stack_cnt = 0
                seat.chip_cnt = 0
                seat.folded = True
                seat.last_action = 0
                seat.hand_poke0 = 0
                seat.hand_poke1 = 0
                return True
        return False

    def action(self, user_name, action_type, raise_num):
        self.pod_info.curr_id = user_name
        self.last_info.user_id = user_name
        self.last_info.action_type = action_type
        self.last_info.raise_num = raise_num
        # pass
        # pod_info.curr_id=user_name
        # last_action.user_id=user_name
        # last_action.action_type=action_type
        # last_action.raise_num=raise_num

    def get_user_seat_id(self, user_name):
        i = 0
        while i < 8:
            if self.user_info[i].user_name == user_name:
                return i + 1
            i += 1
        return 1
    
    def get_player_info(self):
        resp = []
        for u in self.user_info:
            # resp.append(json.dumps(u))
            # u_json={}
            # u_json["user_name"]=u["user_name"]
            # u_json["seat_id"]=u["seat_id"]
            # u_json["stack_cnt"]=u["stack_cnt"]
            # u_json["chip_cnt"]=u["chip_cnt"]
            # u_json["folded"]=u["folded"]
            # u_json["last_action"]=u["last_action"]
            # u_json["stack_cnt"]=u["stack_cnt"]
            # hand_pokes=[]
            # hand_pokes[0]=u["hand_poke0"]
            # hand_pokes[1]=u["hand_poke1"]
            # u_json["hand_pokes"]=hand_pokes
            resp.append(u.to_dict())
        return resp

desks = dict()