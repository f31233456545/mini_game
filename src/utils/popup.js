import { createApp } from 'vue'

// 将指定组件以浮窗形式弹出，并赋予其 remove 方法
const createPopup = function (component, position, props) {
    let body = document.body
    let mountNode = document.createElement('div')
    let style = `position: absolute; left: ${position.left}; top: ${position.top}; $right: ${position.right}; ${position.bottom};`
    mountNode.style = style
    body.appendChild(mountNode)

    const app = createApp(component, {
        ...props,
        remove() {  // 用于让组件自行 umount
            app.unmount(mountNode)
            document.body.removeChild(mountNode)
        }
    })
    return app.mount(mountNode)
}

export default createPopup