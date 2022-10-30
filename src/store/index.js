import { createStore } from 'vuex'
import sourceData from '../game-list.json'

const store = createStore({
    state() {
        return {
            login: false,
            userName: "",
            inRoomId: 0,
            games: sourceData.gamelist,
        }
    },
    mutations: {
        login(state) {
            state.login = true;
        },
        logout(state) {
            state.login = false;
            state.userName = ""
        },
        enterRoom(state, room_id) {
            state.inRoomId = room_id;
        },
        exitRoom(state) {
            state.inRoomId = 0;
        },
        updateRoomListInfo(state, info) {
            state.games[info.gameId].rooms=info.list
        }
    },
    actions: {
        // updateRoomList({ commit, state }, gameId) {
        //     var params = {game_kind: gameId, user_name: state.userName}
        //     request('request_room_list', params)
        //         .then(data => {
        //             commit('updateRoomListInfo', {gameId:gameId, list:data})
        //             console.log(data)
        //         })
        //         .catch(function (error) { // 请求失败处理
        //             console.log("request failed!")
        //             console.log(error);
        //         })
        // }
    }
})

export default store