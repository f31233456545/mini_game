import axios from 'axios'

export function request(request_type, params) {
    return axios
        .get('http://47.94.92.103:3005'+'/'+request_type, {params})
        .then(response => {
            //console.log(response.data)
            return response.data
        })
}