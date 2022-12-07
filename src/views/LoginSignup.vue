<template>
  <Navigation />
  <div class="container">
    <div class="login-signup-wrapper">
      <div class="menu-wrapper">
        <el-menu class="login-signup-menu" mode="horizontal" background-color="#434a50" text-color="white" active-text-color="#ffd04b">
          <el-menu-item v-if="islogin">登录</el-menu-item>
          <el-menu-item v-else>注册</el-menu-item>
        </el-menu>
      </div>
      <div class="form-section" v-if="islogin">
        <el-form label-position="top" label-width="100px" >
          <el-form-item props="name">
            <el-input type="text" placeholder="用户名" v-model="rulesForm.username"></el-input>
          </el-form-item>
          <el-form-item props="password">
            <el-input type="password" placeholder="密码" v-model="rulesForm.password" class="demo-ruleForm" :rules="rules" :model="rulesForm" ref="ruleForm"></el-input>
            <span class="errTips" v-if="error">*用户名或密码错误！</span>
          </el-form-item>
          <el-form-item>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="login()">登录</el-button>
            </div>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="changeType">立即注册</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
      <div class="form-section" v-else>
        <el-form label-position="top" label-width="100px" class="demo-ruleForm" :rules="rules" status-icon ref="ruleForm">
          <el-form-item props="name">

            <el-input type="text" placeholder="用户名" v-model="rulesForm.username"></el-input>
          </el-form-item>
          <el-form-item props="password">
            <el-input type="password" placeholder="密码" v-model="rulesForm.password"></el-input>
            <span class="errTips" v-if="existed">*用户名已经存在！</span>
          </el-form-item>
          <el-form-item>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="register()">注册</el-button>
            </div>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="changeType"> 马上登录</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
    
<script>
import Navigation from "../components/Navigation.vue";
import { request } from "../utils/request.js";
import store from "../store/index.js";
import router from "../router/index.js";
export default {
  components: { Navigation },
  data() {
    return {
      islogin: true, //当前界面：true：登录 false：注册
      error: false, //用户名或密码是否错误
      existed: false, //用户名是否已被注册
      clickState:false,
      rulesForm: {
        username: "",
        password: "",
      },
    };
  },
  created() {
    this.keyupSubmit();
  },
  methods: {
    keyupSubmit() {
      document.onkeydown = (e) => {
        let _key = window.event.keyCode;
        if (_key === 13 && !this.clickState) {
          this.clickState=true;
          if (this.islogin == true) this.login();
          else this.register();
          setTimeout(() => {
                  this.clickState = false;
                }, 3000);
        }
      };
    },
    //登录/注册界面切换
    changeType() {
      this.islogin = !this.islogin;
    },
    //用户登录
    login() {
      const self = this;
      if (self.rulesForm.username != "" && self.rulesForm.password != "") {
        request("login", self.rulesForm)
          .then(function (res) {
            console.log(res.succeed);
            switch (res.succeed) {
              case true:
                self.$message.success("登录成功！");
                store.commit("login", self.rulesForm.username);
                router.back();
                break;
              case false:
                self.error = true;
                setTimeout(() => {
                  self.error = false;
                }, 2000);
                break;
            }
          })
          .catch((err) => {
            console.log(err); //代码错误、请求失败捕获
          });
      } else {
        self.$message.error("请填写用户名和密码！");
      }
    },
    //用户注册
    register() {
      const self = this;
      if (self.rulesForm.username != "" && self.rulesForm.password != "") {
        request("register", self.rulesForm)
          .then(function (res) {
            switch (res.succeed) {
              case true:
                self.$message.success("注册成功！正在登录，请稍后...");
                self.login();
                break;
              case false:
                self.existed = true;
                setTimeout(() => {
                  self.existed = false;
                }, 2000);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } else {
        self.$message.error("填写不能为空！");
      }
    },
  },
  mounted() {},
};
</script>

<style lan="css">
.login-signup-wrapper {
  width: 100%;
}
.menu-wrapper {
  width: 400px;
  margin: 0 auto;
}
.form-section {
  width: 400px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 6px;
  background: #434a50;
  position: relative;
  top: -7px;
}
.button-wrapper {
  margin: 0 auto;
  padding-top: 10px;
}
.button {
  width: 200px;
}
.errTips {
  color: white;
}
</style>

