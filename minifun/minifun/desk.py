import numpy as np
class desk(object):
    def __init__(self) -> None:
        pass
    
    #定义并初始化pod_info信息
    class pod_infoClass:
        playing=False
        curr_id=0
        bookmarker_id=0
        term=0
        pod_chip_cnt=0
        pokes=[0,0,0]
    
    class last_actionClass:
        user_id=0
        action_type=0
        raise_num=0
        
    global pod_info
    global last_action
    pod_info=pod_infoClass()
    last_action=last_actionClass()
    
    user_infoType=np.dtype(
        {
            'names':['user_name','seat_id','stack_cnt','chip_cnt','folded','last_action','hand_poke0','hand_poke1'],
            'formats':['a','i','i','i','b','i','i','i']
            #names表示所需变量名，formats表示变量名对应的数据类型
        }
    )
    #建立一个有八个元素的初始化为0的数组保存user_info
    user_info=np.array([('zero',0.,0.,0.,0.,0.,0.,0.)]*10,dtype=user_infoType)
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
        self.cnt=chip_cnt
    
    def start_game(room_id):
        pod_info.playing=True
    
    def stand(self,room_id,user_name):
        pass
    
    def action(self,user_name,action_type,raise_num):
        pod_info.curr_id=user_name
        last_action.user_id=user_name
        last_action.action_type=action_type
        last_action.raise_num=raise_num
    
    def request_game_info(self,room_id,user_name):
        i=1
        while i<9:
            if self.user_info[i]['username']==user_name:
                pod_info.your_id = i
                break
            i += 1
        if i==9:
            pod_info.your_id=0
        return self
        





        