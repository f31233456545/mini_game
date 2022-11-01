import axios from 'axios'
import { ElLoading } from 'element-plus'

export function request(request_type, params) {
    const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0,0,0,0)',
        fullscreen: false,
    })
    return axios
        .get('http://127.0.0.1:9000'+'/'+request_type, {params})
        .then(response => {
            //console.log(response.data)
            loading.close()
            return response.data
        })
        .catch(function (error) {
            alert("request failed!")
            console.log("request failed!")
            console.log(error);
            loading.close()
            return null
        })
}

