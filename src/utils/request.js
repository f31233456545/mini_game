import axios from 'axios'

export function request(request_type, params) {
    return axios
        .get('http://127.0.0.1:9000'+'/'+request_type, {params})
        .then(response => {
            //console.log(response.data)
            return response.data
        })
}