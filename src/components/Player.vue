<template>
    <div :class="'player p'+pos" v-if="playerInfo.user_name!=''">
        <div class="player-container">
            <div class="user-wrapper">
                <div class="user-name">{{playerInfo.user_name}}</div>
                <img class="user-icon" src="../assets/icons/user-regular.svg" />
                <div class="user-chip">
                    <img class="chip-icon" src="../assets/icons/chip2.png"/>
                    <div class="chip-num">
                        {{playerInfo.stack_cnt}}
                    </div>
                </div>
                <div :class="'tag '+playerCharacter[0]">
                    {{playerCharacter[1]}}
                </div>
                <div class="action-info">
                    行动中...
                </div>
            </div>

            <div class="hand">
                <Card :value="playerInfo.hand_pokes[0]"/>
                <Card :value="playerInfo.hand_pokes[1]"/>
            </div>
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'

export default{
    components:{Card},
    props:{
        pos: Number,
    },
    computed:{
        playerInfo(){
            return this.$store.state.gameInfo.user_infos[this.pos-1]
        },
        playerCharacter(){
            let bookmarkerId = this.$store.state.gameInfo.pod_info.bookmarker_id;
            if(this.playerInfo.seat_id==bookmarkerId){
                return ["bookmarker","庄家"]
            }
            else if(this.playerInfo.seat_id==(bookmarkerId%8)+1){
                return ["small-blind","小盲"]
            }
            else if(this.playerInfo.seat_id==((bookmarkerId+1)%8)+1){
                return ["big-blind","大盲"]
            }
            else{
                return ["normal-player",""]
            }
        }
    },
}
</script>
<style scoped>
.player{
    position: absolute;
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
    left: -110px;
}
.user-wrapper{
    height: 120px;
    width: 100px;
    background: rgba(100,150,210,0.5);
    border-radius: 6px;
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
    height: 20px;
    background: rgba(70,180,120,1);
}
.chip-icon{
    width: 20px;
    height: 20px;
    display: flex;
    float: left;
    margin-left: 5px;
    margin-right: 5px;
}
.chip-num{
    display: flex;
    float: left;
    color: rgb(60,60,200);
}
.action-info{
    position: absolute;
    width: 100px;
    height: 30px;
    top: 70px;
    left: 0px;
    padding-top: 5px;
    padding-bottom: 5px;
    font-size: 16px;
    color: yellow;
    text-align: center;
}
.tag{
    position: absolute;
    width: 40px;
    height: 20px;
    top: 20px;
    left: 0px;
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
</style>