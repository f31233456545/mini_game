<template>
    <div class="room">
        <div class="content" v-if="this.type=='normal'">
            <div class="room-id">{{id}}</div>
            <div class="room-name">xxx's room</div>
            <div class="state">
                State
            </div>
            <div class="room-button-wrapper">
                <el-button class="room-button" type="primary">Join</el-button>
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
        id: Number,
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
    border-style: solid;
    border-color: black;
    margin: 20px;
    position: relative;
}
.room-id{
    padding-top: 3px;
    font-size: 1.5rem;
}
.room-name{
    padding: 3px;
    font-size: 1.5rem;
}
.state{
    height: 140px;
    border-style: dotted;
    border-color: black;
}
.room-button-wrapper{
    padding: 5px;
}
.room-button{
    width: 100px;
}

.create{
    margin: 0 auto;
    font-size: 1.5rem;
    height: 100%;
}
.create-tag{
    padding-top: 3px;
    font-size: 1.5rem;
}
.create-icon{
    position: absolute;
    top: 50px;
    font-size: 8.0rem;
    width: 100%;
    color: #636a70;
}
</style>