<template>
    <router-link :to="`/${this.id}/${this.name}`">
        <div class="game-list-item">
            <div class="game-list-item-game-name">
                {{name}}
            </div>
            <div class="game-list-item-img-wrapper">
                <img :src="`images/${this.img}`"/>
            </div>
            <div class="game-list-item-footer">
                . . .
            </div>
        </div>
    </router-link>

</template>

<script>
export default{
    props:{
        id: Number,
        name: String,
        img: String,
    },
}
</script>

<style lan="css">
.game-list-item{
    float: left;
    height: 300px;
    width: 280px;
    text-align: center;
    /* border-style: solid;
    border-color: black; */
    border-radius: 6px;
    background: #434a50;
    margin: 20px;
}
.game-list-item:hover{
    transform: scale(1.05);
}
.game-list-item-game-name{
    color: white;
    font-size: 20px;
    padding: 8px;
}
.game-list-item-img-wrapper img{
    width: 100%;
    height: 220px;
}
.game-list-item-footer{
    font-size: 20px;
    color: #ccc;
    padding-bottom: 10px;
}
</style>