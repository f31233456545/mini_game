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
        self.ranking = 0

    def to_dict(self):
        dict = {}
        dict["user_name"] = self.user_name
        dict["seat_id"] = self.seat_id
        dict["stack_cnt"] = self.stack_cnt
        dict["chip_cnt"] = self.chip_cnt
        dict["folded"] = self.folded
        dict["last_action"] = self.last_action
        dict["hand_pokes"] = self.hand_pokes
        dict["ranking"] = self.ranking
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
        if self.pod_info.term == 1:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], 0, 0]
        elif self.pod_info.term == 2:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], 0]
        elif self.pod_info.term == 3:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], self.pod_info.inplay[4]]
        
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
            # id is 1~8
            self.curr_id = 0
            self.bookmarker_id = 0
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
        self.pod_info.curr_id = user_id 
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
                u.hand_pokes=[0,0]
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
        print("players cleared")    
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
    
    def score(self, seat_id):

        hand = self.user_info[seat_id].hand_pokes
        hand += self.pod_info.pokes
        score = 0
        kicker = []

        #pairs{card value:card num}
        #nop{card num of pair:num of pair} 
        pairs = {}
        for card in hand:
            card %= 13
            #for convient comparation
            #set 14 as value of A
            #set 13 as value of K
            #...
            if card <= 1:
                card += 13
            if card in pairs:
                pairs[card] += 1
            else:
                pairs[card] = 1

        nop = {}
        for k, v in pairs.items():
            if v in nop:
                nop[v] += 1
            else:
                nop[v] = 1

        #
        if 4 in nop:        #Has 4 of a kind, assigns the score and the value of the 
            score = 7
            pokes = list(pairs.keys())
            kicker = [key for key in pokes if pairs[key] == 4] 
            key = kicker[0]
            pokes.remove(key)
            kicker.append(max(pokes))
            return [score, kicker]

        elif 3 in nop:      #Has At least 3 of A Kind
            if nop[3] == 2 or 2 in nop:     #Has two 3 of a kind, or a pair and 3 of a kind (fullhouse)
                score = 6
                
                #gets a list of all the pairs
                pokes = list(pairs.keys())
                
                #ensures the first kicker is the value of the highest 3 of a king
                kicker = [key for key in pokes if pairs[key] == 3]
                if( len(kicker) > 1):   # if there are two 3 of a kinds, take the higher as the first kicker
                    key = max(kicker)
                    kicker.clear()
                    kicker.append(key)

                #removes the value of the kicker already in the list
                pokes.remove(kicker[0])
                kicker[1] = 0
                #Gets the highest pair or 3 of kind and adds that to the kickers list
                for card in pokes:
                    if pairs[card] >= 2 and card > kicker[2]:
                        kicker[1] = card

            else:
                score = 3
                pokes = list(pairs.keys())       #Gets the value of the 3 of a king
                kicker = [key for key in pokes if pairs[key] == 3]
                
                #Gets a list of all the cards remaining once the three of a kind is removed
                pokes.remove(kicker[0])
                #Get the 2 last cards in the list which are the 2 highest to be used in the 
                #event of a tie
                card = max(pokes)
                kicker.append(card)
                pokes.remove(card)
                card = max(pokes)
                kicker.append(card)
        
        elif 2 in nop:      #Has at Least a Pair
            if nop[2] >= 2:     #Has at least 2  or 3 pairs
                score = 2
                pokes = list(pairs.keys())   
                
                #Gets the card value of all the pairs 
                temp = [key for key in pokes if pairs[key] == 2]
                
                key = max(temp)
                kicker.append(key)
                temp.remove(key)

                key = max(temp)
                kicker.append(key)
                
                #Gets a list of all the cards remaining once the the 2 pairs are removed
                pokes.remove(kicker[0])
                pokes.remove(kicker[1])
                #Gets the max card in the list remained
                card = max(pokes)
                kicker.append(card)

            else:
                score = 1 
                
                pokes = list(pairs.keys())   
                #Gets the value of the pair
                kicker = [key for key in pokes if pairs[key] == 2]
                #Gets a list of all the cards remaining once pair are removed
                pokes.remove(kicker[0])
                #Gets the last 3 cards in the list which are the highest remaining cards
                #which will be used in the event of a tie
                pokes.sort()
                kicker.append(pokes[4])
                kicker.append(pokes[3])
                kicker.append(pokes[2])




desks = dict()
