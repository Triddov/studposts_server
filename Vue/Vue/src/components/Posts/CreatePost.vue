<template>
    <Header :isProfile="true"></Header>
    <div class="createpost">
        <h1>
            Публикация
        </h1>
        <div class="params">
            <div class="entertitle">
                <div class="title">
                    Придумайте название публикации <my-question>Введите название своей интереснейшей публикации</my-question>
                </div>
                <div class="input_block"><my-input placeholder="Какие места стоит посетить на отпуске ?" class="input-post" v-model="title" :limit="200" @input="saveStorage"></my-input></div>
            </div>
            <div class="entercontent">
                <div class="title">
                    Добавьте содержание для публикации <my-question>Поделитесь своими мыслями!</my-question>
                </div>
                <img />
                <div class="input_block"><my-textarea :limit="5000" placeholder="Отпуск - это прежде всего ответственная задача..." class="textarea-createpost" v-model="content" @input="saveStorage"></my-textarea></div>
            </div>
            <div class="entertags">
                <div class="title">
                    Укажите категории для поста <my-question>Помогите читателям найти вашу публикацию по тегам</my-question>
                </div>
                <div class="input_block"><my-input placeholder="отдых отпуск планирование..." class="input-post"  v-model="tags" :limit="100" @input="saveStorage"></my-input></div>
            </div>
            <div class="enterpicture">
                <div class="title">
                    Добавьте картинку для поста <my-question>Все любят красочные картинки. Добавьте одну, чтобы больше заинтересовать читателя</my-question>
                </div>
                <div :class="{'input-createpost-picture-container' : !userPhoto, 'input-createpost-picture-container-ready' : userPhoto}">
                    <AddPhoto v-model="userPhoto" :isPost="true" v-show="!userPhoto"></AddPhoto>
                    <Photo v-show="userPhoto" :picture="userPhoto" @deletePhoto="userPhoto = $event" @changePhoto="userPhoto = $event"></Photo>
                </div>
            </div>
            <my-button class="button_create" @click="createPost">Добавить публикацию</my-button>
        </div>
    </div>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Header from '../Parts/Header.vue'
import Footer from '../Parts/Footer.vue'
import AddPhoto from '../Parts/AddPhoto.vue'
import Photo from '../Parts/Photo.vue'
import Info from '../Info/Info.vue'
import MakeRequest from '../../API/Request.js'
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: 'create-post',
    components: {
        Header,
        Footer,
        AddPhoto,
        Photo,
        Info
    },
    data()
    {
        return {
            title: '',
            content: '',
            tags: '',
            picture: '',
            userPhoto: "",
            isError: false,
            isInfo: false,
            status_error: "",
            title_error: ""
        }
    },

    methods:
    {
        async createPost()
        {
            if(this.title == '' || this.content == '' || this.tags == '')
            {
                this.status_error = "Ошибка"
                this.title_error = "Введены не все данные"
                this.isInfo = true
                this.isError = true
                return
            }

            let response;
            try{
                const url = `${BASE_URL}/api/create_post`;
                const params = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": document.cookie.split('session_token=')[1]
                    },
                    body: JSON.stringify({
                        title: this.title,
                        content: this.content,
                        tags: this.tags,
                        image_data: this.userPhoto || null
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
                localStorage.removeItem('post_info')
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

        saveStorage()
        {
            localStorage.setItem('post_info', JSON.stringify({title: this.title, content: this.content, tags: this.tags}))
        },

        getElemStorage()
        {
            if(localStorage.getItem('post_info'))
            {
                this.title = JSON.parse(localStorage.getItem('post_info')).title
                this.content = JSON.parse(localStorage.getItem('post_info')).content
                this.tags = JSON.parse(localStorage.getItem('post_info')).tags
            }
        }
    },

    mounted()
    {
        this.getElemStorage()
    }
}

</script>

<style scoped>

    .createpost
    {
        width: 53%;
        height: 215vh;
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
        width: 75%;
        height: 90%;
        display: flex;
        flex-direction: column;
        padding-top: 4%;
        border-top: 1px solid #E7E7E7;
    }

    .entertitle, .entertags
    {
        width: 100%;
        height: 6%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 6%;
    }

    .input_block
    {
        width: 100%;
        height: 25%;
        display: flex;
        align-items: center;
        background-color: #F3F3F3;
        border-radius: 30px;
        display: flex;
    }

    .title
    {
        color: #515151;
        font-size: 1.5em;
        padding-left: 5px;
        display: flex;
        position: relative;
        align-items: center;
    }

    .entertitle > .input_block, .entertags > .input_block
    {
        height: 52%;
    }

    .entercontent
    {
        width: 100%;
        height: 40%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-top: 6%;
    }

    .entercontent> .input_block
    {
        height: 91%;
        align-items: flex-start;
    }

    .enterpicture
    {
        width: 100%;
        height: 30%;
        display: flex;
        flex-direction: column;
        margin-top: 6%;
    }

    .input-createpost-picture-container
    {
        width: 45%;
        height: 50%;
        border-radius: 15px;
        position: relative;
        top: 25%;
        left: 27.5%;
    }

    .input-createpost-picture-container-ready
    {
        width: 100%;
        height: 93%;
        top: 1%;
        position: relative;
    }

</style>
