<template>
    <div class="create-room">
        <el-input
            class="create-room-input-box"
            v-model="this.room_name"
            placeholder="Enter new room name here"
            maxlength="20"
        />
        <el-button class="create-room-button" type="primary">Create Room</el-button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            room_name: ""
        }
    }
}
</script>

<style lan="css">
.create-room {
    height: auto;
    width: 960px;
    background: #434a50;
    border-radius: 6px;
    padding: 10px 8px;
}
.create-room-input-box {
    width: 80%;
    margin-right: 1%;
    font-size: 24px;
}
.create-room-button {
    width: 19%;
    font-size: 24px;
}
</style>