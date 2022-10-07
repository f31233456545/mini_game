<template>
    <router-link :to="`/${this.id}/${this.name}`">
        <div class="game-list-item">
            <div>
                {{id}}
            </div>
            <div>
                {{name}}
            </div>
        </div>
    </router-link>

</template>

<script>
export default{
    props:{
        id: Number,
        name: String,
    },
}
</script>

<style lan="css">
.game-list-item{
    float: left;
    height: 300px;
    width: 280px;
    text-align: center;
    border-style: solid;
    border-color: black;
    margin: 20px;
}
</style>