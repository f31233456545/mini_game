import { createStore } from 'vuex'
import sourceData from '../game-list.json'

const store = createStore({
    state() {
        return {
            count: 1,
            login: false,
            userName: "Bob",
            isPlaying: false,
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
        }
    },
    actions: {

    }
})

export default store