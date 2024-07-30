<template>
    <Header></Header>
    <div class="register">
        <h1>
            Регистрация
        </h1>
        <div class="container_params">
            <div class="photoAndCaptcha">
                <div class="photo-reg">
                    <div class="title">
                        Изображение профиля <my-question>Вставьте свою иконку (опционально), картинка должна быть квадратной</my-question>
                    </div>
                    <div class="input-registr-picture-container">
                        <AddPhoto v-model="userPhoto" :isProfile="true" v-show="!userPhoto"></AddPhoto>
                        <Photo v-show="userPhoto" :picture="userPhoto" :blocked="true"></Photo>
                    </div>
                </div>
                <div class="captcha">
                    <div class="title">
                        Решите задачу <my-question>Введите символы, которые видите на картинке</my-question>
                    </div>
                    <img ref="captcha__img"/>
                    <div class="input_block"><span class="symbol_input symbol_input__captcha"></span><my-input limit="6" placeholder="Текст на картинке" class="input-profile" v-model="captcha" :class="{input_profile_error: spaceCheck(captcha)}"></my-input></div>
                </div>
            </div>
            <div class="params">
                <div class="aboutme">
                    <div class="title">
                        Обо мне <my-question>Введите данные о себе без пробелов (отчество при наличии)</my-question>
                    </div>
                    <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input limit="50" placeholder="Имя" class="input-profile" v-model="first_name" :class="{input_profile_error: spaceCheck(first_name)}"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input limit="50" placeholder="Фамилия" class="input-profile" v-model="sur_name" :class="{input_profile_error: spaceCheck(sur_name)}"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input limit="50" placeholder="Отчество (при наличии)" class="input-profile" v-model="middle_name" :class="{input_profile_error: spaceCheck(middle_name)}"></my-input></div>
                </div>
                <div class="enterparams">
                    <div class="title">
                        Параметры ввода <my-question>Придумайте логин и пароль без пробелов и повторите придуманный пароль</my-question>
                    </div>
                    <div class="input_block"><span class="symbol_input symbol_input__login"></span><my-input limit="50" placeholder="Логин" class="input-profile" v-model="login" :class="{input_profile_error: spaceCheck(login)}"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__password"></span> <my-input limit="50" placeholder="Придумайте пароль" class="input-profile" type="password" v-model="password" :class="{input_profile_error: spaceCheck(password)}"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__password"></span><my-input limit="50" placeholder="Повторите пароль" class="input-profile" type="password" v-model="password_repeat" :class="{input_profile_error: spaceCheck(password_repeat)}"></my-input></div> 
                </div>
                <div class="optional">
                    <div class="title">
                        Связь со мной (не обязательно) <my-question>Введите почту и номер телефона без специальных символов (только первый +)</my-question>
                    </div>
                    <div class="input_block"><span class="symbol_input symbol_input__mail"></span><my-input limit="100" placeholder="Почта" class="input-profile" v-model="email" :class="{input_profile_error: spaceCheck(email)}"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__phone"></span><my-input limit="12" placeholder="Номер телефона" class="input-profile" v-model="phone" :class="{input_profile_error: spaceCheck(phone)}"></my-input></div>
                </div>
            </div>
        </div>
        <div class="agree">
            <div>
                Я ознакомился(-лась) с <router-link>политикой конфеденциальности, </router-link><br>
                также согласен(-на) с <router-link>правилами поведения на платформе</router-link>
            </div>
            <my-checkbox class="registr_checkbox" @click="checkbox = !checkbox" :checkbox="checkbox"></my-checkbox>
        </div>
        <div class="buttonsenter">
            <my-button class="button_regist" @click = 'registration'>Создать аккаунт</my-button>
            <router-link to="/auth">У меня уже есть аккаунт</router-link>
        </div>
    </div>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Info from '../Info/Info.vue'
import Header from '../Parts/Header.vue'
import Footer from '../Parts/Footer.vue'
import AddPhoto from '../Parts/AddPhoto.vue'
import Photo from '../Parts/Photo.vue'

export default {
    name: 'reg-block',
    components: {
        Header,
        AddPhoto,
        Info,
        Footer,
        Photo
    }, 
    data()
    {
        return {
            checkbox: false,
            first_name: '',
            sur_name: '',
            middle_name: '',
            login: '',
            password: '',
            password_repeat: '',
            email: '',
            phone: '',
            captcha: '',
            captcha_token: '',
            userPhoto: "",
            notSpace: false,
            isError: false,
            isInfo: false,
            status_error: "",
            title_error: ''
        }
    },
    methods:
    {
        async getCaptcha()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/captcha`)
            const data = await response.json()
            this.$refs.captcha__img.src = "data:image/png;base64," + data.captcha_image
            this.captcha_token = data.captcha_token
        },

        loadPicture(event)
        {   
            let file = event.target.files[0];
            let pictureProfile = this.$refs.pictureProfile;
            if(file)
            {
                let reader = new FileReader();
                reader.onload = function(e) {
                    pictureProfile.src = e.target.result
                };
                reader.readAsDataURL(file);
                this.isPictureOnload = true
            }
        },

        async registration()
        {
            if(this.first_name == '' && this.sur_name == '' && this.middle_name == '' && this.login == '' && this.password == '' && this.password_repeat == '' && this.captcha == '')
            {
                this.status_error = "Ошибка"
                this.title_error = "Введены не все данные"
                this.isInfo = true
                this.isError = true
                return
            }
            if(document.getElementsByClassName('input_profile_error').length != 0)
            {
                this.status_error = "Ошибка"
                this.title_error = "Введены некорректные данные"
                this.isInfo = true
                this.isError = true
                return
            }
            if(this.password.length < 8)
            {
                this.status_error = "Ошибка"
                this.title_error = "Слишком короткий пароль"
                this.isInfo = true
                this.isError = true
                return
            }
            if(this.password != this.password_repeat)
            {
                this.status_error = "Ошибка"
                this.title_error = "Пароли не совпадают"
                this.isInfo = true
                this.isError = true
                return
            }
            if(!this.checkbox)
            {
                this.status_error = "Ошибка"
                this.title_error = "Не согласен(-на) с правилами поведения на платформе"
                this.isInfo = true
                this.isError = true
                return
            }
            let data = {
                first_name: this.first_name,
                sur_name: this.sur_name,
                middle_name: this.middle_name || null,
                login: this.login,
                password: this.password,
                email: this.email || null,
                phone_number: this.phone || null,
                captcha_token: this.captcha_token,
                input_captcha: this.captcha,
                pers_photo_data: this.userPhoto || null
            }
            for(let key in data)
            {
                console.log(key)
                if(key == "pers_photo_data")
                {
                    data[key] = this.userPhoto || null
                    continue
                }
                if(data[key] == '' || data[key] == null)
                {
                    delete data [key]
                }
            }
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/auth`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Target-Action': 'REGISTER'
                },
                body: JSON.stringify(data)
            })
            const resData = await response.json()
            console.log(resData)
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            if(/2../.test(String(resData.status)))
            {
                document.cookie = `session_token=Bearer ${resData.session_token}; path=/; expires=${new Date(Date.now() + 1000 * 60 * 60 * 2).toUTCString()}`
                this.$router.push('/home')
            }
            else
            {
                this.status_error = String(resData.status)
                this.title_error = resData.message
                this.isError = true
            }
        },

        spaceCheck(elem)
        {
            let isSpace = false
            Array.from(elem).forEach(element => {
                if (element == ' ')
                {
                    isSpace = true
                }
            });
            if(isSpace)
            {
                return true
            }
            return false 
        }
    },

    mounted()
    {
        this.getCaptcha()
    }
}
</script>

<style scoped>
    .register
    {
        width: 70%;
        height: 159vh;
        position: relative;
        left: 15%;
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

    .container_params
    {
        width: 80%;
        height: 55%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        padding-top: 4%;
        border-top: 1px solid #E7E7E7;
    }
        
    .container_params .title
    {
        color: #515151;
        font-size: 1.5em;
        padding-left: 5px;
        display: flex;
        position: relative;
        align-items: center;
    }

    .photoAndCaptcha
    {
        width: 50%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .photo-reg
    {
        width: 100%;
        height: 52%;
        position: relative;
        display: flex;
        flex-direction: column;
    }

    .enterpicture
    {
        width: 100%;
        height: 21%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 6%;
    }

    .input-registr-picture-container
    {
        width: 80%;
        height: 83%;
        position: relative;
        margin-top: 5.7%;
    }

    .captcha
    {
        width: 80%;
        height: 41%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .captcha > .input_block
    {
        height: 17.3%;
    }

    .captcha > img
    {
        width: 100%;
        height: 61%;
        border-radius: 30px;
    }

    .params
    {
        width: 50%;
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    .aboutme, .enterparams, .optional
    {
        width: 100%;
        height: 36%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 5%;
    }

    .aboutme
    {
        margin-top: 0;
    }

    .optional
    {
        height: 28%;
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

    .optional > .input_block
    {
        height: 27%;
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

    .symbol_input__phone
    {
        background-image: url('@/assets/regist_auth/phone.svg');
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

    .symbol_input__user
    {
        background-image: url('@/assets/regist_auth/usericon.svg');
    }

    .symbol_input__mail
    {
        background-image: url('@/assets/regist_auth/mail.svg');
    }

    .agree
    {
        width: 70%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 4%;
    }

    .agree > div:nth-child(1)
    {
        font-size: 1.2em;
    }

    .agree > div:nth-child(1)> a
    {
        text-decoration: none;
        color: #0000A9;
    }

    .buttonsenter
    {
        width: 80%;
        height: 9%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 6%;
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
    