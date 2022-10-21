import { createStore } from 'vuex'
import sourceData from '../game-list.json'
import { request } from '../utils/request.js'

const store = createStore({
    state() {
        return {
            count: 1,
            login: false,
            userName: "Bob",
            isInRoom: false,
            games: sourceData.gamelist,
        }
    },
    mutations: {
        increment(state,n) {
            state.count+=n
        },
        login(state) {
            state.login = true;
        },
        logout(state) {
            state.login = false;
        },
        enterRoom(state) {
            state.isInRoom = true;
        },
        exitRoom(state) {
            state.isInRoom = false;
        },
        updateRoomListInfo(state, info) {
            state.games[info.gameId].rooms=info.list
            //console.log(list)
        }
    },
    actions: {
        updateRoomList({ commit, state }, gameId) {
            var params = {game_kind: gameId, user_name: state.userName}
            request('request_room_list', params)
                .then(data => {
                    commit('updateRoomListInfo', {gameId:gameId, list:data})
                    console.log(data)
                })
                .catch(function (error) { // 请求失败处理
                    console.log("request failed!")
                    console.log(error);
                })
        }
    }
})

export default store