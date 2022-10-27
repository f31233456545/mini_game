import { createStore } from 'vuex'
import sourceData from '../game-list.json'
import { request } from '../utils/request.js'

const store = createStore({
    state() {
        return {
            count: 1,
            login: false,
            userName: "Bob",
            inRoomId: 0,
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
        enterRoom(state, room_id) {
            state.inRoomId = room_id;
        },
        exitRoom(state) {
            state.inRoomId = 0;
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
        },
        createRoom({ commit, dispatch, state }, params) {
            return new Promise((resolve, reject) => {
                request('request_create_room', params)
                .then(data => {
                    if (data.succeed == true)
                    {
                        console.log(data);
                        resolve(data.room_id);
                    }
                    else
                    {
                        console.log("create failed!");
                        reject(data);
                    }
                })
                .catch(function (error) {
                    console.log("request failed!");
                    reject(error);
                })
            })
        },
        joinRoom({ commit, state }, params) {
            return new Promise((resolve, reject) => {
                request('request_join_room', params)
                .then(data => {
                    if (data.succeed == true)
                    {
                        console.log(data);
                        commit("enterRoom", params.room_id);
                        resolve();
                    }
                    else
                    {
                        console.log("join failed!");
                        reject(data);
                    }
                })
                .catch(function (error) {
                    console.log("request failed!");
                    reject(error);
                })
            })
        }
    }
})

export default store