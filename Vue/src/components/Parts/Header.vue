<template>
    <header :class="{shadow: !isSearchSort}">
        <div class="profile">
            <div class="profile__icon" v-if="isProfile && isLoad && isAuthoized">
                <img :src="userIcon"/>
            </div>
            <div class="profile__icon__standart" v-if="isProfile && isLoad && !isAuthoized">
                <img src="@/assets/header/usericon.svg"/>
            </div>
            <div class="profile__link" v-if="isProfile && !isAuthoized && isLoad"><router-link to="/auth">войти</router-link><router-link to="/regist">регистрация</router-link></div>
            <div class="profile__link" v-if="isProfile && isAuthoized  && isLoad"><span class="prifle_exit_link" @click="exitProfile">выйти</span><router-link to="/profile">профиль</router-link></div>
        </div>
        <div class="logo">
            <img class="logo__ncfu" src="@/assets/header/ncfu.svg"/><img class="logo__studposts" src="@/assets/header/studposts.svg"/>
        </div>
        <nav>
            <router-link to="/home" class="nav__link" exact-active-class="nav__link_active">
                Главная
                <div></div>
            </router-link>
            <router-link to="/aboutus" class="nav__link" exact-active-class="nav__link_active">
                О проекте
                <div></div>
            </router-link>
        </nav>
    </header>
    <div class="sortAndSearch" :class="{sortAndSearchHide: isSearchHide}" v-if="isSearchSort">
        <div class="search__input">
            <span class="symbol_input"></span> <my-input placeholder="Искать в постах" class="input-main" @input="$emit('input', $event.target.value)"></my-input>
        </div>
        Сортировать: <my-select class="select-main" @select="$emit('select', $event)"></my-select>
    </div>
    <my-button class="hideSearch" :class="{hideSearchHidden: isSearchHide}" @click="hideSearch" v-if="isSearchSort" :hideSearch="isSearchHide"></my-button>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError}"></Info>
</template>

<script>

import Info from '../Info/Info.vue'
import MakeRequest from '../../API/Request.js'
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: 'header-block',
    components: {
        Info
    },
    props:
    {
        isProfile: Boolean,
        isSearchSort: Boolean,
    },
    data()
    {
        return {
            isSearchHide: false,
            isAuthoized: false,
            isLoad: false,
            userIcon: "",
            status_error: "",
            title_error: "",
            isError: false,
            isInfo: false
        }
    },
    methods:
    {
        hideSearch()
        {
            this.isSearchHide = !this.isSearchHide
        },

        async isAuthor()
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

                if(/2../.test(String(response.status)))
                {
                    this.isLoad = true
                    this.isAuthoized = true
                    this.userIcon = `${BASE_URL}/api/${response.user_data.persPhotodata}` //QW
                }
            }
            else
            {
                this.isLoad = true
            }
        },

        exitProfile()
        {
            this.isAuthoized = false
            document.cookie = `session_token=Bearer ${document.cookie.split(/Bearer /)[1]}; path=/; expires=${new Date(Date.now() - 1000).toUTCString()}`
        }
    },

    mounted()
    {
        this.isAuthor()
    }
}

</script>

<style scoped>

    header
    {
        width: 100%;
        height: 34vh;
        position: relative;
        background-color: white;
        z-index: 1;
    }

    .prifle_exit_link{
        cursor: pointer;
    }

    .shadow
    {
        box-shadow: 0px 10px 25px 0px rgba(0, 0, 0, 0.08);
    }

    .profile
    {
        width: 100%;
        height: 26%;
        display: flex;
        justify-content: right;
        align-items: center;
    }

    .profile__icon
    {
        height: 70px;
        width: 70px;
        border-radius: 50%;
        overflow: hidden;
    }

    .profile__icon > img
    {
        width: 70px;
        height: 70px;
        position: relative;
    }

    .profile__icon__standart
    {
        height: 70px;
        width: 70px;
        border-radius: 50%;
        overflow: hidden;
        background-color: #8C3CFF;
    }

    .profile__icon__standart > img
    {
        width: 60px;
        height: 60px;
        position: relative;
        top: 10px;
        left: 5px;
    }

    .profile__link
    {
        margin-left: 10px;
        color: #4301A1;
        font-size: 1.6em;
        margin-right: 20px;
        display: flex;
        flex-direction: column;
    }

    .header_regist .profile__link
    {
        display: none;
    }

    .profile__link > a
    {
        text-decoration: none;
    }

    .logo
    {
        width: 100%;
        height: 58%;
        display: flex;
        align-items: center;
    }

    .logo__ncfu
    {
        height: 88%;
        width: 12%;
        margin-left: 4%;
        margin-right: 4%;
    }

    .logo__studposts
    {
        height: 90%;
        width: 71%;
    }

    nav
    {
        width: 100%;
        height: 16%;
        display: flex;
        align-items: center;
    }

    .nav__link
    {
        width: 15%;
        height: 100%;
        font-size: 1.8em;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        left: 6%;
        margin-left: 2%;
        text-decoration: none;
        color: black;
    }

    .nav__link_active
    {
        color: #8C3CFF;
    }

    .nav__link> div
    {
        width: 100%;
        height: 2px;
        background-color: #C9C9C9;
        position: absolute;
        bottom: 0;
        border-radius: 2.5px;
    }

    .nav__link_active> div
    {
        background-color: #8C3CFF;
    }

    .sortAndSearch
    {
        width: 100%;
        height: 6vh;
        top: 0;
        display: flex;
        justify-content: right;
        align-items: center;
        background-color: white;
        border-top: 1px solid #C9C9C9;
        font-size: 1.4em;
        box-shadow: 0px 10px 25px 0px rgba(0, 0, 0, 0.08);
        position: relative;
        transition: top 0.3s;
        z-index: 0;
    }

    .sortAndSearchHide
    {
        top: -6vh;
    }

    .search__input
    {
        width: 18%;
        height: 60%;
        background-color: #F3F3F3;
        border-radius: 30px;
        display: flex;
        align-items: center;
        margin-right: 20px;
    }

    .search__input> span
    {
        width: 12%;
        height: 80%;
        margin-left: 5%;
        display: inline-block;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        vertical-align: middle;
        position: relative;
        background-image: url('@/assets/header/search.svg');
    }





</style>
