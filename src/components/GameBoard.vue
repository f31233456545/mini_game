<template>
    <div class="gameboard">
        <div class="gameboard-container">
            <div class="term">
                {{term}}
            </div>
            <div class="cards">
                <Card
                v-for="i in podInfo.pokes"
                :value="i"
                />
            </div>
            <div class="chips">
                <img class="chip-icon" src="../assets/icons/chip.png"/>
                <div class="chip-num">
                    {{podInfo.pod_chip_cnt}}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Card from './Card.vue'

export default{
    components:{Card},
    computed:{
        podInfo(){
            return this.$store.state.gameInfo.pod_info
        },
        term(){
            switch(this.podInfo.term){
            case 0:
                return "PREFLOP"
            case 1:
                return "FLOP"
            case 2:
                return "TURN"
            case 3:
                return "RIVER"
            }
        }
    },
}
</script>

<style scoped>
.gameboard{
    position: absolute;
    left: 50%;
    top: 50%;
}
.gameboard-container{
    position: absolute;
    width: 400px;
    height: 200px;
    left: -200px;
    top: -100px;
    /* border: solid; */
}
.term{
    color: white;
    text-align: center;
    font-size: 25px;
    margin: 0 auto;
    margin-top: 5px;
    margin-bottom: 15px;
    background: rgba(200,200,255,0.2);
    width: 68%;
    border-radius: 6px;
}
.cards{
    width: 100%;
    height: 80px;
    padding-left: 62.5px;
}
.chips{
    height: 30px;
    margin-top: 10px;
}
.chip-icon{
    width: 30px;
    height: 30px;
    display: flex;
    float: left;
    margin-left: 150px;
    margin-right: 10px;
}
.chip-num{
    height: 30px;
    display: flex;
    float: left;
    color: rgb(60,60,200);
    font-size: 25px;
    padding-top: 2px;
    color: white;
}
</style>