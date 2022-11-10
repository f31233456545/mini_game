<template>
    <div
        class="simplepopup-head"
        @mouseover="mouseoverHandler"
        @mouseout="mouseoutHandler"
        @click="clickHandler">
        <span :style="{ color: titleColor }">
            {{ title }}:
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
            default: '#FFCC00'
        },
        message: {
            type: String,
            default: 'something'
        },
        messageColor: {
            type: String,
            default: '#FFFFFF'
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
.simplepopup-head {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    padding: 3px;
}
</style>