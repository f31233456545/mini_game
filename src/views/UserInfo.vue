<template>
  <Navigation/>
  <div class="container">
    <div class="user-info">
      <h1>User Information</h1>
      <p class="user-name">username: {{this.$store.state.userName}}</p>
    </div>
  </div>
</template>

<script>
import Navigation from '../components/Navigation.vue'
export default {
  components: { Navigation },
}
</script>

<style scoped>
.user-name {
  font-size: 1.5rem;
}
</style>
