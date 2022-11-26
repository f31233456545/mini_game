<template>
  <div class="play-room">
      <div class="play-room-header">
          <div class="room-info">
              <div class="room-name">
                  {{gameInfo.room_name}}
              </div>
              <div class="room-id">
                  {{"房间号: "+this.$route.params.room_id}}
              </div>
              <div class="spectate">
                  <div class="spectate-icon">
                      <img :src="spectate"/>
                  </div>
                  <div class="spectate-num">
                      {{gameInfo.view_cnt}}
                  </div>
              </div>
  
          </div>
          <div class="button-group1">
              <el-button 
                  v-if="!seated"
                  type="success" 
                  @click="sit({
                              room_id:this.$store.state.inRoomId,
                              user_name:this.$store.state.userName,
                              chip_cnt:600,
                          })"
              >
                  坐下
              </el-button>
              <el-button 
                  v-if="seated"
                  type="warning" 
                  @click="stand({
                          room_id:this.$store.state.inRoomId,
                          user_name:this.$store.state.userName
                      })"
              >
                  站起
              </el-button>
              <el-button 
                  type="danger" 
                  @click="exit_room({
                          room_id:this.$store.state.inRoomId,
                          user_name:this.$store.state.userName
                      })"
              >
                  离开房间
              </el-button>
          </div>
      </div>
  
      <GameBoard v-if="playing"/>

  
      <div class="play-room-footer">
          <div v-if="!playing && isHost && seated" class="waiting">
              <el-button type="danger" @click="start">开始游戏</el-button>
          </div>
          <div v-if="playing && acting" class="playing">
              <div v-if="acting" class="button-group2">
                  <!-- <el-input-number 
                      v-model="num" @change="handleChange" 
                      :step="1" step-strictly 
                      :min="this.$store.state.gameInfo.last_action.raise_num+1"
                      :max="this.$store.state.gameInfo.user_infos[0].stack_cnt" 
                  ></el-input-number> -->
                  <el-button type="success" @click="raise">加注</el-button>
                  <el-button type="primary" @click="call">跟注</el-button>
                  <el-button type="danger" @click="fold">弃牌</el-button>
              </div>
          </div>
      </div>
  
      <!-- 调试用 -->
      <div class="debug">
          <el-button type="primary" @click="debug1">debug: close timer</el-button>
          <el-button type="primary" @click="debug2">debug: get game info</el-button>
      </div>  
  
  </div>
  </template>
    
  <script>
  import table0 from "../assets/table.jpg"
  import spectate from "../assets/icons/eye.svg"
  import Player from '../components/Player.vue'
  import GameBoard from '../components/GameBoard.vue'
  import store from "../store/index.js"
  import router from "../router/index.js"
  import { request } from "../utils/request.js"
  import { createActionPopup } from '../utils/popup.js'
    
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
              timeInter: null, // 定时器，mount时设定
          };
      },
      computed:{
          roomId(){
              return this.$store.state.inRoomId
          },
          userName(){
              return this.$store.state.userName
          },
          gameInfo(){
              return this.$store.state.gameInfo
          },
          lastAction(){
              return this.gameInfo.last_action
          },
          userInfos(){
              return this.gameInfo.user_infos
          },
          term(){
              switch(this.gameInfo.pod_info.term){
              case 0:
                  return "PREFLOP"
              case 1:
                  return "FLOP"
              case 2:
                  return "TURN"
              case 3:
                  return "RIVER"
              }
          },
          playing(){
              return this.gameInfo.pod_info.playing
          },
          acting(){
              return this.gameInfo.pod_info.your_id == this.gameInfo.pod_info.curr_id
          },
          isHost(){
              //return this.gameInfo.your_id == this.gameInfo.pod_info.bookmarker_id
              return true
          },
          seated(){
              return this.$store.state.sitDown
          },
          defaultRaiseNum(){
              return this.lastAction.raise_num+1
          }
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
                          self.$message.success('已坐下！')
                          self.$store.commit("sit")
                          this.request_gameinfo()
                          break
                      case false:
                          console.log("sit err!")
                          self.$message.error('发生错误！')
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  })   
          },
          stand(stand_data) {
              const self = this;
              request("stand", stand_data) 
                  .then(function (res) {
                      console.log(res.data)
                      switch (res.succeed) {
                      case true:
                          self.$message.success('已站起！')
                          self.$store.commit("stand")
                          this.request_gameinfo()
                          break
                      case false:
                          self.$message.error('发生错误！')
                          console.log(res.message)
                          break
                      }
                  })
                  .catch((err) => {
                      console.log(err)
                  })
          },
          exit_room(exit_data) {
              const self = this;
              request("exit_room", exit_data)
                  .then(function (res) {
                      switch (res.succeed) {
                      case true:
                          store.commit("stand")
                          self.$store.commit("exitRoom")
                          return self.$router.push({ name: 'enter-game', params: { id:store.state.inGameId,name:exit_data.user_name}})
                          break
                      case false:
                          if(self.seated){
                              self.$message.error('请先站起！')
                          }
                          else{
                              self.$message.error('发生错误！')
                          }
                          console.log(res.message)
                          break
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  });
          },
          start(){
              const self = this;
              var start_data = {
                  room_id: self.roomId
              };
              request("start_game",start_data)
                  .then(function (res) {
                      console.log(res.data);
                      switch (res.succeed) {
                      case true:
                          self.$message.success('游戏开始！')
                          self.playing = true
                          break
                      case false:
                          self.$message.error('发生错误！')
                          console.log(res.message)
                          break
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  });
          },
          fold(){ //弃牌
              const self = this
              var fold_data = {
                  user_name: self.userName,
                  action_type: 0,
                  raise_num: 0,
                  room_id: self.roomId,
              }
              request("action",fold_data)
                  .then(function (res) {
                      console.log(res.data);
                      if(!res.succeed){
                          self.$message.error('发生错误！')
                          console.log(res.message)
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  });
          },
          call(){ //跟注
              const self = this
              var call_data = {
                  user_name: self.userName,
                  action_type: 1,
                  raise_num: self.lastAction.raise_num,
                  room_id: self.roomId,
              }
              request("action",call_data)
                  .then(function (res) {
                      console.log(res.data)
                      if(!res.succeed){
                          self.$message.error('发生错误！')
                          console.log(res.message)
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  });
          },
          raise(){ //加注
              const self = this
              var raise_data = {
                  user_name: self.userName,
                  action_type: 2,
                  raise_num: self.lastAction.raise_num,
                  room_id: self.roomId, 
              }
              request("action",raise_data)
                  .then(function (res) {
                      console.log(res.data)
                      if(!res.succeed){
                          self.$message.error('发生错误！')
                          console.log(res.message)
                      }
                  })
                  .catch((err) => {
                      console.log(err);
                  });
          },
          request_gameinfo(){
              const self = this;
              var request_data = {
                  room_id:  self.$store.state.inRoomId,
                  user_name: self.$store.state.userName,
              };
              request("request_game_info", request_data)
                  .then(data => {
                      self.$store.commit('updataGameinfo', data)
                      console.log(data)
                  })
                  .catch((err) => {
                      console.log(err)
                  })
          },
          // debug 改变游戏信息
          debug1(){
              //this.$store.commit('changeInfo')
              clearInterval(this.timeInter)
              this.timeInter = null
          },
          debug2(){
              this.request_gameinfo()
              console.log(this.acting)
          }
      },
      watch: {
          lastAction(newLastAction,oldLastAction){
              if(oldLastAction == null){
                  return
              }
              if(newLastAction.user_id == oldLastAction.user_id && newLastAction.action_type == oldLastAction.action_type){
                  return
              }
              const self = this
              let user_id = newLastAction.user_id
              let user_name = ""
              let chip_cnt = -1
              let action_type = newLastAction.action_type
              let raise_num = newLastAction.raise_num
              let user = self.userInfos.find(user => user.seat_id===user_id)
              if(user){
                  user_name = user.user_name
                  chip_cnt = user.chip_cnt
              }
              let title = ""
              let action = ""
              switch(action_type){
              case 0: // 弃牌
                  title = user_id + " " + user_name
                  action = "弃牌"
                  break;
              case 1: // 过牌
                  title = user_id + " " + user_name
                  action = "过牌"
                  break;
              case 2: // 跟注
                  title = user_id + " " + user_name
                  action = "跟注到" + chip_cnt
                  break;
              case 3: // 加注
                  title = user_id + " " + user_name
                  action = "加注到" + chip_cnt
                  break;
              case 4: // 新回合
                  title = "<< " + self.term + " >>"
                  action = ""
                  break;
              case 5: // 结束
                  title = "游戏结束！"
                  action = ""
                  break;
              }
              createActionPopup(
                  title,
                  action
              )
          }
      },
      mounted() {
          //this.$store.commit('enterRoom')
          document.body.style.overflow = "hidden"
          this.request_gameinfo()
          this.timeInter = setInterval(() => {
              this.request_gameinfo()
          }, 1000);
      },
      unmounted() {
          document.body.style.overflow = "auto"
          clearInterval(this.timeInter)
          this.timeInter = null
          if(this.$store.state.inRoomId!=0){
              this.exit_room({
                          room_id:this.$store.state.inRoomId,
                          user_name:this.$store.state.userName,
                          force:true,
                      })
          }
      },
  }
  if (sessionStorage.getItem('store')) {
  try {
    store.replaceState(JSON.parse(sessionStorage.getItem('store')))
  } 
  catch (error) {
    console.log(error);
  }
}
window.addEventListener('beforeunload', () => {
  sessionStorage.setItem('store', JSON.stringify(store.state));
});
window.addEventListener("popstate", function(e) { 
  this.exit_room({
                          room_id:this.$store.state.inRoomId,
                          user_name:this.$store.state.userName
                      });	
}, false);
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
  /* debug */
  .debug{
      position: absolute;
      top: 100px;
      left: 10px;
  }
  </style>
    