<script setup>
import { User, Lock } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios';
//控制注册与登录表单的显示， 默认显示注册
const isRegister = ref(false)
const router = useRouter();

//定义数据模型
const registerData = ref({
    email: '',
    password: '',
    rePassword: ''
})

const loginData = ref({
    email: '',
    password: '',
})

const checkRePassword = (rule, value, callback) => {
    if (value === '') {
        callback(new Error('请再次输入密码'))
    } else if (value !== registerData.value.password) {
        callback(new Error('请确保两次输入的密码一样'))
    } else {
        callback()
    }
}

// 定义表单校验规则
const rules = {
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
    ],
    rePassword: [
        { validator: checkRePassword, trigger: 'blur' }
    ],
}

//调用后台接口，完成注册
import { userRegisterService, userLoginService } from '@/api/login'
const register = async () => {
    //registerData是一个响应式对象
    console.log(registerData.value)
    let result = await userRegisterService(registerData.value);
    if (result.code === 0) {
        alert(result.msg ? result.msg : '注册成功');
    }
    else {
        alert(result.msg ? result.msg : '注册失败')
    }
}

//调用接口完成登录
const login = async () => {
    console.log(loginData.value);
    try {
        const response = await axios.post('http://localhost:8000/api/user/login', {
            email: loginData.value.email,
            password: loginData.value.password
        });

        if (response.data.status_code === 0) {
            // 登录成功后跳转到 /conversation
            router.push('/conversation');
        } else {
            alert(response.data.status_msg);
        }
    } catch (error) {
        console.error('登录请求失败:', error);
        if (error.response) {
            console.error('后端返回的状态码:', error.response.status);
            console.error('后端返回的数据:', error.response.data);
        } else if (error.request) {
            console.error('请求已发出，但未收到响应:', error.request);
        } else {
            console.error('请求设置过程中出现问题:', error.message);
        }
        alert('登录请求失败');
    }
};
// const login = async () => {
//     console.log(loginData.value)
//     if (loginData.value.email === 'admin@163.com' && loginData.value.password === 'admin') {
//         // 登录成功后跳转到 /main
//         router.push('/conversation')  // 跳转到 main 页面
//     }
//     else {
//         alert(console.log('用户名或密码错误'))
//     }
    // let result = await userLoginService(loginData.value);
    // console.log(result)
    // if(result.data.status_code===200){
    //     alert(result.msg?result.msg:'登录成功');
    // }
    // else {
    //     alert(result.msg?result.msg:'登录失败')
    // }
// }


//定义函数，用来清空数据模型的数据
const clearRegisterData = () => {
    registerData.value = {
        username: '',
        password: '',
        repassword: ''
    }
}

const clearLoginData = () => {
    loginData.value = {
        username: '',
        password: ''
    }
}


</script>



<template>
    <el-row class="login-page">
        <el-col :span="1" :offset="1" class="title">
            <h1>PaleoGPT</h1>
        </el-col>
        <el-col :span="6" :offset="13" class="form">
            <div class="login-container">
                <!-- 注册表单 -->
                <el-form ref="form" size="large" autocomplete="off" v-if="isRegister" :model="registerData"
                    :rules="rules">
                    <el-form-item>
                        <h1>注册</h1>
                    </el-form-item>
                    <el-form-item prop="email">
                        <el-input :prefix-icon="User" placeholder="输入邮箱" v-model="registerData.email"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input :prefix-icon="Lock" type="password" placeholder="请输入密码"
                            v-model="registerData.password"></el-input>
                    </el-form-item>
                    <el-form-item prop="rePassword">
                        <el-input :prefix-icon="Lock" type="password" placeholder="请输入再次密码"
                            v-model="registerData.rePassword"></el-input>
                    </el-form-item>
                    <!-- 注册按钮 -->
                    <el-form-item>
                        <el-button class="button" type="primary" auto-insert-space @click="register">
                            注册
                        </el-button>
                    </el-form-item>
                    <el-form-item class="flex">
                        <el-link type="info" :underline="false" @click="isRegister = false; clearRegisterData()">
                            ← 返回
                        </el-link>
                    </el-form-item>
                </el-form>
                <!-- 登录表单 -->
                <el-form ref="form" size="large" autocomplete="off" v-else :model="loginData" :rules="rules">
                    <h1>密码登录</h1>
                    <el-form-item prop="email">
                        <div>邮箱</div>
                        <el-input class="input" :prefix-icon="User" placeholder="输入邮箱"
                            v-model="loginData.email"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <div>密码</div>
                        <el-input class="input" name="password" :prefix-icon="Lock" type="password" placeholder="请输入密码"
                            v-model="loginData.password"></el-input>
                    </el-form-item>
                    <el-form-item class="flex">
                        <div class="flex">
                            <el-checkbox>记住我</el-checkbox>
                            <el-link type="primary" :underline="false">忘记密码？</el-link>
                        </div>
                    </el-form-item>
                    <!-- 登录按钮 -->
                    <el-form-item>
                        <el-button class="button" type="primary" auto-insert-space @click="login">登录</el-button>
                    </el-form-item>
                    <el-form-item class="flex">
                        <el-link type="info" :underline="false" @click="isRegister = true; clearLoginData()">
                            注册 →
                        </el-link>
                    </el-form-item>
                </el-form>
            </div>
        </el-col>
    </el-row>
</template>

<style lang="scss" scoped>
/* 样式 */
.login-page {
    height: 100vh;
    background-image: url('@/assets/login_bg.jpg');
    background-size: cover;
    /* 图片覆盖整个页面 */

    .login-container {
        background: rgba(255, 255, 255, 0.8);
        /* 白色半透明背景 */
        border-radius: 20px;
        padding: 70px 40px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 600px;
        width: 110%;
    }


    .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        user-select: none;

        h2 {
            margin: 0 0 20px 0;
            text-align: center;
        }


        .button {
            width: 110%;
            background-color: rgb(82, 82, 228);
        }

        .flex {
            width: 100%;
            display: flex;
            justify-content: space-between;
        }
    }
}
</style>