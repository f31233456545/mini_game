<template>

<div id="nav">
  <div class="nav-wrapper">
    <div class="menu left">
        <router-link class="logo" to='/'>MiniFun</router-link>
    </div>

    <div class="menu right">
        <router-link class="menu-item" to='/login-signup' v-if="!this.$store.state.login">Login/Sign Up</router-link>
        <div v-else>
          <router-link class="user" to='/user-info'>
            <img src="../assets/icons/user-circle.svg" />
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
    }
  }
}
</script>

<style lan="css">

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

.user {
    font-size: 1.2rem;
    position: absolute;
    top: -2px;
}

.logout {
    margin-left: 40px;
    cursor: pointer;
}
</style>