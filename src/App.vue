<script>
import Navigation from './components/Navigation.vue'

export default {
  components:{Navigation},
}

</script>

<template>

<Navigation v-if="!this.$store.state.isPlaying" />

<div class="container">
  <router-view></router-view>
</div>

</template>