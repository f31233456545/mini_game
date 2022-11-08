<template>
  <Navigation />
  <div class="container">
    <div class="login-signup-wrapper">
      <div class="menu-wrapper">
        <el-menu class="login-signup-menu" mode="horizontal" background-color="#434a50" text-color="white" active-text-color="#ffd04b">
          <el-menu-item v-if="!islogin">登录</el-menu-item>
          <el-menu-item v-else>注册</el-menu-item>
        </el-menu>
      </div>
      <div class="form-section" v-if="!islogin">
        <el-form label-position="top" label-width="100px" class="demo-ruleForm" :rules="rules" :model="rulesForm" status-icon ref="ruleForm">
          <el-form-item props="name">
            <el-input type="text" placeholder="用户名" v-model="rulesForm.name"></el-input>
          </el-form-item>
          <el-form-item props="password">
            <el-input type="password" placeholder="密码" v-model="rulesForm.password"></el-input>
            <span class="errTips" v-if="error">*用户名或密码错误！</span>
          </el-form-item>
          <el-form-item>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="login">登录</el-button>
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
            <el-input type="text" placeholder="用户名" v-model="rulesForm.name"></el-input>
            <span class="errTips" v-if="existed">*用户名已经存在！</span>
          </el-form-item>
          <el-form-item props="password">
            <el-input type="password" placeholder="密码" v-model="rulesForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <div class="button-wrapper">
              <el-button class="button" type="primary" @click="register">注册</el-button>
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
      islogin: false, //当前界面：false：登录 true：注册
      error: false, //用户名或密码是否错误
      existed: false, //用户名是否已被注册
      rulesForm: {
        islogin: true,
        name: "",
        password: "",
      },
    };
  },
  methods: {
    //登录/注册界面切换
    changeType() {
      (this.islogin = !this.islogin),
        (this.rulesForm.name = ""),
        (this.rulesForm.password = "");
    },
    //用户登录
    login() {
      const self = this;
      var LoginData = {
        name: self.rulesForm.name,
        password: self.rulesForm.password,
      };
      if (self.rulesForm.name != "" && self.rulesForm.password != "") {
        //axios.post('http://47.94.92.103:3005/login',LoginData)
        request("login", LoginData)
          .then(function (res) {
            console.log(res.succeed);
            switch (res.succeed) {
              case true:
                self.$message.success('登陆成功！');
                store.commit("login", LoginData.name);
                //router.push('/');
                router.back();
                break;
              case false:
                self.error = true;
                break;
            }
          })
          .catch((err) => {
            console.log(err); //代码错误、请求失败捕获
          });
      } else {
        this.$message.error('请填写用户名和密码！');
      }
      },
    //用户注册
    register() {
      const self = this;
      var LoginData = {
        name: self.rulesForm.name,
        password: self.rulesForm.password,
      };
      if (self.rulesForm.name != "" && self.rulesForm.password != "") {
        //axios.post('http://47.94.92.103:3005/register',LoginData)
        request("register", LoginData)
          .then(function (res) {
            switch (res.succeed) {
              case true:
                  self.$message.success('注册成功！');
                  self.$message.success('正在登陆，请稍后...');
                self.login();
                break;
              case false:
                self.existed = true;
            }
          })
          .catch((err) => {
            console.log(err); //代码错误、请求失败捕获
          });
      } else {
        this.$message.error("填写不能为空！");
      }
    },
  },
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
</style>

