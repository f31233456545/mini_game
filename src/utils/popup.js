import { createApp } from 'vue'
import ActionPopup from '../components/ActionPopup.vue'

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

export function createActionPopup(title, message) {
    let position = { top: `15%`, right: `0px` }
    let props = { title: title, message: message, duration: 1000 }
    createPopup(ActionPopup,position,props)
}

export default createPopup