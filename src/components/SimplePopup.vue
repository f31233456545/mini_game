<template>
    <div class="simplepopup-head" @click="clicked">
        <span :style="{color: titleColor}">
            {{title}}: 
        </span>
        <span :style="{color: messageColor}">
            {{message}}
        </span>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            default: "message"
        },
        titleColor: {
            type: String,
            default: "#FFCC00"
        },
        message: {
            type: String,
            default: "something"
        },
        messageColor: {
            type: String,
            default: "#FFFFFF"
        },
        remove: Function  // 在 popup.js 中提供，用于 umount 组件
    },
    methods: {
        clicked() {
            this.remove()
        }
    }
}
</script>

<style>
.simplepopup-head {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    padding: 3px;
    float: left;
}
</style>