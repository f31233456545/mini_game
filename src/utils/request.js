import axios from 'axios'
import { ElLoading } from 'element-plus'

export function request(request_type, params, useloading = true) {
    if (useloading) {
        const loading = ElLoading.service({
            lock: true,
            text: 'Loading',
            background: 'rgba(0,0,0,0)',
            fullscreen: true,
        })
        return axios
            .get('http://47.94.92.103:3006'+'/'+request_type, {params})
            .then(response => {
                loading.close()
                return response.data
            })
            .catch(function (error) {
                console.log("request failed!")
                console.log(error)
                loading.close()
                return null
            })
    }
    else {
        return axios
            .get('http://47.94.92.103:3006'+'/'+request_type, {params})
            .then(response => {
                return response.data
            })
            .catch(function (error) {
                console.log("request failed!")
                console.log(error)
                return null
            })
    }

}