import random
import copy
import time
import math
import threading

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
        self.side_pot = 0 # if he wins, how many will he win? 0 means all

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
        self.lock=threading.Lock()

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
        if self.pod_info.term == 0:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], 0, 0]
        elif self.pod_info.term == 1:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], 0]
        elif self.pod_info.term == 2:
            self.pod_info.pokes = [self.pod_info.inplay[0], self.pod_info.inplay[1], self.pod_info.inplay[2], self.pod_info.inplay[3], self.pod_info.inplay[4]]        
        
        for seat in self.user_info:
            self.pod_info.pod_chip_cnt += seat.chip_cnt

        for seat in self.user_info:
            if seat.stack_cnt == 0: # allin
                seat.side_pot = self.pod_info.pod_chip_cnt
                for u in self.user_info:
                    if u.chip_cnt > seat.chip_cnt:
                        seat.side_pot -= (u.chip_cnt - seat.chip_cnt)

        for seat in self.user_info:        
            seat.chip_cnt = 0
            seat.flag = False

        self.pod_info.term += 1
        if self.pod_info.term >= 4:
            self.pod_info.term = 0
            # check if only one player remain
            remain_num = 0
            remain_player = self.user_info[0]
            for u in self.user_info:
                if u.folded == False:
                    remain_num+=1
                    remain_player = u
            
            if remain_num == 1:
                remain_player.stack_cnt += self.pod_info.pod_chip_cnt
                self.pod_info.pod_chip_cnt = 0
                self.action(remain_player.seat_id, 4, 0)
            else:
                self.determine_winner()
                self.assign_chips()
                winner_id = 0
                for u in self.user_info:
                    if u.rank == 1:
                        winner_id = u.seat_id
                        break
                self.action(winner_id, 4, 0)
            self.lock.release()
            self.prepare_new_game()

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
            self.action_type = -1
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
        self.lock.release()
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
                seat.hand_pokes = [0, 0]
                if self.pod_info.playing == False:
                    return True
                # Judge if the game state will change because of this
                cur_index = self.pod_info.curr_id-1
                if seat.user_name == self.user_info[cur_index].user_name:
                    pnum = 0
                    for u in self.user_info:
                        if u.folded == False:
                            pnum += 1
                    if pnum == 1:
                        # win
                        self.pod_info.term = 3
                        self.round_end()
                    else:
                        chip = -1
                        term_flag = True
                        for u in self.user_info:
                            if u.flag == False and u.folded == False:
                                term_flag = False
                                break
                            if u.folded == False:
                                if chip == -1:
                                    chip = u.chip_cnt
                                if chip != u.chip_cnt:
                                    term_flag = False
                                break
                        if term_flag == True:
                            # A new term
                            self.action(-1, 3, 0)
                            self.round_end()
                        # Move onto the next player 
                        cur_index = (cur_index+1)%8
                        while self.user_info[cur_index].folded == True:
                            cur_index = (cur_index+1)%8
                        self.pod_info.curr_id=cur_index+1
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
        return 0
    
    def get_player_info(self,username):
        resp = []
        for u in self.user_info:
            if u.folded == True:
                hand = copy.deepcopy(u.hand_pokes)
                u.hand_pokes=[]
                resp.append(u.to_dict())
                u.hand_pokes=copy.deepcopy(hand)
            elif self.last_info.action_type == 4: #game ends, show hands
                resp.append(u.to_dict())
            elif username != u.user_name:
                hand = copy.deepcopy(u.hand_pokes)
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
    
    def assign_chips(self):
        r = 1
        while r < MAX_PLAYER_NUM: 
            winner = []
            for u in self.user_info:
                if u.rank == r:
                    winner.append(u)
            # give chips.
            num = len(winner)
            no_allin_winner = []
            # firstly gives all allin-players money
            for w in winner:
                if w.side_pot > 0:
                    w.stack_cnt += math.floor(w.side_pot/num)
                    self.pod_info.pod_chip_cnt -= math.floor(w.side_pot/num)
                else:
                    no_allin_winner.append(w)

            # then split money
            pot = self.pod_info.pod_chip_cnt
            num_no_allin = len(no_allin_winner)
            for w in no_allin_winner:
                w.stack_cnt += math.floor(pot/num_no_allin)
                self.pod_info.pod_chip_cnt -= math.floor(pot/num_no_allin)
               

            # gives the rest money to someone
            if self.pod_info.pod_chip_cnt > 0 :
                winner_index = self.pod_info.small_blind
                while self.user_info[winner_index].folded == True:
                    winner_index=self.get_next_player_index(winner_index)
                self.user_info[winner_index].stack_cnt += self.pod_info.pod_chip_cnt
                self.pod_info.pod_chip_cnt=0
            if num_no_allin > 0:
                break
            if self.pod_info.pod_chip_cnt == 0 :
                break
            r += 1

    # show hands, distribute chips, then call this func.
    def prepare_new_game(self):
        self.lock.acquire()
        time.sleep(5)
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
                self.user_info[i].hand_pokes = [0,0]
                self.user_info[i].last_action = -1
            else:
                self.user_info[i].folded = False
                self.user_info[i].flag = False
                self.user_info[i].last_action = -1
                self.user_info[i].side_pot = 0
            i += 1
        print("players reset")    
        # check if the game ends
        if self.get_player_num() < 2:
            print("too less players. game ends")
            self.end_game()
            return
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
        self.lock.release()

    def score(self, seat_id):

        hand = copy.deepcopy(self.user_info[seat_id - 1].hand_pokes)
        pokes = copy.deepcopy(self.pod_info.pokes)
        hand += pokes
        score = 0
        kicker = []

        #pairs:  {cardValue:cardNum}   cardValue in range(2,14) stand for 2->ace
        #nop  :  {cardNum of one pair:num of according pair} 
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

        #----------Has 4 of a kind------------- 
        if 4 in nop:
            score = 7
            pokes = list(pairs.keys())
            kicker = [key for key in pokes if pairs[key] == 4] 
            key = kicker[0]
            pokes.remove(key)
            kicker.append(max(pokes))
            return [score, kicker]
        #----------Has At least 3 of A Kind----------
        elif 3 in nop:      
            if nop[3] == 2 or 2 in nop:     #Has two 3 of a kind, or a pair and 3 of a kind (fullhouse)
                score = 6
                
                #gets a list of all the pairs
                pokes = list(pairs.keys())
                
                #ensures the first kicker is the value of the highest 3 of a king
                kicker = [key for key in pokes if pairs[key] == 3]
                if( len(kicker) > 1):   # if there are two 3 of a kinds, take the higher as the first kicker
                    key = max(kicker)
                    kicker = [key]

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
        #----------Has at Least a Pair-----------
        elif 2 in nop: 
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
                score = 1   #Has only one Pair
                
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
        
        #------------------------------------------------
        #------------Checking for Straight---------------
        #------------------------------------------------    
        
        counter = 1
        high = 0
        straight = False
        pokes = list(pairs.keys())
        pokes.sort()
        
        
        #Loops through pokes checking for the straight by comparing the current card to the
        #the previous one and tabulates the number of cards found in a row
        #Notice:card in range(2,15) stand for 2->ace
        prev = 0
        for card in pokes:
            if card == (prev + 1):
                counter += 1
                if counter >= 5: #A straight has been recognized
                    straight = True
                    high = card
            else:
                counter = 1
            prev = card

        if straight and score < 4:
            score = 4
            kicker = [high]

        #------------------------------------------------
        #-------------Checking for Flush-----------------
        #------------------------------------------------
        flush = False
        total = {}
        
        #Loops through the hand calculating the number of cards of each symbol.
        #card 1-52 stand for club->diamond->heart->spade  ace->king
        for card in hand:
            key = (card-1) //13
            if key in total:
                total[key] += 1
            else:
                total[key] = 1
        
        #key represents the suit of a flush if it is within the hand
        key = -1
        for k, v in total.items():
            if v >= 5:
                key = k
        
        #If a flush has been realized and the hand has a lower score than a flush
        if key != -1 and score < 5:
            flush = True
            score = 5
            kicker = [card for card in hand if (card-1)//13 == key]
            kicker.sort()

        #------------------------------------------------
        #-----Checking for Straight & Royal Flush--------
        #------------------------------------------------
        if flush and straight:            
            #Notice:card of kicker is in range(1,53)
            #convert it to range(2,14) for convience
            temp = []
            for card in kicker:
                key =card
                key %= 13
                if key <=1 :
                    key +=13
                temp.append(key)
            temp.sort()
            #Loops through temp checking for the straight by comparing the current card to the
            #the previous one and tabulates the number of cards found in a row
            prev = 0
            counter = 0
            high = 0
            straight_flush = False

            for card in temp:
                if card == prev + 1:
                    counter += 1
                    if counter >= 5: #A straight has been recognized
                        straight_flush = True
                        high = card
                else:
                    counter = 1
                prev = card
            #If a straight has been realized and the hand has a lower score than a straight
            if straight_flush:
                if high == 14:
                    score = 9
                else:
                    score = 8
                kicker = [high]
                return [score, kicker]

        #if there is only a flush then determines the kickers
        if flush: 
            #Notice:card of kicker is in range(1,53)
            #convert it to range(2,14) for convience
            temp = []
            for card in kicker:
                key =card
                key %= 13
                if key <=1 :
                    key += 13
                temp.append(key)
            temp.sort(reverse=True)
            #This ensures only the top 5 kickers are selected and not more.
            over = len(temp) - 5
            for i in range (0,over):
                temp.pop()
            kicker = temp
            return [score,kicker]
        
        #------------------------------------------------
        #-------------------High Card--------------------
        #------------------------------------------------

        #If the score is 0 then high card is the best possible hand
        if score == 0:      
            #It will keep track of only the card's value
            kicker = list(pairs.keys())
            kicker.sort(reverse=True)
            #Since the hand is sorted it will pop the two lowest cards position 0, 1 of the list
            kicker.pop()
            kicker.pop()   
        #Return the score, and the kicker to be used in the event of a tie
        return [score, kicker]


    def determine_winner(self):
        #seats contains all playing players
        seats = [seat for seat in self.user_info if seat.folded == False]
        scores = []

        for seat in seats:
            score_kicker = self.score(seat.seat_id)
            scores.append( [ seat.seat_id, score_kicker] )
        scores = sorted(scores, key = lambda s:s[1], reverse=True)
        print(scores)
        rank = 1
        length = len(seats)
        
        #Set rank for all players
        for i in range(0,length):
            self.user_info[scores[i][0] - 1].rank = rank;
            if i < length-1 and scores[i][1] != scores[i + 1][1]:
                rank += 1


desks = dict()
