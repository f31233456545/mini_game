<template>
    <div class="create-room">
        <h1>
            Create Room: {{this.gameInfo.name}}
        </h1>
    </div>
</template>

<script>
export default {
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id === parseInt(this.$route.params.id))
        }
    }
}
</script>