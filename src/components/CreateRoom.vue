<template>
    <div class="create-room">
        <el-input
            class="create-room-input-box"
            v-model="this.room_name"
            placeholder="Enter new room name here"
            maxlength="20"
        />
        <span class="create-room-radios">
            <input
                type="radio"
                value="private"
                v-model="room_privacy"
            />
            Private
            <input
                type="radio"
                value="public"
                v-model="room_privacy"
            />
            Public
        </span>
        <el-button
            class="create-room-button"
            type="primary"
            @click="create_room">
            Create Room
        </el-button>
    </div>
</template>

<script>
import { request } from '../utils/request';

export default {
    data() {
        return {
            room_name: "",
            room_privacy: "private",
        }
    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id===parseInt(this.$route.params.id))
        }
    },
    methods: {
        create_room() {
            var self = this;  // 组件自身
            request("create_room", {
                private: (self.room_privacy == "private"),
                room_name: self.room_name,
                game_kind: self.gameInfo.id,
                creator_name: self.$store.state.userName
            })
            .then(function (response) {
                if (response.succeed == true)
                {
                    console.log("create succeed!");
                    self.join_room(response.room_id);
                    return;
                }
                else
                {
                    console.log("create failed!");
                    console.log(response)
                }
            })
            .catch(function (error) {
                console.log("request failed!");
                console.log(error);
            });
        },
        join_room(room_id) {
            var self = this;  // 组件自身
            if(this.$store.state.login == false){
                alert('请先登录')
                self.$router.push('/login-signup')
                return
            }
            request('join_room', {
                room_id: room_id,
                user_name: self.$store.state.userName,
            })
            .then(function (response) {  // 等待请求返回
                if (response.succeed == true)
                {
                    self.$store.commit("enterRoom", room_id)
                    console.log(`joined room ${self.$store.state.inRoomId}`);
                    self.$router.push(`${self.$route.path}/content/${self.$store.state.inRoomId}`);
                    return;
                }
                else
                {
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
.create-room {
    height: auto;
    width: 960px;
    background: #434a50;
    border-radius: 6px;
    padding: 10px 8px;
}
.create-room-input-box {
    width: 55%;
    font-size: 24px;
}
.create-room-radios {
    width: auto;
    font-size: 24px;
    color: white;
    vertical-align: middle;
    margin-left: 10px;
    margin-right: 10px;
}
.create-room-button {
    width: 20%;
    font-size: 24px;
}
</style>