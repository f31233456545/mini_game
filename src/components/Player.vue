<template>
    <div :class="'player p'+pos" v-if="playerInfo.user_name!=''">
        <div class="player-container">
            <div class="your-pos-tip" v-if="seated && pos==1">YOU<br/><span class="pointer">▼</span></div>
            <div :class="inAction?'user-wrapper in-action':'user-wrapper'">
                <div class="user-name">{{playerInfo.user_name}}</div>
                <img class="user-icon" src="../assets/icons/user-regular.svg" />
                <div class="user-chip">
                    <img class="chip-icon" src="../assets/icons/chip.png"/>
                    <div class="stack-cnt">
                        {{playerInfo.stack_cnt}}
                    </div>
                </div>
                <div :class="'tag '+playerCharacter[0]">
                    {{playerCharacter[1]}}
                </div>
                <div class="action-info">
                    {{inAction?'行动中...':''}}
                </div>
                <div class="waiting-info">
                    {{waiting?'等待中...':''}}
                </div>
                <div :class="'last-action '+lastAction[0]" v-if="showActionTag">
                    {{lastAction[1]}}
                </div>
                <div class="put-chip">
                    <img class="chip-icon2" src="../assets/icons/chip2.png"/>
                    <div class="chip-cnt">
                        {{playerInfo.chip_cnt}}
                    </div>
                </div>
            </div>

            <div class="hand">
                <Card
                v-for="i in playerInfo.hand_pokes"
                :value="i"
                />
            </div>

            <div class="seat-id">
                {{playerInfo.seat_id}}
            </div>
        </div>
    </div>
    <div :class="'empty p'+pos" v-else>
        <div class="player-container">
            <div class="empty-wrapper">
                <div class="empty-sign">空位</div>
            </div>
            
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'
import SimplePopup from './SimplePopup.vue'

export default{
    components:{Card, SimplePopup},
    props:{
        pos: Number,
    },
    computed:{
        gameInfo(){
            return this.$store.state.gameInfo
        },
        seated(){
            return this.gameInfo.pod_info.your_id >=1 && this.gameInfo.pod_info.your_id <=8
        },
        seatId(){ // 该位置玩家座位号
            if(this.seated){
                return (this.pos + this.gameInfo.pod_info.your_id-2) % 8 + 1
            }
            else{
                return this.pos
            }
        },
        playerInfo(){
            return this.gameInfo.user_infos[this.seatId-1]
        },
        playerCharacter(){
            if(!this.gameInfo.pod_info.playing || this.playerInfo.folded)
                return ["normal-player",""]
            let bookmarkerId = this.gameInfo.pod_info.bookmarker_id
            let smallId = this.gameInfo.pod_info.small_id
            let bigId = this.gameInfo.pod_info.big_id
            if(this.playerInfo.seat_id==smallId){
                return ["small-blind","小盲"]
            }
            else if(this.playerInfo.seat_id==bigId){
                return ["big-blind","大盲"]
            }
            if(this.playerInfo.seat_id==bookmarkerId){
                return ["bookmarker","庄家"]
            }
            else{
                return ["normal-player",""]
            }
        },
        inAction(){
            return (this.playerInfo.seat_id == this.gameInfo.pod_info.curr_id) && (this.gameInfo.pod_info.playing)
        },
        waiting(){
            if(this.playerInfo.hand_pokes.length == 0){
                return true
            }
            else{
                return false
            }
        },
        showActionTag(){
            return this.$store.state.showAction[this.seatId-1]
        },
        lastAction(){
            if(!this.gameInfo.pod_info.playing)
                return ["no-action",""]
            let actionType = this.playerInfo.last_action
            switch(actionType){
            case 0:
                return ["fold","弃牌"]
            case 1:
                return ["follow","跟注"]
            case 2:
                return ["raise","加注"]
            default:
                return ["no-action",""]
            }
        },

    }
}
</script>
<style scoped>
.player{
    position: absolute;
}

.empty{
    position: absolute;
}
.empty-sign{
    position: absolute;
    top: 40px;
    height: 40px;
    width: 100px;
    color: rgba(255,255,255,0.5);
    font-size: 30px;
    text-align: center;
}
.empty-wrapper{
    position: absolute;
    height: 120px;
    width: 100px;
    border: solid;
    border-color: rgba(255,255,255,0.5);
    border-width: 1px;
    border-radius: 6px;
}

.p1{
    left: 50%;
    top: 80%;
}
.p2{
    left: 20%;
    top: 65%;
}
.p3{
    left: 20%;
    top: 35%;
}
.p4{
    left: 30%;
    top: 15%;
}
.p5{
    left: 50%;
    top: 15%;
}
.p6{
    left: 70%;
    top: 15%;
}
.p7{
    left: 80%;
    top: 35%;
}
.p8{
    left: 80%;
    top: 65%;
}

.player-container{
    position: absolute;
    width: 220px;
    height: 120px;
    top: -60px;
    left: -50px;
}
.user-wrapper{
    height: 120px;
    width: 100px;
    background: rgba(100,150,210,0.5);
    border: solid;
    border-color: rgba(255,255,255,0);
    border-width: 1px;
}
.in-action{
    border-color: rgba(255,255,50,1);
}
.user-name{
    font-size: 16px;
    height: 20px;
    color: white;
    padding-right: 6px;
    overflow: visible;  
    text-align: center;
    background: rgba(100,180,220,1);
}
.user-icon{
    width: 100px;
    height: 75px;
    padding-left: 15px;
    padding-right: 15px;
    padding-top: 5px;
    opacity: 30%;
}

.user-chip{
    height: 19px;
    background: rgba(80,200,50,1);
}
.chip-icon{
    width: 20px;
    height: 20px;
    display: flex;
    float: left;
    margin-left: 5px;
    margin-right: 5px;
}
.stack-cnt{
    display: flex;
    float: left;
    color: white;
}

.action-info{
    position: absolute;
    width: 100px;
    height: 20px;
    top: 50px;
    left: 0px;
    font-size: 16px;
    color: yellow;
    text-align: center;
}
.waiting-info{
    position: absolute;
    width: 100px;
    height: 20px;
    top: 50px;
    left: 0px;
    font-size: 16px;
    color: rgb(180,180,180);
    text-align: center;
}

.last-action{
    position: absolute;
    width: 60px;
    height: 20px;
    top: 76px;
    left: 2px;
    font-size: 14px;
    color: white;
    text-align: center;
    border-radius: 4px;
}
.no-action{
    background: none;
}
.fold{
    background: rgba(128,128,128,0.8);
}
.follow{
    background: rgba(64,158,255,0.8);
}
.raise{
    background: rgba(103,194,58,0.8);
}

.put-chip{
    position: absolute;
    width: 40px;
    height: 26px;
    top: 73px;
    left: 60px;
}
.chip-icon2{
    position: absolute;
    width: 26px;
    height: 26px;
    margin-left: 7px;
    opacity: 50%;
}
.chip-cnt{
    position: absolute;
    top: 2px;
    width: 40px;
    height: 22px;
    color: rgb(220,255,200);
    font-size: 16px;
    text-align: center;
    padding: 2px;
}

.tag{
    position: absolute;
    width: 40px;
    height: 20px;
    top: 21px;
    left: 1px;
    font-size: 14px;
    color: white;
    text-align: center;
}
.bookmarker{
    background: rgba(180,50,50,1);
}
.small-blind{
    background: rgba(50,180,50,1);
}
.big-blind{
    background: rgba(80,80,180,1);
}
.normal-player{
    opacity: 0%;
}

.hand{
    position: absolute;
    left: 105px;
    top: 40px;
}

.seat-id{
    position: absolute;
    left: -15px;
    top: 2px;
    color: white;
    text-align: center;
}

@keyframes tip-animation{
0%{

}
100%{
    transform: translate(0px,-3px);
}
}
.your-pos-tip{
    position: absolute;
    left: 0px;
    top: -30px;
    width: 100px;
    color: white;
    font-size: 10px;
    text-align: center;
    animation: tip-animation 0.7s linear infinite alternate;
    -webkit-animation: tip-animation 0.7s linear infinite alternate;
}
.pointer{
    position: relative;
    top: -2px;
    font-size: 10px;
}
</style>