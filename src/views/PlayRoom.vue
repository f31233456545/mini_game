<template>
<div class="play-room">
  
    <div class="play-room-header">
        <div class="room-info">
            <div class="room-name">
                {{this.$store.getters.currRoom.room_name}}
            </div>
            <div class="room-id">
                {{"房间号: "+this.$store.getters.currRoom.room_id}}
            </div>
            <div class="spectate">
                <div class="spectate-icon">
                    <img :src="spectate"/>
                </div>
                <div class="spectate-num">
                    {{this.$store.getters.currRoom.viewer_num}}
                </div>
            </div>
        </div>
        <div class="button-group1">
            <el-button type="success">坐下</el-button>
            <el-button type="warning">站起</el-button>
            <el-button type="danger">离开房间</el-button>
        </div>
    </div>

    <Player 
    v-for="i in [1,2,3,4,5,6,7,8]"
    :pos="i"
    />

    <GameBoard/>

    <div class="play-room-footer">
        <div class="button-group2">
            <el-button type="success">加注</el-button>
            <el-button type="primary">跟注/过牌</el-button>
            <el-button type="danger">弃牌</el-button>
        </div>
    </div>
  
</div>
</template>
  
<script>

import table0 from "../assets/table.jpg"
import spectate from "../assets/icons/eye.svg"
import Player from '../components/Player.vue'
import GameBoard from '../components/GameBoard.vue'
  
export default {
    name: 'PlayRoom',
    components: {
        Player,
        GameBoard
    },
    data(){
        return{
            table0: table0,
            spectate: spectate,
        };

    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === parseInt(this.$route.params.id))
        }
    },
    props: {
      room_id: Number,
    },
    methods: {
      open2() {
        this.$notify({
          title: '操作提示',
          message: '玩家5加注15,玩家6开始操作',
          duration: 0,
          offset: 100
        });
      }
    },
    mounted() {
      //this.$store.commit('enterRoom')
    },
    unmounted(){
      this.$store.commit('exitRoom')
    },
}
</script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.play-room {
    background-image: url("../assets/table.jpg");
    background-repeat: no-repeat;
    background-size: 100% 100%;
    height: 100%;
    overflow: hidden;
    width: 100%;
    position: absolute;
}
.play-room-header {
    position: absolute;
    top: 0px;
    width: 100%;
    height: 40px;
}
.room-info {
    display: flex;
    float: left;
    position: relative;
}
.room-name {
    display: flex;
    float: left;
    height: 30px;
    font-size: 20px;
    color: white;
    background: rgba(50,50,120,1);
    border-radius: 2px;
    margin-top: 5px;
    margin-left: 5px;
    margin-right: 5px;
    padding-left: 5px;
    padding-right: 5px;
}
.room-id {
    display: flex;
    float: left;
    height: 30px;
    font-size: 16px;  
    color: white;
    background: rgba(150,100,60,1);
    border-radius: 2px;
    margin-top: 5px;
    padding-left: 5px;
    padding-right: 5px;      
}
.spectate {
    position: absolute;
    top: 40px;
    left: 10px;
}
.spectate-icon {
    display: flex;
    float: left;
    width: 30px;
    height: 30px;
    padding: 4px;
}
.spectate-num {
    display: flex;
    float: left;
    height: 30px;
    color: rgb(50,200,240);
    font-size: 20px;
    padding: 4px;
}
.play-room-footer {
    position: absolute;
    bottom: 0px;
    width: 100%;
    height: 60px;
    text-align: center;
}
.button-group1 {
    display: flex;
    float: right;
    margin-top: 5px;
    margin-right: 20px;
}
.button-group2 {

}


</style>
  