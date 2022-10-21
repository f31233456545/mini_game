import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'


const routes = [
    { path: '/', name: 'Home', component: () => import('../views/Home.vue') },
    { path: '/games', name: 'Games', component: () => import('../views/Games.vue') },
    { path: '/user-info', name: 'User Info', component: () => import('../views/UserInfo.vue') },
    { path: '/login-signup', name: 'Login/Sign up', component: () => import('../views/LoginSignup.vue') },
    {
        path: '/:id/:name',
        name: 'enter-game',
        component: () => import('../views/Rooms.vue'),
    },
    {
        path: '/:id/:name/content/:room_id',
        name: 'play-room',
        component: () => import('../views/PlayRoom.vue'),
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    linkActiveClass:"active-link"
})

export default router