<template>
    <Header></Header>
    <div class="authorization">
        <h1>
            Авторизация
        </h1>
        <div class="params">
            <div class="enterparams">
                <div class="title">
                    Параметры ввода <my-question>Ваш логин и пароль</my-question>
                </div>
                <div class="input_block"><span class="symbol_input symbol_input__login"></span><my-input limit="50" placeholder="Логин" v-model="login" class="input-profile"></my-input></div>
                <div class="input_block"><span class="symbol_input symbol_input__password"></span> <my-input limit="50" placeholder="Пароль" v-model="password" class="input-profile" type="password"></my-input></div>
            </div>
            <div class="captcha">
                <div class="title">
                    Решите задачу <my-question>Введите символы с картинки (буквы заглавные)</my-question>
                </div>
                <img ref="captcha__img"/>
                <div class="input_block"> <span class="symbol_input symbol_input__captcha"></span><my-input limit="6" placeholder="Текст на картинке"  class="input-profile" v-model="captcha"></my-input></div>
            </div>
            <div class="buttonsenter">
                <my-button class="button_regist" @click="authorization">Зайти в аккаунт</my-button>
                <router-link to="/regist">Создать новый</router-link>
            </div>
        </div>
    </div>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Info from '../Info/Info.vue'
import Header from '../Parts/Header.vue'
import Footer from '../Parts/Footer.vue'
import MakeRequest from '../../API/Request.js'
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: 'reg-block',
    components: {
        Header,
        Footer,
        Info
    },

    data()
    {
        return {
            login: '',
            password: '',
            captcha: '',
            captcha_token: '',
            status_error: '',
            title_error: '',
            isInfo: false,
            isError: false
        }
    },

    methods:
    {
        async getCaptcha()
        {
            let response;
            try{
                const url = `${BASE_URL}/api/captcha`;
                response = await MakeRequest(url);

            //обработка ошибок
            }catch(err){
                this.title_error = err.message;
                this.status_error = err.status;
                this.isInfo = true;
                this.isError = true;
                return;
            }

            this.$refs.captcha__img.src = "data:image/png;base64," + response.captcha_image
            this.captcha_token = response.captcha_token
        },

        async authorization()
        {
            if(this.first_name == '' && this.password == '')
            {
                this.status_error = "Ошибка"
                this.title_error = "Введены не все данные"
                this.isInfo = true
                this.isError = true
                return
            }

            let response;
            try{
                const url = `${BASE_URL}/api/auth`;
                const params = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Target-Action': 'LOGIN'
                    },
                    body: JSON.stringify({
                        login: this.login,
                        password: this.password,
                        captcha_token: this.captcha_token,
                        input_captcha: this.captcha
                    })
                }

                response = await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                this.title_error = err.message;
                this.status_error = err.status;
                this.isInfo = true;
                this.isError = true;
                return;
            }
            if(/2../.test(String(response.status)))
            {
                document.cookie = `session_token=Bearer ${response.session_token}; path=/; expires=${new Date(Date.now() + 1000 * 60 * 60 * 2).toUTCString()}`
                this.$router.push('/home')
            }
            else
            {
                this.status_error = "Ошибка"
                this.title_error = response.message
                this.isInfo = true
                this.isError = true
            }
        },
    },

    mounted()
    {
        this.getCaptcha()
    }
}

</script>

<style scoped>

    .authorization
    {
        width: 53%;
        height: 117vh;
        position: relative;
        left: 23.5%;
        margin-top: 50px;
        background-color: white;
        border-radius: 50px;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    h1
    {
        font-size: 4.3em;
        color: #AC2DFE;
        font-weight: 400;
        margin-top: 4%;
        margin-bottom: 6%;
        font-family: "Montserrat", sans-serif;
    }

    .params
    {
        width: 100%;
        height: 80%;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 4%;
        border-top: 1px solid #E7E7E7;
    }

    .enterparams
    {
        width: 48%;
        height: 28%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 5%;
    }

    .captcha
    {
        width: 48%;
        height: 40%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 5%;
    }

    .enterparams > .title, .captcha > .title
    {
        color: #515151;
        font-size: 1.5em;
        padding-left: 5px;
        display: flex;
        position: relative;
        align-items: center;
    }

    .question
    {
        display: inline-block;
        height: 20px;
        width: 20px;
        margin-left: 15px;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        vertical-align: middle;
        position: relative;
        background-image: url('@/assets/regist_auth/info.svg');
        font-size: 0.8em;
    }

    .answer
    {
        width: 200px;
        padding: 10px;
        position: absolute;
        background-color: white;
        border-radius: 25px;
        left: 20px;
        display: none;
        border: 1px solid #AC2DFE;
        transition-duration: 0.5s;
    }

    .question_enterparams:hover > .answer_enterparams, .question_captcha:hover > .answer_captcha
    {
        display: inline-block;
    }

    .input_block
    {
        width: 100%;
        height: 21%;
        display: flex;
        align-items: center;
        background-color: #F3F3F3;
        border-radius: 30px;
        display: flex;
        align-items: center;
    }

    .captcha > .input_block
    {
        height: 15%;
    }

    .captcha > img
    {
        width: 100%;
        height: 61%;
        border-radius: 30px;
    }

    .symbol_input
    {
        width: 6%;
        height: 50%;
        margin-left: 20px;
        display: inline-block;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        vertical-align: middle;
        position: relative;
    }

    .symbol_input__captcha
    {
        background-image: url('@/assets/regist_auth/capcha.svg');
    }

    .symbol_input__password
    {
        background-image: url('@/assets/regist_auth/password.svg');
    }

    .symbol_input__login
    {
        background-image: url('@/assets/regist_auth/login.svg');
    }

    .buttonsenter
    {
        width: 100%;
        height: 15%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 9%;
        position: relative;
    }

    .buttonsenter> a
    {
        font-size: 1.6em;
        text-decoration: none;
        color: #0000A9;
        margin-top: 3%;
    }



</style>
