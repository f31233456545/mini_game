<template>

<div id="nav">
  <div class="nav-wrapper">
    <div class="menu left">
        <router-link class="logo" to='/'>MiniFun</router-link>
    </div>

    <div class="menu right">
        <router-link class="menu-item" to='/login-signup' v-if="!this.$store.state.login">Login/Sign Up</router-link>
        <div v-else class="user-and-logout">
          <router-link class="menu-item user" to='/user-info'>
            <img class="user-icon" src="../assets/icons/user-circle.svg"/>
            <div class="user-name">{{this.$store.state.userName}}</div>
          </router-link>
          <a class="menu-item logout" @click="logout">Logout</a>
        </div>
        
    </div>
  </div>

</div>

</template>

<script>
export default {
  methods:{
    logout(){
      this.$store.commit('logout')
      if(this.$route.path=='/user-info'){
        this.$router.back()
      }
    }
  }
}
</script>

<style lan="css" scoped>

/* Navigation */
#nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  margin-top: 0;
  padding: 20px;
  background: #434a50;
  color: white;
  display: flex;
  align-items: center;
  border-bottom: 5px solid #636a70;
  z-index: 2;
}

#nav a {
  /* display: inline-block; */
  margin-right: 15px;
  color: white;
  opacity: 0.85;
  transition: 0.2 ease color;
  /* font-size: 1.0rem; */
}

#nav a:hover {
  opacity: 1;
}

#nav .active-link{
    color: #ffb600;
}

#logo {
  font-weight: bold;
  font-size: 1.5rem !important;
  opacity: 1 !important;
  /* position: relative;
  top: -5px; */
}

.nav-wrapper {
    width: 100%;
}

.menu {    
    display: flex;
    height: 22.5px;
}

.left {
    float: left;
}

.right {
    float: right;
    position: relative;
}

.menu-item {
    display: inline-block;
    padding: 2px;
    font-size: 1.2rem;
}

.logo {
    display: inline-block;
    padding: 2px;
    font-weight: bold;
    font-size: 1.5rem !important;
    opacity: 1;
    position: relative;
    top: -4px;
}

.user-and-logout {
    display: flex;
}

.user {
    font-size: 1.2rem;
    position: relative;
    top: 0px;
    width: 90px;
    height: 25px;
    display: flex;
    background: rgb(70,90,120);
    border-radius: 4px;
    padding: 2px;
}

.user-icon {
  width: 22.5px;
  height: 22.5px;
}

.user-name {
    width: 60px;
    height: 22.5px;
    overflow: hidden;
    text-overflow: ellipsis;
}

.logout {
    margin-left: 0px;
    cursor: pointer;
}
</style>