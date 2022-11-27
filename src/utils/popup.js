import { createApp } from 'vue'
import ActionPopup from '../components/ActionPopup.vue'
import SimplePopup from '../components/SimplePopup.vue'

// 将指定组件以浮窗形式弹出，并赋予其 remove 方法
const createPopup = function (component, position, props) {
    let body = document.body
    let mountNode = document.createElement('div')
    let style = `position: absolute;\
        z-index: 100;\
        left: ${position.left};\
        top: ${position.top};\
        right: ${position.right};\
        bottom: ${position.bottom};`
    mountNode.style = style
    body.appendChild(mountNode)

    const app = createApp(
        component,
        {
            ...props,
            remove() {  // 用于让组件自行 umount
                app.unmount(mountNode)
                document.body.removeChild(mountNode)
            }
        })
    return app.mount(mountNode)
}

// 将指定组件以浮窗形式弹出，并赋予其 remove 方法
// 此时 position 应以小数形式给出
// offset 以整数形式给出
const createPopupOffset = function (component, position, offset, props) {
    let body = document.body

    let mountNode = document.createElement('div')
    let style = `position: absolute;\
        z-index: 100;\
        left: ${Math.floor(position.left * window.innerWidth + offset.left)}px;\
        top: ${Math.floor(position.top * window.innerHeight + offset.top)}px;`
    mountNode.style = style
    // console.log(style)
    body.appendChild(mountNode)

    const app = createApp(
        component,
        {
            ...props,
            remove() {  // 用于让组件自行 umount
                app.unmount(mountNode)
                document.body.removeChild(mountNode)
            }
        })
    return app.mount(mountNode)
}

export function createActionPopup(title, message) {
    let position = { top: `10%`, right: `0px` }
    let props = { title: title, message: message, duration: 1000 }
    createPopup(ActionPopup,position,props)
}

var seatPopupPositions = {
    [-1] : { top: 0.5, left: 0.5 },

    [1] : { top: 0.8, left: 0.5 },
    [2] : { top: 0.65, left: 0.2 },
    [3] : { top: 0.35, left: 0.2 },
    [4] : { top: 0.15, left: 0.3 },
    [5] : { top: 0.15, left: 0.5 },
    [6] : { top: 0.15, left: 0.7 },
    [7] : { top: 0.35, left: 0.8 },
    [8] : { top: 0.65, left: 0.8 },
}

var seatPopupOffsets = {
    [-1] : { top: -130, left: -200 + 64 },

    [1] : { top: -60, left: 60 },
    [2] : { top: -60, left: 60 },
    [3] : { top: -60, left: 60 },
    [4] : { top: -60, left: 60 },
    [5] : { top: -60, left: 60 },
    [6] : { top: -60, left: 60 },
    [7] : { top: -60, left: 60 },
    [8] : { top: -60, left: 60 },
}

export function createSimplePopup(title, message, seat) {
    let props = { title: title, message: message, duration: 3000 }
    createPopupOffset(SimplePopup, seatPopupPositions[seat], seatPopupOffsets[seat], props)
}

export default createPopup