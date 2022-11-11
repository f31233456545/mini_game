<template>
    <Navigation />
    <div class="container" >

        <div>
            <h1>Games</h1>
        </div>

        <div class="game-list-wrapper">
            <div class="game-list">
                <GameListItem
                    v-for="item in games"
                    :key="item.id"
                    :id="item.id"
                    :name="item.name"
                    :img="item.img"
                />
            </div>
        </div>
        
    </div>
</template>

<script>
import GameListItem from '../components/GameListItem.vue'
import Navigation from '../components/Navigation.vue'

export default {
    components:{GameListItem, Navigation},
    data(){
        return{
            games: this.$store.state.games
        }
    },
    mounted(){
        this.$store.commit('setGameId',-1)
    }
}
</script>

<style lan="css">
.game-list-wrapper{
    width: 100%;
}
.game-list{
    max-width: 960px;
    margin: 0 auto;
}
</style>