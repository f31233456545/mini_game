<script>
import Navigation from './components/Navigation.vue'
import PlayRoom from './views/PlayRoom.vue'

export default {
  components:{Navigation, PlayRoom},
}

</script>

<template>

<Navigation v-if="this.$store.state.inRoomId==0" />

<div class="container" v-if="this.$store.state.inRoomId==0">
  <router-view></router-view>
</div>

<div class="playroom-container" v-else>
  <router-view></router-view>
</div>

</template>