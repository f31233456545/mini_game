<template>
    <div class="room">
         <div class="content" v-if="this.type=='normal'">
            <div class="room-id">{{this.room_id}}</div>
            <div class="room-name">{{this.room_name}}</div>
            <div class="state">
                <div class="player-num">
                    {{this.player_num}}/{{this.max_player_num}}
                </div>
                <div class="status">
                    {{this.status==0?"waiting...":"playing..."}}
                </div>
            </div>
            <div class="room-button-wrapper">
            <router-link :to="`${this.$route.path}/content/${this.room_id}`">
                <el-button class="room-button" type="primary">Join</el-button>
            </router-link>
            </div> 
         </div>
        <router-link :to="`${this.$route.path}/create`" v-else>
            <div class="create">
                <div class="create-tag">Create</div>
                <div class="create-icon">+</div>
            </div>
        </router-link>
    </div>
</template>

<script>
export default{
    props:{
        room_id: Number,
        room_name: String,
        player_num: Number,
        max_player_num: Number,
        status: Number,
        gameId: Number,
        type: String,
    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === this.gameId)
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

.create{
    margin: 0 auto;
    font-size: 1.5rem;
    height: 100%;
    background: #eee;
    border-radius: 6px;
}
.create-tag{
    padding-top: 3px;
    font-size: 1.5rem;
    background: #434a50;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: white;
}
.create-icon{
    position: absolute;
    top: 60px;
    font-size: 8.0rem;
    width: 100%;
    color: #636a70;
}
</style>