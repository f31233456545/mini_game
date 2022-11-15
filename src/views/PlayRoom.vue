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
            <el-button type="success" @click="sit">坐下</el-button>
            <el-button type="warning" @click="stand">站起</el-button>
            <el-button type="danger" @click="exit_room">离开房间</el-button>
        </div>
    </div>

    <GameBoard/>

    <Player
        v-for="i in [1,2,3,4,5,6,7,8]"
        :pos="i"
    />

    <div class="play-room-footer">
        <div class="button-group2">
            <el-button type="success">加注</el-button>
            <el-button type="primary">跟注/过牌</el-button>
            <el-button type="danger">弃牌</el-button>
        </div>
    </div>

    <!-- 调试用 -->
    <div class="debug">
        <el-button type="primary" @click="debug1">debug: change</el-button>
    </div>
  
</div>
</template>
  
<script>

import table0 from "../assets/table.jpg"
import spectate from "../assets/icons/eye.svg"
import Player from '../components/Player.vue'
import GameBoard from '../components/GameBoard.vue'
import {request} from '../utils/request.js'
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
        };

    },
    computed:{
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
            })
        },
        sit() {
            const self = this
            var sit_data = {
                room_id:self.$route.params.room_id,
                user_name:self.$route.params.userName
            }
            request("sit", sit_data) 
                .then(function (res) {
                    switch (res.succeed) {
                    case true: 
                        self.$message.success('已坐下！')
                        break
                    case false:
                        console("sit err!")
                        self.$message.error('发生错误！')
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        
        },
        stand() {
            const self = this;
            var stand_data = {
                room_id:self.$route.params.room_id,
                user_name:self.$route.params.userName
            };
            request("stand", stand_data) 
                .then(function (res) {
                    console.log(res.data)
                    switch (res.succeed) {
                    case true:
                        self.$message.success('已站起！')
                        break
                    case false:
                        self.$message.error('发生错误！')
                        console(succeed.message)
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        },
        exit_room() {
            const self = this
            var exit_data = {
                room_id:self.$route.params.room_id,
                user_name:self.$route.params.userName
            }
        request("exit_room", exit_data)
            .then(function (res) {
            switch (res.succeed) {
            case true:
                self.$message.success('已退出房间！')
                self.$store.exitRoom()
                router.back()
                break
            case false:
                self.$message.error('发生错误！')
                console(succeed.message)
            }
            })
            .catch((err) => {
                console.log(err)
            });
            
        },
        // debug 改变游戏信息
        debug1(){
            this.$store.commit('changeInfo')
        }
    },
    watch: {
        lastAction(newLastAction,oldLastAction){
            const self = this
            let user_id = newLastAction.user_id
            let action_type = newLastAction.action_type
            let raise_num = newLastAction.raise_num
            let user = self.userInfos.find(user => user.seat_id===user_id)
            let user_name = user.user_name
            let chip_cnt = user.chip_cnt
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
    },
    unmounted() {
        document.body.style.overflow = "auto"
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

/* debug */
.debug{
    position: absolute;
    top: 100px;
    left: 10px;
}
</style>
  