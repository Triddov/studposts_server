<template>
    <Header :isProfile="true"></Header>
    <div class="profile">
        <h1>
            Редактирование профиля
        </h1>
        <div class="params">
            <div class="photoAndAbout">
                <div class="picture">
                    <div class="title">
                        Изображение профиля <my-question>Покажите себя миру!</my-question>
                    </div>
                    <div class="input-picture-container">
                        <AddPhoto v-model="userPhoto" v-show="!userPhoto" :isProfile="true"></AddPhoto>
                        <Photo v-show="userPhoto" :picture="userPhoto" @deletePhoto="userPhoto = $event" @changePhoto="userPhoto = $event"></Photo>
                    </div>
                </div>
                <div class="common">
                    <div class="about">
                        <div class="title">
                            Обо мне <my-question>Ограничение на поле 50 символов</my-question>
                        </div>
                        <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input placeholder="Имя" class="input-profile" v-model="first_name"></my-input></div>
                        <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input placeholder="Фамилия" class="input-profile" v-model="sur_name"></my-input></div>
                        <div class="input_block"><span class="symbol_input symbol_input__user"></span><my-input placeholder="Отчество" class="input-profile" v-model="middle_name"></my-input></div>
                    </div>
                    <div class="pass">
                        <div class="title">
                            Введите пароль для любых изменений <my-question> Введите новый пароль для любых изменений</my-question>
                        </div>
                        <div class="input_block"><span class="symbol_input symbol_input__redpass"></span><my-input placeholder="Старый пароль" class="input-profile" v-model="oldPassword"></my-input></div>
                    </div>
                </div>
            </div>
            <div class="mailAndPassword">
                <div class="mailAndPassword_block">
                    <div class="title">
                        Связь со мной (не обязательно) <my-question>Только российские номера</my-question>
                    </div>
                    <div class="input_block"><span class="symbol_input symbol_input__mail"></span><my-input placeholder="email" class="input-profile" v-model="email"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__phone"></span><my-input placeholder="Номер телефона" class="input-profile" v-model="phone"></my-input></div>
                </div>
                <div class="mailAndPassword_block">
                    <div class="title">
                        Параметры входа <my-question>Введите пароль, если хотите изменить его</my-question>
                    </div>
                    <div class="input_block"><span class="symbol_input symbol_input__password"></span><my-input placeholder="Пароль (не менее 8 симв)" class="input-profile" v-model="password"></my-input></div>
                    <div class="input_block"><span class="symbol_input symbol_input__password"></span><my-input placeholder="Повторить пароль" class="input-profile" v-model="password_rep"></my-input></div>
                </div>
            </div>
        </div>
        <my-button class="button_profile" @click="editProfile">Обновить профиль</my-button>
    </div>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Header from '../Parts/Header.vue';
import Footer from '../Parts/Footer.vue';
import Photo from '../Parts/Photo.vue';
import AddPhoto from '../Parts/AddPhoto.vue';
import Info from '../Info/Info.vue';
import MakeRequest from '../../API/Request.js';
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: "profile-block",
    components: {
        Header,
        Footer,
        Photo,
        AddPhoto,
        Info
    },

    data()
    {
        return {
            userPhoto: "",
            user: {},
            first_name: "",
            sur_name: "",
            middle_name: "",
            email: "",
            phone: "",
            password: "",
            isInfo: false,
            isError: false,
            status_error: "",
            title_error: "",
            oldPassword: "",
            password_rep: ""
        }
    },

    methods: {
        async isAuthorized()
        {
            if(document.cookie.split('session_token=')[1])
            {
                let response;
                try{
                    const url = `${BASE_URL}/api/get_user`;
                    const params = {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            "Authorization": document.cookie.split('session_token=')[1]
                        }
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

                const data = response;
                this.user = data.user_data
                this.userPhoto = `${BASE_URL}/api/${data.user_data.persPhotodata}` //QW
                this.first_name = this.user.firstName || ""
                this.sur_name = this.user.surName || ""
                this.middle_name = this.user.middleName || ""
                this.email = this.user.email || ""
                this.phone = this.user.phoneNumber || ""
            }
            else
            {
                this.$router.push('/home');
            }
        },

        async editProfile()
        {
            if(this.first_name == '' && this.sur_name == '')
            {
                this.status_error = "Ошибка"
                this.title_error = "Введите имя и фамилию"
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
            if(this.oldPassword == '' || this.oldPassword == null)
            {
                this.status_error = "Ошибка"
                this.title_error = "Вы не ввели использующийся пароль"
                this.isInfo = true
                this.isError = true
                return
            }
            if(this.password)
            {
                if(this.password.length < 8)
                {
                    this.status_error = "Ошибка"
                    this.title_error = "Новый пароль должен состоять из 8 и более символов"
                    this.isInfo = true
                    this.isError = true
                    return
                }
                if(this.password != this.password_rep)
                {
                    this.status_error = "Ошибка"
                    this.title_error = "Пароли не совпадают"
                    this.isInfo = true
                    this.isError = true
                    return
                }
            }
            let data = {
                first_name: this.first_name,
                sur_name: this.sur_name,
                middle_name: this.middle_name  || null,
                password: this.password || null,
                email: this.email || null,
                phone_number: this.phone || null,
                pers_photo_data: this.userPhoto || null,
                current_password: this.oldPassword
            }
            if(/sources/.test(this.userPhoto))
            {
                data.pers_photo_data = "alreadyExist"
            }
            for(let key in data)
            {
                if(data[key] == '' || data[key] == null)
                {
                    delete data [key]
                }
            }
            try{
                const url = `${BASE_URL}/api/edit_user`;
                const params = {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authorization": document.cookie.split('session_token=')[1]
                    },
                    body: JSON.stringify(data)
                }

                await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                this.title_error = err.message;
                this.status_error = err.status;
                this.isInfo = true;
                this.isError = true;
                return;
            }

          if(this.password)
          {
            document.cookie = `session_token=Bearer ${document.cookie.split(/Bearer /)[1]}; path=/; expires=${new Date(Date.now() - 1000).toUTCString()}`
            this.$router.push('/auth')
          }

          this.$router.push('/home')
        }
    },

    mounted()
    {
        this.isAuthorized()
    }
}
</script>

<style scoped>

    .profile
    {
        width: 70%;
        height: 117vh;
        background-color: white;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        left: 15%;
        margin-top: 60px;
        border-radius: 50px;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
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
        width: 73%;
        height: 59%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding-top: 4%;
        border-top: 1px solid #E7E7E7;
    }

    .photoAndAbout
    {
        width: 100%;
        height: 64%;
        display: flex;
        justify-content: space-between;
    }

    .title
    {
        color: #515151;
        font-size: 1.3em;
        padding-left: 5px;
        display: flex;
        position: relative;
        align-items: center;
    }

    .picture
    {
        width: 43%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .input-picture-container
    {
        width: 100%;
        height: 90%;
    }

    .common
    {
        width: 47%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between
    }

    .about
    {
        width: 100%;
        height: 65%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .pass
    {
        width: 100%;
        height: 30%;
        display: flex;
        flex-direction: column;
        justify-content: end;
    }

    .pass > .title
    {
        color: red;
    }

    .about > .input_block
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

    .pass > .input_block
    {
        width: 100%;
        height: 45%;
        display: flex;
        align-items: center;
        background-color: #F3F3F3;
        border-radius: 30px;
        display: flex;
        align-items: center;
        margin-top: 10px;
    }

    .mailAndPassword
    {
        width: 100%;
        height: 27%;
        display: flex;
        justify-content: space-between;
    }

    .mailAndPassword_block
    {
        width: 47%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .mailAndPassword_block > .input_block
    {
        width: 100%;
        height: 32%;
        display: flex;
        align-items: center;
        background-color: #F3F3F3;
        border-radius: 30px;
        display: flex;
        align-items: center;
    }

    .symbol_input
    {
        width: 6%;
        height: 50%;
        margin-left: 20px;
        display: inline-block;
        background-size: 100%;
        background-repeat: no-repeat;
        background-position: center;
        vertical-align: middle;
        position: relative;
    }

    .symbol_input__phone
    {
        background-image: url('@/assets/regist_auth/phone.svg');
    }

    .symbol_input__redpass
    {
        background-image: url('@/assets/regist_auth/redPass.svg');
        background-size: 70%;
    }

    .symbol_input__password
    {
        background-image: url('@/assets/regist_auth/password.svg');
    }

    .symbol_input__user
    {
        background-image: url('@/assets/regist_auth/usericon.svg');
    }

    .symbol_input__mail
    {
        background-image: url('@/assets/regist_auth/mail.svg');
    }

</style>
