<template>
    <div>
        <h1>{{ gameInfo.name }}</h1>
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
</template>

<script>
import sourceData from '../game-list.json'

import RoomListItem from '../components/RoomListItem.vue'
import CreateRoom from '../components/CreateRoom.vue'

export default {
    components:{ RoomListItem, CreateRoom },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id===parseInt(this.$route.params.id))
        }
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
}
</style>
