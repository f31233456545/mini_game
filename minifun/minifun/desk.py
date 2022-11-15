import numpy as np
class desk(object):
    def __init__(self) -> None:
        #定义并初始化pod_info信息
        class pod_infoClass:
            playing=False
            your_id=0
            curr_id=0
            bookmarker_id=0
            trem=0
            pod_chip_cnt=0
            pokes=[0,0,0]
        
        class last_actionClass:
            user_id=0
            action_type=0
            raise_num=0
        
        self.pod_info=pod_infoClass()
        self.last_action=last_actionClass()
        
        user_infoType=np.dtype(
            {
                'names':['user_name','seat_id','stack_cnt','chip_cnt','folded','last_action','hand_poke0','hand_poke1'],
                'formats':['a','i','i','i','b','i','i','i']
                #names表示所需变量名，formats表示变量名对应的数据类型
            }
        )
        #建立一个有八个元素的初始化为0的数组保存user_info
        self.user_info=np.array([('zero',0.,0.,0.,0.,0.,0.,0.)]*10,dtype=user_infoType)
        user_info=self.user_info
        #对于user_info初始化
        i=1
        while i<9 :
            
            #用户名为‘’表示该座位无人
            user_info[i]['user_name']=''
            user_info[i]['seat_id']=i
            user_info[i]['stack_cnt']=0
            user_info[i]['chip_cnt']=0
            user_info[i]['folded']=True
            #0表示弃牌
            user_info[i]['last_action']=0
            #手牌初始化为背面
            user_info[i]['hand_poke0']=0
            user_info[i]['hand_poke1']=0
            i += 1
    
    def create_room(self,private,room_name,game_kind,creator_name):
            self.room_name=room_name
        
    def sit(self,room_id,user_name,chip_cnt):
        i=1
        while i<9:
            seat = self.user_info[i]
            if seat['user_name'] == '':
                seat['user_name'] = user_name
                seat['chip_cnt']=chip_cnt
                break
            i += 1
        return i
    
    def start_game(self,room_id):
        self.pod_info.playing=True
    
    def stand(self,room_id,user_name):
        for seat in self.user_info:
            if seat['user_name'] == user_name:
                seat['user_name'] = ''
                #用户名为‘’表示该座位无人
                #恢复初始化状态
                seat['stack_cnt']=0
                seat['chip_cnt']=0
                seat['folded']=True
                seat['last_action']=0
                seat['hand_poke0']=0
                seat['hand_poke1']=0
                return True
        return False
    
    def action(self,user_name,action_type,raise_num):
        self.pod_info.curr_id=user_name
        self.last_action.user_id=user_name
        self.last_action.action_type=action_type
        self.last_action.raise_num=raise_num
        
    
    def request_game_info(self,room_id,user_name):
        self.pod_info.your_id=user_name