<template>
    <div class="login-signup-wrapper">
        <div class="menu-wrapper">
            <el-menu
                :default-active="activeIndex"
                class="login-signup-menu"
                mode="horizontal"
                background-color="#434a50"
                text-color="white"
                active-text-color="#ffd04b"
                @select="handleSelect"
            >
                <el-menu-item index="1">登录</el-menu-item>
                <el-menu-item index="2">注册</el-menu-item>
            </el-menu>
        </div>
        <div class="form-section">
            <el-form
                label-position="top" label-width="100px" class="demo-ruleForm"
                :rules="rules"
                :model="rulesForm"
                status-icon
                ref="ruleForm"
            >
                <el-form-item props="name">
                    <el-input type="text" placeholder="用户名" v-model="rulesForm.name"></el-input>
                </el-form-item>
                <el-form-item props="password">
                    <el-input type="password" placeholder="密码" v-model="rulesForm.password"></el-input>
                </el-form-item>
                <el-form-item>
                    <div class="button-wrapper">
                        <el-button class="button" type="primary" @click="submitForm('ruleForm')">
                            {{this.activeIndex=="1"?"登录":"注册"}}
                        </el-button>
                    </div>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default{
    data(){
        return{
            rulesForm:{
                name:'',
                password:''
            },
            rules:{
                name:[
                    {required:true,message:"请输入名字",trigger:"blur"},
                    {min:1,max:12,message:"长度1-12",trigger:"blur"}
                ],
                password:[
                    {required:true,message:"请输入密码",trigger:"blur"},
                    {min:6,max:20,message:"长度6-20",trigger:"blur"}
                ],
            },
            activeIndex:'1'
        }
    },
    methods:{
        handleSelect(index){
            this.activeIndex=index
        },
        submitForm(ruleForm){
            this.$store.commit('login')
            this.$router.push('/games')
        }
    }
}
</script>

<style lan="css">
.login-signup-wrapper{
    width: 100%;
}
.menu-wrapper{
    width: 400px;
    margin: 0 auto;
}
.form-section{
    width: 400px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 6px;
    background: #434a50;
    position: relative;
    top: -7px;
}
.button-wrapper{
    margin: 0 auto;
    padding-top: 10px;
}
.button{
    width: 200px;
}
</style>