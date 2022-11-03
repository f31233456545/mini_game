<template>
    <div class="user">
    
       <el-avatar>{{user_name}}</el-avatar>
       <el-card>
        <span class="txt">{{user_money}}</span>
       </el-card>
    
    </div>
  </template>
<script>
export default{
    props:{
        user_name: String,
        user_num: Number,
        user_status: Number,
        user_action: Number,
        user_money: Number,
        user_bet: Number,
        gameId: Number,
        type: String,
    },
    computed:{
      gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === this.gameId)
        }
    },
}
</script>
<style scoped>
 .el-card{
    background-color: bisque;
    color:blue;
    width: 60px;
    height: 50px;
  }
</style>