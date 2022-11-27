<template>
    <div
        class="actionpopup-head"
        @mouseover="mouseoverHandler"
        @mouseout="mouseoutHandler"
        @click="clickHandler"
    >
        <div class="prefix"/>
        <span :style="{ color: titleColor }">
            {{ title + " " }}
        </span>
        <span :style="{ color: messageColor }">
            {{ message }}
        </span>
    </div>
</template>

<script>
export default {
    data() {
        return {
            timer: null
        }
    },
    props: {
        title: {
            type: String,
            default: 'message'
        },
        titleColor: {
            type: String,
            default: '#FFAA00'
        },
        message: {
            type: String,
            default: 'something'
        },
        messageColor: {
            type: String,
            default: '#000000'
        },
        duration: {
            type: Number,
            default: 0
        },
        remove: Function  // 在 popup.js 中提供，用于 umount 组件
    },
    methods: {
        setTimer(duration) {
            if (duration > 0) {
                this.timer = setTimeout(this.remove, duration)
            }
        },
        removeTimer() {
            if (this.timer !== null) {
                clearTimeout(this.timer)
                this.timer = null
            }
        },
        mouseoverHandler() {
            this.removeTimer()
        },
        mouseoutHandler() {
            this.setTimer(this.duration)
        },
        clickHandler() {
            this.remove()
        }
    },
    mounted() {
        this.setTimer(this.duration)
    },
    unmounted() {
        this.removeTimer()
    }
}
</script>

<style>
@keyframes slide-in {
0%{
    transform: translate(200px,0px);
}
10%{
    transform: translate(0px,0px);
}
90%{
    transform: translate(0px,0px);
    opacity: 100%;
}
95%{
    transform: translate(0px,0px);
    opacity: 50%;
}
100%{
    transform: translate(200px,0px);
    opacity: 0%;
}
}
.actionpopup-head {
    position: relative;
    background-color: white;
    /* border-radius: 4px; */
    padding: 10px;
    width: 200px;
    height: 40px;
    animation: slide-in 1s;
    -webkit-animation: slide-in 3s;
}
.prefix {
    position: absolute;
    top: 0px;
    left: -5px;
    height: 40px;
    width: 8px;
    background: #FFAA00;
}


</style>