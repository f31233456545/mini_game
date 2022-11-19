<template>
  <div class="play-room">
    <div class="play-room-header">
      <div class="room-info">
        <div class="room-name">
          {{this.$store.state.room_name}}
        </div>
        <div class="room-id">
          {{"房间号: "+this.$store.state.room_id}}
        </div>
        <div class="spectate">
          <div class="spectate-icon">
            <img :src="spectate" />
          </div>
          <div class="spectate-num">
            {{this.$store.state.viewer_num}}
          </div>
        </div>

      </div>
      <div class="button-group1">
        <el-button type="success" @click="sit({room_id:this.$store.state.inRoomId,user_name:this.$store.state.userName})">坐下</el-button>
        <el-button type="warning" @click="stand({room_id:this.$store.state.inRoomId,user_name:this.$store.state.userName})">站起</el-button>
        <el-button type="danger" @click="exit_room({room_id:this.$store.state.inRoomId,user_name:this.$store.state.userName})">离开房间</el-button>
        <el-button type="danger" @click=" request_gameinfo">轮询</el-button>
      </div>
    </div>

    <GameBoard />

    <div class="play-room-footer">
      <div v-if="!playing && this.$store.state.gameInfo.user_infos[0].seat_id==this.$store.state.gameInfo.pod_info.bookmarker_id" class="waiting">
        <el-button type="danger" @click="start">开始游戏</el-button>
      </div>
      <div v-if="playing" class="playing">
        <div v-if="!acting && this.$store.state.gameInfo.user_infos[0].seat_id==this.$store.state.gameInfo.pod_info.curr_id" class="button-group2">
          <el-input-number v-model="num" @change="handleChange" :step="1" step-strictly :min=this.$store.state.gameInfo.last_action.raise_num+1 :max=this.$store.state.gameInfo.user_infos[0].stack_cnt></el-input-number>
          <el-button type="success" @click="bet">加注</el-button>
          <el-button type="primary" @click="call">跟注</el-button>
          <el-button type="danger" @click="fold">弃牌</el-button>
        </div>
      </div>
    </div>

  </div>
</template>
  
<script>

import table0 from "../assets/table.jpg"
import spectate from "../assets/icons/eye.svg"
import store from "../store/index.js";
import Player from '../components/Player.vue'
import GameBoard from '../components/GameBoard.vue'
import { request } from "../utils/request.js";

  
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
            playing: false,
            acting: false,
            num: this.$store.state.gameInfo.last_action.raise_num + 1
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
      },

      handleChange(value) {
        console.log(value);
      },

      sit(sit_data) {
      const self = this;
      request("sit", sit_data) 
        .then(function (res) {
          switch (res.succeed) {
            case true:
            self.$message.success('已坐下！');
            store.commit("sit");
            case false:
            self.$message.error('发生错误！');
            console.log(res.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });    

    },
    stand(stand_data) {
      const self = this;
      request("stand", stand_data) 
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            self.$message.success('已站起！');
            store.commit("stand");
            case false:
            self.$message.error('发生错误！');
            console.log(res.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
        
    },
    exit_room(exit_data) {
      const self = this;
      request("exit_room", exit_data)
        .then(function (res) {
          switch (res.succeed) {
            case true:
            console.log(res.succeed);
            store.commit("stand");
            store.commit("exitRoom");
            self.$message.success('已退出房间！');
            console.log(exit_data);
            return self.$router.push({ name: 'enter-game', params: { id:store.state.inGameId,name:exit_data.user_name}})
            case false:
              console.log('res.message'+res.message);
              console.log('exit_data'+exit_data);
              console.log('store.state.inRoomId'+store.state.inRoomId);
              console.log('store.state.inRoomId'+store.state.inRoomId);
            self.$message.error('发生错误！（房间可能不存在）');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },






    start(){
      const self = this;
    //  self.playing = true;
      var start_data = {
        room_id: self.room_id
      };
      request("start_game",start_data)
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            self.$message.success('游戏开始！');
            self.playing = true;
            case false:
            self.$message.error('发生错误！');
            console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    bet(){
      const self = this;
      self.acting = true;
      var bet_data = {
        user_name: self.$store.state.gameInfo.user_infos[0].user_name,
        action_type: 2,
        raise_num: self.num,
        room_id: self.room_id,
      };
      request("action",bet_data)
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            self.$message.success('已下注！');
            case false:
            self.$message.error('发生错误！');
            console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    call(){
      const self = this;
      self.acting = true;
      var call_data = {
        user_name: self.$store.state.gameInfo.user_infos[0].user_name,
        action_type: 1,
        raise_num: self.$store.state.gameInfo.last_action.raise_num,
        room_id: self.room_id,
      };
      request("action",call_data)
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            self.$message.success('已跟注！');
            case false:
            self.$message.error('发生错误！');
            console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    fold(){
      const self = this;
      self.acting = true;
      var fold_data = {
        user_name: self.$store.state.gameInfo.user_infos[0].user_name,
        action_type: 0,
        raise_num: self.$store.state.gameInfo.user_infos[0].chip_cnt,
        room_id: self.room_id,
      };
      request("action",fold_data)
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            self.$message.success('已下注！');
            case false:
            self.$message.error('发生错误！');
            console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        }); 
    },

    request_gameinfo()
    {
      const self = this;
      let  timer = setInterval(() => {
        this.fun(timer)
         }, 1000)
      },
    fun (timer) {
      var request_data = {
        room_id:  store.state.inRoomId,
        user_name: store.state.userName,
      };
         setTimeout(()=>{
                console.log("开始轮循请求：");
                request("request_game_info", request_data)
                .then(data => {
                    store.commit('updataGameinfo', data)
                    console.log(data)
                    if(store.state.gameInfo.pod_info.playing==false){
                             clearInterval(timer);
                             console.log("结束轮循请求：");
                             }
                })
        .catch((err) => {
          console.log(err);
        });
        }, 0)
      }
     },
    mounted() {
      //this.$store.commit('enterRoom')
    },
    unmounted() {
      //this.$store.commit('exitRoom')
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
  background: rgba(50, 50, 120, 1);
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
  background: rgba(150, 100, 60, 1);
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
  color: rgb(50, 200, 240);
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