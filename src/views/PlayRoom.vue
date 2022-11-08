<template>
<div class="play-room">
       <el-row>
        <el-col :span="20">
         <h6>
            Play Room: {{this.$route.params.room_id}}
         </h6>
        </el-col>
        <el-col :span="4">
         <el-button type="success" @click="sit" >坐下</el-button>
         <el-button type="warning" @click="stand">站起</el-button>
         <el-button type="info" @click="leave_room">离开房间</el-button>
        </el-col>
       </el-row>
    <el-container>
    <el-header height="120px">
      <el-row>
       <el-col :span="5">
        &nbsp;
       </el-col>
       <el-col :span="1">
       <el-avatar>小盲</el-avatar>
       <el-card>
        <span class="txt">95</span>
       </el-card>
       </el-col>
       <el-col :span="3">
        <div class="demo-image">
        <img :src="back0" alt="">
        <img :src="back0" alt="">
        </div>
       </el-col>
       <el-col :span="1">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <el-avatar>大盲</el-avatar>
        <el-card>
         <span class="txt">90</span>
        </el-card>
       </el-col>
       <el-col :span="3">
        <div class="demo-image">
        <img :src="back0" alt="">
        <img :src="back0" alt="">
        </div>
       </el-col>
       <el-col :span="1">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <el-avatar>玩家3</el-avatar>
        <el-card>
         <span class="txt">90</span>
        </el-card>
       </el-col>
       <el-col :span="3">
        <div class="demo-image">
        <img :src="back0" alt="">
        <img :src="back0" alt="">
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
        <el-avatar>玩家8</el-avatar>
        <el-card>
         <span class="txt">100</span>
        </el-card>
       </el-col>
       <el-col :span="3">
        <div class="demo-image">
        <img :src="back0" alt="">
        <img :src="back0" alt="">
        </div>
       </el-col>
       <el-col :span="10">
        &nbsp;
       </el-col>
       <el-col :span="1">
        <el-avatar>玩家4</el-avatar>
        <el-card>
         <span class="txt">90</span>
        </el-card>
       </el-col>
       <el-col :span="3">
        <div class="demo-image">
        <img :src="back0" alt="">
        <img :src="back0" alt="">
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
       <el-col :span="6">
          &nbsp;
       </el-col>
       <el-col :span="10">
        <div class="demo-image">
        <img :src="d8" alt="">
        <img :src="s8" alt="">
        <img :src="d9" alt="">
        <img :src="s9" alt="">
        <img :src="s10" alt="">
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
         <el-avatar>玩家7</el-avatar>
         <el-card>
          <span class="txt">100</span>
         </el-card>
        </el-col>
        <el-col :span="3">
         <div class="demo-image">
         <img :src="back0" alt="">
         <img :src="back0" alt="">
         </div>
        </el-col>
        <el-col :span="10">
         &nbsp;
        </el-col>
        <el-col :span="1">
         <el-avatar>玩家5</el-avatar>
         <el-card>
          <span class="txt">85</span>
         </el-card>
        </el-col>
        <el-col :span="3">
         <div class="demo-image">
         <img :src="back0" alt="">
         <img :src="back0" alt="">
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
      <el-avatar>玩家6</el-avatar>
      <el-card>
        <span class="txt">100</span>
      </el-card>
    </el-col>
    <el-col :span="3">
        <div class="demo-image">
        <img :src="d7" alt="">
        <img :src="s7" alt="">
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
  import back0 from "../assets/back.png"
  import d7 from "../assets/d7.png"
  import d8 from "../assets/d8.png"
  import d9 from "../assets/d9.png"
  import s7 from "../assets/s7.png"
  import s8 from "../assets/s8.png"
  import s9 from "../assets/s9.png"
  import s10 from "../assets/s10.png"
  import table0 from "../assets/table.jpg"
  import GameListItem from '../components/GameListItem.vue'
  
  export default {
    name: 'PlayRoom',
    components: {
      GameListItem
    },
    data(){
        return{
            back0: back0,
            d7: d7,
            d8: d8,
            d9: d9,
            s7: s7,
            s8: s8,
            s9: s9,
            s10: s10,
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
      },
      sit() {
      const self = this;
      var sit_data = {
       room_id:self.$route.params.room_id,
       user_name:self.$route.params.userName
      };
      request("sit", sit_data) 
        .then(function (res) {
          switch (res.succeed) {
            case true:
            this.$message.success('已坐下！');
            case false:
            console("sit err!");
            this.$message.error('发生错误！');
          }
        })
        .catch((err) => {
          console.log(err);
        });
        
    },
    stand() {
      const self = this;
      var stand_data = {
        room_id:self.$route.params.room_id,
       user_name:self.$route.params.userName
      };
      request("stand", stand_data) 
        .then(function (res) {
          console.log(res.data);
          switch (res.succeed) {
            case true:
            this.$message.success('已站起！');
            case false:
            this.$message.error('发生错误！');
            console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
        
    },
    exit_room() {
      const self = this;
      var exit_data = {
      room_id:self.$route.params.room_id,
      user_name:self.$route.params.userName
      };
      request("exit_room", exit_data)
        .then(function (res) {
          switch (res.succeed) {
            case true:
            this.$message.success('已退出房间！');
            this.$store.exitroom();
            router.back();
            case false:
            this.$message.error('发生错误！');
              console(succeed.message);
          }
        })
        .catch((err) => {
          console.log(err);
        });
        
    },
    },
    mounted() {
      //this.$store.commit('enterRoom')
    },
    unmounted(){
      this.$store.commit('exitRoom')
    },
    clicked() {
            createPopup(SimplePopup, {
                top: `${Math.random() * 80}%`,
                left: `${Math.random() * 80}%`
            }, {
                title: `${Math.round(Math.random() * 10)}`,
                message: `${Math.random()}`
            })
        }
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
  