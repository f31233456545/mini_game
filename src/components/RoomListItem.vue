<template>
    <div class="room">
        <div class="room-id">{{this.room_id}}</div>
        <div class="room-name">{{this.room_name}}</div>
        <div class="state">
            <div class="player-num">
                <img src="../assets/icons/user-regular.svg" />
                <div>{{this.player_num}}/{{this.max_player_num}}</div>
            </div>
            <div class="status">
                <div v-if="this.status==0">
                    <img src="../assets/icons/cafe.svg" />
                    waiting...
                </div>
                <div v-else>
                    <img src="../assets/icons/dice.svg" />
                    playing...
                </div>
                <!-- {{this.status==0?"waiting...":"playing..."}} -->
            </div>
        </div>
        <div class="room-button-wrapper">
            <el-button class="room-button" type="primary" @click="join_room">Join</el-button>
        </div>
    </div>
</template>

<script>
import { resolveComponent } from "vue"
import routes from "../router/index.js"
import { request } from '../utils/request.js'

export default{
    props:{
        room_id: Number,
        room_name: String,
        player_num: Number,
        max_player_num: Number,
        status: Number,
        gameId: Number,
    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === this.gameId)
        }
    },
    methods: {
        join_room() {
            var self = this;  // 组件自身
            if(this.$store.state.login == false){
                alert('请先登录')
                self.$router.push('/login-signup')
                return
            }
            request('join_room', {
                room_id: self.room_id,
                user_name: self.$store.state.userName,
            })
            .then(function (response) {  // 等待请求返回
                if (response.succeed == true)
                {
                    self.$store.commit("enterRoom", self.room_id)
                    console.log(`joined room ${self.$store.state.inRoomId}`);
                    self.$router.push(`${self.$route.path}/content/${self.$store.state.inRoomId}`);
                    return
                }
                else
                {
                    console.log("join failed!");
                    console.log(response);
                    return
                }
            })
            .catch(function (error) {
                console.log("request failed!");
                console.log(error);
            })
        }
    }
}
// "`/${this.gameInfo.id}/${this.gameInfo.name}`"
</script>

<style lan="css">
.room{
    float: left;
    height: 250px;
    width: 200px;
    text-align: center;
    /* border-style: solid;
    border-color: black; */
    background: #434a50;
    border-radius: 6px;
    margin: 20px;
    position: relative;
}
.room:hover{
    transform: scale(1.05);
}
.room-id{
    padding-top: 3px;
    font-size: 1.5rem;
    color: white;
}
.room-name{
    padding: 3px;
    font-size: 1.5rem;
    background: #eee;
}
.state{
    height: 140px;
    /* border-style: dotted;
    border-color: black; */
    background: #eee;
    padding-top: 30px;
}
.player-num{
    font-size: 2.5rem;
    padding: 10px;
    display: flex;
}
.player-num img{
    padding-left: 30px;
    padding-right: 10px;
}
.status{
    font-size: 1.2rem;
    padding: 4px;
}
.room-button-wrapper{
    padding: 5px;
}
.room-button{
    width: 140px;
    font-size: 1.2rem;
}

</style>