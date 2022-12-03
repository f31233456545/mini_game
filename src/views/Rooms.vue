<template>
    <Navigation />
    <div class="container">

        <div class="header-wrapper">
            <h1 class="room-list-header">{{ gameInfo.name }} rooms</h1>
            <div class="update-wrapper">
                <button class="update-button" @click="update()">
                    <img src="../assets/icons/update.svg" />
                    <div class="update-hint"><span>刷新房间列表</span></div>
                </button>
            </div>
            <JoinRoom class="join-room-wrapper" />
        </div>

        <div class="room-list-wrapper">
            <div class="room-list">
                <CreateRoom class="create-room-wrapper" />
                <RoomListItem v-for="item in gameInfo.rooms" :key="item.room_id" :room_id="item.room_id"
                    :room_name="item.room_name" :player_num="item.player_num" :viewer_num="item.viewer_num"
                    :max_player_num="item.max_num" :status="item.status" :gameId="gameInfo.id" />
            </div>
        </div>

    </div>
</template>

<script>
import sourceData from '../game-list.json'

import RoomListItem from '../components/RoomListItem.vue'
import CreateRoom from '../components/CreateRoom.vue'
import Navigation from '../components/Navigation.vue'
import JoinRoom from '../components/JoinRoom.vue'
import { request } from '../utils/request.js'

export default {
    components: { RoomListItem, CreateRoom, Navigation, JoinRoom },
    data(){
        return {
            timeInter: null, // 定时器，mount时设定
        }
    },
    computed: {
        gameInfo() {
            return this.$store.state.games.find(gameInfo => gameInfo.id === parseInt(this.$route.params.id))
        }
    },
    methods: {
        // update(){
        //     this.$store.dispatch('updateRoomList',this.gameInfo.id)
        // },
        update(useloading=true) {
            var params = { game_kind: this.gameInfo.id, user_name: this.$store.state.userName }
            request('request_room_list', params, useloading)
                .then(data => {
                    this.$store.commit('updateRoomListInfo', { gameId: this.gameInfo.id, list: data.rooms })
                    console.log(data)
                })
                .catch(function (error) { // 请求失败处理
                    alert("request failed!")
                    console.log("request failed!")
                    console.log(error);
                })
        }
    },
    mounted() {
        this.$store.commit('setGameId', this.gameInfo.id)
        this.update(false)
        this.timeInter = setInterval(() => {
            this.update(false)
        }, 10000) // 10s自动刷新一次房间列表
    },
    unmounted() {
        clearInterval(this.timeInter)
        this.timeInter = null
    }
}

</script>

<style lan="css">
.room-list-wrapper {
    max-width: 960px;
}

.room-list {
    max-width: 960px;
    flex-wrap: wrap;
    margin: 0 auto;
    margin-top: 5px;
}

.update-wrapper {
    float: left;
}

.update-button {
    position: relative;
    width: 50px;
    height: 50px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    margin-top: 21px;
    margin-left: 20px;
}

.update-hint {
    position: absolute;
    width: 50px;
    height: 50px;
    top: 0px;
    left: 0px;
}

.update-hint span{
    display: none;
}

.update-hint:hover span{
    position: relative;
    top: 20px;
    left: 40px;
    display: block;
    width: 100px;
    height: 20px;
    background: rgb(250,250,220);
    color: rgb(50,50,50);
}

.update-button:hover {
    transform: scale(1.02);
}

.join-room-wrapper {
    margin-top: 21px;
    margin-bottom: 20px;
    float: right;
}

.create-room-wrapper {
    float: left;
}

.room-list-header {
    float: left;
}

.header-wrapper {
    width: 100%;
    height: 85px;
}

</style>
