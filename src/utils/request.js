import axios from 'axios'
import store from '../store/index.js'

export function request(request_type, params) {
    return axios
        .get('http://127.0.0.1:9000'+'/'+request_type, {params})
        .then(response => {
            //console.log(response.data)
            return response.data
        })
        // .catch(function (error) { // 请求失败处理
        //     console.log(error);
        // })

}