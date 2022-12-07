import { createStore } from 'vuex'
import sourceData from '../game-list.json'
import gameData from '../game-info.json'

const store = createStore({
    state() {
        return {
            login: false,
            userName: "",
            inRoomId: 0,
            inGameId: -1, //当前游戏id，-1表示未选择
            games: sourceData.gamelist,
            gameInfo: 
            {
                room_name: gameData.room_name,
                view_cnt: gameData.view_cnt,
                user_infos: gameData.user_infos,
                pod_info: gameData.pod_info,
                last_action: gameData.last_action,
            },
            sitDown: false, //是否坐下
            showAction: [false,false,false,false,false,false,false,false], //是否显示玩家行动记录
        }
    },
    mutations: {
        login(state, name) {
            state.login = true
            state.userName = name
            console.log("userName:" + name)
        },
        logout(state) {
            state.login = false
            state.userName = ""
        },
        enterRoom(state, room_id) {
            state.inRoomId = room_id
            state.sitDown = false
        },
        sit(state) {
            state.sitDown = true
        },
        stand(state) {
            state.sitDown = false
        },
        exitRoom(state) {
            state.inRoomId = 0
        },
        updateRoomListInfo(state, info) {
            state.games[info.gameId].rooms = info.list
        },
        setGameId(state, id) {
            state.inGameId = id
        },
        updataGameinfo(state,info){
            state.gameInfo=info
        },
        changeShowAction(state, user_id) {
            if (user_id >= 1 && user_id <=8) {
                state.showAction[user_id - 1] = true
            }
            else if(user_id == -1){
                state.showAction = [false,false,false,false,false,false,false,false]
            }
            console.log(user_id)
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