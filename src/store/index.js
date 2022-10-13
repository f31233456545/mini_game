import { createStore } from 'vuex'
import sourceData from '../game-list.json'

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
        }
    },
    actions: {

    }
})

export default store