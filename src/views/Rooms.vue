<template>
    <Navigation />
    <div class="container" >

        <div class="header-wrapper">
            <h1 class="room-list-header">{{gameInfo.name}} rooms</h1>
            <div class="update-wrapper">
                <button class="update-button" @click="update()"><img src="../assets/icons/update.svg"/></button>
            </div>
        </div>

        <div class="room-list-wrapper">
            <div class="room-list">
                <CreateRoom />
                <RoomListItem
                    v-for="item in gameInfo.rooms"
                    :key="item.room_id"
                    :room_id="item.room_id"
                    :room_name="item.room_name"
                    :player_num="item.player_num"
                    :max_player_num="item.max_player_num"
                    :status="item.status"
                    :gameId="gameInfo.id"
                />
            </div>
        </div>
        
    </div>
</template>

<script>
import sourceData from '../game-list.json'

import RoomListItem from '../components/RoomListItem.vue'
import CreateRoom from '../components/CreateRoom.vue'
import Navigation from '../components/Navigation.vue'
import { request } from '../utils/request.js'

export default {
    components:{ RoomListItem, CreateRoom, Navigation },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id===parseInt(this.$route.params.id))
        }
    },
    methods:{
        // update(){
        //     this.$store.dispatch('updateRoomList',this.gameInfo.id)
        // },
        update() {
            var params = {game_kind: this.gameInfo.id, user_name: this.$store.state.userName}
            request('request_room_list', params)
                .then(data => {
                    if(!data){
                        return
                    }
                    this.$store.commit('updateRoomListInfo', {gameId:this.gameInfo.id, list:data})
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    },
    mounted(){
        this.update()
    }
}
</script>

<style lan="css">
.room-list-wrapper{
    max-width: 960px;
}
.room-list{
    max-width: 960px;
    flex-wrap: wrap;
    margin: 0 auto;
    margin-top: 5px;
}

.update-wrapper{
    float: left;
}
.update-button{
    width: 50px;
    height: 50px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    margin-top: 21px;
    margin-left: 20px;
}
.update-button:hover{
    transform: scale(1.02);
}

.room-list-header{
    float: left;
}

.header-wrapper{
    width: 100%;
    height: 85px;
}
</style>
