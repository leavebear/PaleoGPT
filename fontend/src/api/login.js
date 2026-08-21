//导入request.js请求工具
import request from '@/utils/request.js'
import axios from 'axios';

//提供调用注册接口的函数
export const userRegisterService = (registerData)=>{
    //借助于UrlSearchParams完成传递
    const params = new URLSearchParams()
    for(let key in registerData){
        params.append(key,String(registerData[key]));
    }
    return request.post('/api/register/pwd',params);
}

//提供调用登录接口的函数
// export const userLoginService = (loginData)=>{
//     const params = new URLSearchParams();
//     for(let key in loginData){
//         params.append(key,String(loginData[key]))
//     }
//     request.post('/api/login/pwd',params);
// }

export const userLoginService = (loginData) => {
    return axios.post('http://localhost:17100/api/login/pwd', loginData, {
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => {
        // 处理响应
        return response;
    }).catch(error => {
        // 处理错误
        console.error('Error during login:', error);
        throw error;
    });;
};