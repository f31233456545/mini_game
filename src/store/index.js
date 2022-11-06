import { createStore } from 'vuex'
import sourceData from '../game-list.json'
import gameData from '../game-info.json'

const store = createStore({
    state() {
        return {
            login: false,
            userName: "",
            inRoomId: 0,
            games: sourceData.gamelist,
            gameInfo: {
                user_infos: gameData.user_infos,
                pod_info: gameData.pod_info,
                last_action: gameData.last_action,
            }
        }
    },
    mutations: {
        login(state, name) {
            state.login = true;
            state.userName = name;
        },
        logout(state) {
            state.login = false;
            state.userName = "";
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