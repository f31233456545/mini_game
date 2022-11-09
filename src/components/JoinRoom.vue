<template>
    <div class="join-room">
        <el-input class="join-room-input-box" v-model="this.room_id" oninput="value=value.replace(/[^\d]/g, '')" maxlength="15" placeholder="Enter room ID here" />
        <el-button class="join-room-button" type="primary" @click="join_room">
            Join Room
        </el-button>
    </div>
</template>

<script>
import { isInteger } from 'lodash';
import { request } from '../utils/request';

export default {
    data() {
        return {
            room_id: "",
        }
    },
    computed: {
        gameInfo() {
            return this.$store.state.games.find(gameInfo => gameInfo.id === parseInt(this.$route.params.id))
        }
    },
    methods: {
        join_room() {
            const self = this;  // 组件自身
            if (this.$store.state.login == false) {
                self.$message.error('请先登录')
                self.$router.push('/login-signup')
                return
            }
            if(self.room_name == ""){
                self.$message.error('请输入房间号')
                return
            }
            request('join_room', {
                room_id: parseInt(self.room_id),
                user_name: self.$store.state.userName,
            })
                .then(function (response) {  // 等待请求返回
                    if (response.succeed == true) {
                        self.$store.commit("enterRoom", self.room_id)
                        console.log(`joined room ${self.$store.state.inRoomId}`);
                        self.$router.push(`${self.$route.path}/content/${self.$store.state.inRoomId}`);
                        return;
                    }
                    else {
                        console.log("join failed!");
                        console.log(response);
                        return;
                    }
                })
                .catch(function (error) {
                    console.log("request failed!");
                    console.log(error);
                });
        }
    }
}
</script>

<style lan="css">
.join-room {
    height: auto;
    width: 480px;
    background: #434a50;
    border-radius: 6px;
    padding: 10px 8px;
}

.join-room-input-box {
    width: 300px;
    font-size: 24px;
}

.join-room-button {
    margin-left: 10px;
    width: 150px;
    font-size: 24px;
}
</style>