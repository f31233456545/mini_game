<template>
    <div class="play-room">
        <div class="play-room-header">
            <div class="room-info">
                <div class="room-name">
                    {{ gameInfo.room_name }}
                </div>
                <div class="room-id">
                    {{ "房间号: " + this.$route.params.room_id }}
                </div>
                <div class="spectate-state" v-if="!seated">
                    您尚未坐下，正在观战
                </div>
                <div class="spectate">
                    <div class="spectate-icon">
                        <img :src="spectate" />
                    </div>
                    <div class="spectate-num">
                        {{ gameInfo.view_cnt }}
                    </div>
                </div>

            </div>

            <div class="button-group1">
                <div class="sit-tip" v-if="!seated">点击这里坐下 ▷</div>
                <el-button v-if="!seated" type="success" @click="sit({
                    room_id: this.$store.state.inRoomId,
                    user_name: this.$store.state.userName,
                    chip_cnt: 600,
                })">
                    坐下
                </el-button>
                <el-button v-if="seated" type="warning" @click="stand({
                    room_id: this.$store.state.inRoomId,
                    user_name: this.$store.state.userName
                })">
                    站起
                </el-button>
                <el-button type="danger" @click="exit_room({
                    room_id: this.$store.state.inRoomId,
                    user_name: this.$store.state.userName
                })">
                    离开房间
                </el-button>
            </div>
        </div>

        <GameBoard v-if="playing" />

        <Player v-for="i in [1, 2, 3, 4, 5, 6, 7, 8]" :pos="i" />


        <div class="play-room-footer">
            <div v-if="!playing && isHost && seated" class="waiting">
                <el-button type="danger" @click="start">开始游戏</el-button>
            </div>
            <div v-if="playing && acting" class="playing">
                <div v-if="acting" class="button-group2">
                    <el-input-number v-model="num" @change="handleChange" :step="1"></el-input-number>
                    <el-button type="success" @click="raise" :disabled="raiseCheck">加注</el-button>
                    <el-button type="primary" @click="call">跟注</el-button>
                    <el-button type="danger" @click="fold">弃牌</el-button>
                </div>
            </div>
        </div>

        <!-- 调试用 -->
        <div class="debug" v-if="debug">
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
import { createSimplePopup } from '../utils/popup.js'

export default {
    name: 'PlayRoom',
    components: {
        Player,
        GameBoard
    },
    data() {
        return {
            table0: table0,
            spectate: spectate,
            num: 0,
            oldPodChipCount: 0,
            timeInter: null, // 定时器，mount时设定
            debug: false,
        };
    },
    computed: {
        roomId() {
            return this.$store.state.inRoomId
        },
        userName() {
            return this.$store.state.userName
        },
        gameInfo() {
            return this.$store.state.gameInfo
        },
        lastAction() {
            return this.gameInfo.last_action
        },
        userInfos() {
            return this.gameInfo.user_infos
        },
        term() {
            switch (this.gameInfo.pod_info.term) {
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
        playing() {
            return this.gameInfo.pod_info.playing
        },
        acting() {
            return this.gameInfo.pod_info.your_id == this.gameInfo.pod_info.curr_id
        },
        isHost() {
            //return this.gameInfo.your_id == this.gameInfo.pod_info.bookmarker_id
            return true
        },
        seated() {
            return this.$store.state.sitDown
        },
        defaultRaiseNum() {
            return this.lastAction.raise_num + 1
        },
        yourInfo() {
            return this.userInfos.find(info => info.seat_id === this.gameInfo.pod_info.your_id)
        },
        raiseCheck(){
            return this.num!=parseInt(this.num)||this.num<=this.lastAction.raise_num||this.num>this.yourInfo.stack_cnt
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
                            // self.request_gameinfo()
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
                            // self.request_gameinfo()
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
            if (self.seated) {
                self.$message.error('请先站起！')
                return
            }
            request("exit_room", exit_data)
                .then(function (res) {
                    switch (res.succeed) {
                        case true:
                            store.commit("stand")
                            self.$store.commit("exitRoom")
                            router.back()
                            self.$message.success('已退出房间！')
                            break
                        case false:
                            console.log(res.message)
                            break
                    }
                })
                .catch((err) => {
                    console.log(err);
                });


        },
        start() {
            const self = this;
            var start_data = {
                room_id: self.roomId
            };
            request("start_game", start_data)
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
        fold() { //弃牌
            const self = this
            var fold_data = {
                user_name: self.userName,
                action_type: 0,
                raise_num: self.lastAction.raise_num,
                room_id: self.roomId,
            }
            request("action", fold_data)
                .then(function (res) {
                    console.log(res.data);
                    if (!res.succeed) {
                        self.$message.error('发生错误！')
                        console.log(res.message)
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        call() { //跟注
            const self = this
            var call_data = {
                user_name: self.userName,
                action_type: 1,
                raise_num: self.lastAction.raise_num,
                room_id: self.roomId,
            }
            request("action", call_data)
                .then(function (res) {
                    console.log(res.data)
                    if (!res.succeed) {
                        self.$message.error('发生错误！')
                        console.log(res.message)
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        raise() { //加注
            const self = this
            var raise_data = {
                user_name: self.userName,
                action_type: 2,
                raise_num: self.num,
                room_id: self.roomId,
            }
            if(self.num==parseInt(self.num)&&self.num>self.lastAction.raise_num&&self.num<=self.userInfos.find(info => info.seat_id === this.gameInfo.pod_info.your_id).stack_cnt){
            request("action", raise_data)
                .then(function (res) {
                    console.log(res.data)
                    if (!res.succeed) {
                        self.$message.error('发生错误！')
                        console.log(res.message)
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
            }
            else{
                self.$message.error('加注不合法，请重新加注')
            }
        },
        request_gameinfo() {
            const self = this;
            var request_data = {
                room_id: self.$store.state.inRoomId,
                user_name: self.$store.state.userName,
            };
            request("request_game_info", request_data, false)
                .then(data => {
                    self.$store.commit('updataGameinfo', data)
                    console.log(data)
                })
                .catch((err) => {
                    console.log(err)
                })
        },
        // debug 改变游戏信息
        debug1() {
            //this.$store.commit('changeInfo')
            clearInterval(this.timeInter)
            this.timeInter = null
        },
        debug2() {
            this.request_gameinfo()
            console.log(this.acting)
        }
    },
    watch: {
        lastAction(newLastAction, oldLastAction) {
            if (oldLastAction == null) {
                return
            }
            if (newLastAction.user_id == oldLastAction.user_id && newLastAction.action_type == oldLastAction.action_type) {
                return
            }
            const self = this
            let user_id = newLastAction.user_id
            let user_name = ""
            let chip_cnt = -1
            let action_type = newLastAction.action_type
            let raise_num = newLastAction.raise_num
            let user = self.userInfos.find(user => user.seat_id === user_id)
            if (user) {
                user_name = user.user_name
                chip_cnt = user.chip_cnt
            }
            let popupSeat = -1
            let popupProps = null
            switch (action_type) {
                case 0: // 弃牌
                    popupProps = {
                        title: '弃牌',
                        titleColor: '#FFFFFF',
                        message: '',
                        messageColor: '#FFFFFF',
                        backgroundColor: '#F56C6C',
                        duration: 3000
                    }
                    if (user) {
                        if (self.seated) {
                            popupSeat = (user.seat_id - self.yourInfo.seat_id + 8) % 8 + 1
                        } else {
                            popupSeat = user.seat_id
                        }
                        store.commit('changeShowAction', user_id)
                    }
                    break
                case 1: // 跟注
                    popupProps = {
                        title: '跟注 ',
                        titleColor: '#FFFFFF',
                        message: `${chip_cnt}`,
                        messageColor: '#FFFFFF',
                        backgroundColor: '#409EFF',
                        duration: 3000
                    }
                    if (user) {
                        if (self.seated) {
                            popupSeat = (user.seat_id - self.yourInfo.seat_id + 8) % 8 + 1
                        } else {
                            popupSeat = user.seat_id
                        }
                        store.commit('changeShowAction', user_id)
                    }
                    break;
                case 2: // 加注
                    popupProps = {
                        title: '加注 ',
                        titleColor: '#FFFFFF',
                        message: `${chip_cnt}`,
                        messageColor: '#FFFFFF',
                        backgroundColor: '#67C23A',
                        duration: 3000
                    }
                    if (user) {
                        if (self.seated) {
                            popupSeat = (user.seat_id - self.yourInfo.seat_id + 8) % 8 + 1
                        } else {
                            popupSeat = user.seat_id
                        }
                        store.commit('changeShowAction', user_id)
                    }
                    break;
                case 3: // 新回合
                    popupProps = {
                        title: '进入阶段 ',
                        titleColor: '#FFFFFF',
                        message: '<< ' + self.term + ' >>',
                        messageColor: '#FFCC00',
                        backgroundColor: '#00000088',
                        duration: 3000
                    }
                    self.oldPodChipCount = self.$store.state.gameInfo.pod_info.pod_chip_cnt
                    store.commit('changeShowAction', -1)
                    break;
                case 4: // 结束
                    popupProps = {
                        title: '游戏结束 ',
                        titleColor: '#FFFFFF',
                        message: self.userInfos[user_id - 1].user_name + ' 获胜，筹码 +' + self.oldPodChipCount,
                        messageColor: '#FFCC00',
                        backgroundColor: '#00000088',
                        duration: 5000
                    }
                    self.oldPodChipCount = 0
                    store.commit('changeShowAction', -1)
                    break;
            }
            createSimplePopup(
                popupProps,
                popupSeat
            )
        }
    },
    mounted() {
        //this.$store.commit('enterRoom')
        document.body.style.overflow = "hidden"

        this.$store.commit('stand')

        this.request_gameinfo()

        this.timeInter = setInterval(() => {
            this.request_gameinfo()
        }, 1000)
    },
    unmounted() {
        document.body.style.overflow = "auto"
        clearInterval(this.timeInter)
        this.timeInter = null
        if (this.$store.state.inRoomId != 0) {
            this.exit_room({
                room_id: this.$store.state.inRoomId,
                user_name: this.$store.state.userName,
                force: true,
            })
        }
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
    position: fixed;
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

.spectate-state {
    display: flex;
    float: left;
    height: 30px;
    font-size: 16px;
    font-weight: bold;
    color: white;
    background: rgb(15, 115, 143);
    border-radius: 2px;
    margin-top: 5px;
    margin-left: 5px;
    padding-top: 3px;
    padding-left: 5px;
    padding-right: 5px;
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

@keyframes tip-animation {
0%{

}
100%{
    transform: translate(-10px,0px);
}
}

.sit-tip {
    color: yellow;
    font-size: 18px;
    margin-right: 20px;
    margin-top: 3px;
    animation: tip-animation 0.7s linear infinite alternate;
    -webkit-animation: tip-animation 0.7s linear infinite alternate;
}

.button-group2 {}

/* debug */
.debug {
    position: absolute;
    top: 100px;
    left: 10px;
}
</style>
      