<template>
    <Header :isProfile="true"></Header>
    <div class="editpost">
        <h1>
            Публикация
        </h1>
        <div class="params">
            <div class="entertitle">
                <div class="title">
                    Придумайте название публикации <my-question>Введите название своей интереснейшей публикации</my-question>
                </div>
                <div class="input_block"><my-input placeholder="Какие места стоит посетить на отпуске ?" class="input-post" v-model="title" :limit="200"></my-input></div>
            </div>
            <div class="entercontent">
                <div class="title">
                    Добавьте содержание для публикации <my-question>Поделитесь своими мыслями!</my-question>
                </div>
                <div class="input_block"><my-textarea :limit="5000" placeholder="Отпуск - это прежде всего ответственная задача..." class="textarea-editpost" v-model="content"></my-textarea></div>
            </div>
            <div class="entertags">
                <div class="title">
                    Укажите категории для поста <my-question>Помогите читателям найти вашу публикацию по тегам</my-question>
                </div>
                <div class="input_block"><my-input placeholder="отдых отпуск планирование..." class="input-post"  v-model="tags" :limit="100"></my-input></div>
            </div>
            <div class="enterpicture">
                <div class="title">
                    Добавьте картинку для поста <my-question>Все любят красочные картинки! Добавьте одну, чтобы больше заинтересовать читателя</my-question>
                </div>
                <div :class="{'input-editpost-picture-container' : !userPhoto, 'input-editpost-picture-container-ready' : userPhoto}">
                    <AddPhoto v-model="userPhoto" :isPost="true" v-show="!userPhoto"></AddPhoto>
                    <Photo v-show="userPhoto" :picture="userPhoto" @deletePhoto="userPhoto = $event" @changePhoto="userPhoto = $event"></Photo>
                </div>
            </div>
            <my-button class="button_edit" @click="editpost">Добавить публикацию</my-button>
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
            userPhoto: '',
            post: {},
            isError: false,
            isInfo: false,
            status_error: "",
            title_error: ""
        }
    },

    methods:
    {
        async editpost()
        {
            if(this.title == '' || this.content == '' || this.tags == '')
            {
                this.status_error = "Ошибка"
                this.title_error = "Введены не все данные"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = {
                title: this.title,
                content: this.content,
                tags: this.tags,
                image_data: this.userPhoto || null
            }
            if(/sources/.test(this.userPhoto))
            {
                data.image_data = "alreadyExist"
            }
            try{
                const url = `${BASE_URL}/api/updatePost/${this.$route.params.id}`;
                const params = {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
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

            this.$router.push('/home')
        },

        async getPost()
        {

            let response;
            try{
                const url = `${BASE_URL}/api/post/${this.$route.params.id}`;
                response = await MakeRequest(url);

            //обработка ошибок
            }catch(err){
                this.title_error = err.message;
                this.status_error = err.status;
                this.isInfo = true;
                this.isError = true;
                return;
            }

            this.post = response.post
            this.title = this.post.title
            this.content = this.post.content
            this.tags = this.post.tags
            this.userPhoto = `${BASE_URL}/api/${this.post.imageData}` //QW
        }
    },

    mounted()
    {
        this.getPost()
    }
}

</script>

<style scoped>

    .editpost
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
        height: 18%;
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

    .input-editpost-picture-container
    {
        width: 45%;
        height: 50%;
        position: relative;
        top: 25%;
        left: 27.5%;
    }

    .input-editpost-picture-container-ready
    {
        width: 100%;
        height: 93%;
        top: 1%;
        position: relative;
    }

</style>
