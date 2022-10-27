<template>
    <div class="create-room">
        <el-input
            class="create-room-input-box"
            v-model="this.room_name"
            placeholder="Enter new room name here"
            maxlength="20"
        />
        <span class="create-room-radios">
            <input
                type="radio"
                value="private"
                v-model="room_privacy"
            />
            Private
            <input
                type="radio"
                value="public"
                v-model="room_privacy"
            />
            Public
        </span>
        <el-button
            class="create-room-button"
            type="primary"
            @click="create_room">
            Create Room
        </el-button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            room_name: "",
            room_privacy: "private",
        }
    },
    computed:{
        gameInfo(){
            return this.$store.state.games.find(gameInfo => gameInfo.id===parseInt(this.$route.params.id))
        }
    },
    methods: {
        create_room() {
            this.$store.dispatch("createRoom", {
                    private: (this.room_privacy == "private"),
                    room_name: this.room_name,
                    game_kind: 0,
                    creator_name: this.$store.state.userName
                }).then((room_id) => {
                    this.join_room(room_id);
                });
        },
        join_room(room_id) {
            this.$store.dispatch("joinRoom", 
                {
                    room_id: room_id,
                    user_name: this.$store.state.userName,
                }).then(() => {
                    console.log(this.$store.state.inRoomId);
                    this.$router.push(`${this.$route.path}/content/${this.$store.state.inRoomId}`);
                });
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
    width: 55%;
    font-size: 24px;
}
.create-room-radios {
    width: auto;
    font-size: 24px;
    color: white;
    vertical-align: middle;
    margin-left: 10px;
    margin-right: 10px;
}
.create-room-button {
    width: 20%;
    font-size: 24px;
}
</style>