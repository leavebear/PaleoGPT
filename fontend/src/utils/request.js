//定制请求的实例
//导入axios  npm install axios
import axios from 'axios';
// 创建 axios 实例
const baseURL = 'http://localhost:8000';  // 设置正确的后端地址
const instance = axios.create({
    baseURL,  // 使用设置好的 baseURL
    timeout: 300000,  // 设置请求超时
});


import { useTokenStore } from '@/stores/token';
//添加请求拦截器
instance.interceptors.request.use(
    (config)=>{
        //请求前的回调
        const tokenStore = useTokenStore();
        //判断有没有Token
        if(tokenStore.token){
            config.headers.Authorization = tokenStore.token
        }
        return config;

    },
    (err)=>{
        //请求错误的回调
        return Promise.reject(err); // 确保错误能被捕获
    }
)

//添加响应拦截器
instance.interceptors.response.use(
    result=>{
        return result.data
    },
    err=>{
        alert('服务异常');
        return Promise.reject(err);
    }
)

export default instance;