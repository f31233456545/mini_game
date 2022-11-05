<template>
<div class="play-room">
       <el-row>
        <el-col :span="20">
         <h6>
            Play Room: {{this.$route.params.room_id}}
         </h6>
        </el-col>
        <el-col :span="4">
         <el-button type="success">坐下</el-button>
         <el-button type="warning">站起</el-button>
         <el-button type="info">离开房间</el-button>
        </el-col>
       </el-row>
    <el-container>
    <el-header height="120px">
      <el-row>
       <el-col :span="5">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <user  v-for="item in gameInfo.users.slice(0,1)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
       </el-col>
       <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="13"/>
     <card :open="true" :num="15"/>
     </el-row>
     </div>
       </el-col>
       <el-col :span="1">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <user  v-for="item in gameInfo.users.slice(1,2)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
       </el-col>
       <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="16"/>
     <card :open="true" :num="8"/>
     </el-row>
     </div>
       </el-col>
       <el-col :span="1">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <user  v-for="item in gameInfo.users.slice(2,3)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
       </el-col>
       <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="3"/>
     <card :open="true" :num="7"/>
     </el-row>
     </div>
       </el-col>
       <el-col :span="5">
        &nbsp;
       </el-col>
      </el-row>
    </el-header>
    <el-footer height="130px">
      <el-row>
       <el-col :span="3">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <user  v-for="item in gameInfo.users.slice(7,8)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
       </el-col>
       <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="1"/>
     <card :open="true" :num="19"/>
     </el-row>
     </div>
       </el-col>
       <el-col :span="10">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <user  v-for="item in gameInfo.users.slice(3,4)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
       </el-col>
       <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="50"/>
     <card :open="true" :num="42"/>
     </el-row>
     </div>
       </el-col>
       <el-col :span="5">
        &nbsp;
       </el-col>
      </el-row>
    </el-footer>
    </el-container>
    <el-container>
    <el-header height="130px">
      <el-row>
       <el-col :span="9">
          &nbsp;
       </el-col>
       <el-col :span="7">
        <div class="tablecard">
        <el-row>
        <card :open="true" :num="1"/>
        <card :open="true" :num="11"/>
        <card :open="true" :num="26"/>
        <card :open="true" :num="36"/>
        <card :open="true" :num="31"/>
        </el-row>
        </div>
       </el-col>
       <el-col :span="8">
        <el-descriptions title="" :column="1" style="width:200px" border>
        <el-descriptions-item label="底池">50</el-descriptions-item>
        <el-descriptions-item label="前注">15</el-descriptions-item>
        </el-descriptions>
       </el-col>
      </el-row>
    </el-header>
    <el-footer height="120px">
      <el-row>
        <el-col :span="3">
         &nbsp;
        </el-col>
        <el-col :span="1">
          <user  v-for="item in gameInfo.users.slice(6,7)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
        </el-col>
        <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="48"/>
     <card :open="true" :num="38"/>
     </el-row>
     </div>
        </el-col>
        <el-col :span="10">
         &nbsp;
        </el-col>
        <el-col :span="1">
          <user  v-for="item in gameInfo.users.slice(4,5)"
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
        </el-col>
        <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="25"/>
     <card :open="true" :num="37"/>
     </el-row>
     </div>
        </el-col>
        <el-col :span="3">
         &nbsp;
        </el-col>
       </el-row>
    </el-footer>
    </el-container>
  <el-container>
  <el-footer height="105px">
   <el-row>
    <el-col :span="10">
      &nbsp;
    </el-col>
    <el-col :span="1">
    <user  v-for="item in gameInfo.users.slice(5,6)" 
                :key="item.user_num"
                :user_num="item.user_num"
                :user_name="item.user_name"
                :user_status="item.user_status"
                :user_action="item.user_action"
                :user_money="item.user_money"
                :user_bet="item.user_bet"
                />
    </el-col>
    <el-col :span="3">
     <div class="handcard">
     <el-row>
     <card :open="true" :num="51"/>
     <card :open="true" :num="52"/>
     </el-row>
     </div>
    </el-col>
    <el-col :span="10">
     &nbsp;
     <el-button
      plain
      @click="open2">
      当前下注情况
      </el-button>
    </el-col>
   </el-row>
  </el-footer>
  </el-container>
  <el-row>
    <el-col :span="10">
        &nbsp;
    </el-col>
    <el-col :span="14">
     <el-button type="success">加注</el-button>
     <el-button type="primary">跟注/过牌</el-button>
     <el-button type="danger">弃牌</el-button>
    </el-col>
  </el-row>
</div>
</template>
  
  <script>

  import table0 from "../assets/table.jpg"
  import GameListItem from '../components/GameListItem.vue'
  import User from './User.vue'
  import Card from './Card.vue'
  
  export default {
    name: 'PlayRoom',
    components: {
      GameListItem,
      User,
      Card
    },
    data(){
        return{

            table0: table0,
        };

    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === parseInt(this.$route.params.id))
        }
    },
    props: {
      room_id: Number,
    },
    methods: {
      open2() {
        this.$notify({
          title: '操作提示',
          message: '玩家5加注15,玩家6开始操作',
          duration: 0,
          offset: 100
        });
      }
    },
    mounted() {
      //this.$store.commit('enterRoom')
    },
    unmounted(){
      this.$store.commit('exitRoom')
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
    position: absolute;
  }
  .el-header {
    color: #333;
    text-align: center;
  }
  .el-footer {
    color: #333;
    text-align: center;
    padding: 0;
  }
  .el-card{
    background-color: bisque;
    color:blue;
    width: 60px;
    height: 50px;
  }
  </style>
  