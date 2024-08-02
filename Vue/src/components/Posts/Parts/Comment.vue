<template>
    <div class="comment">
        <div class="info">
            <div class="profile">
                <img :src="userIcon"/> {{comment.user_data.surName}} {{comment.user_data.firstName}} {{comment.user_data.middleName}}
            </div>
            <div class="operation">
                <Date :pdate="this.comment.createdAt"></Date><my-operation @error="errorOperation" @redact="this.update = true" :isComment="true" :id="this.comment.unique_id" @remove="$emit('remove', comment)" :operation="this.comment.operations" v-if="this.comment.operations"></my-operation>
            </div>
        </div>
        <div class="content" v-if="!update">
            {{content}}
        </div>
        <my-input v-model="this.content_change" :limit="5000" v-if="update" class="comment_redact"><div>{{content}}</div></my-input>
        <div class="button-container">
            <my-button class="comment-reply" v-if="!this.comment.operations" @click="$emit('reply', comment.user_data.firstName)">
                Ответить
            </my-button>
            <my-button class="comment-reply" v-if="this.comment.operations && !update" @click="this.update = true">
                Изменить
            </my-button>
            <my-button class="comment-reply" v-if="update" @click="redactComment">
                Отправить изменения
            </my-button>
            <my-button class="comment-reply" v-if="update" @click="this.update = false; this.content_change = this.comment.content">
                Отменить
            </my-button>
        </div>
    </div>
</template>

<script>

import Date from '@/components/Posts/Parts/Date.vue'
import MakeRequest from '../../../API/Request.js'
import { BASE_URL } from '../../../BaseURL.js'

export default {

    name: "comment-block",
    components: {
        Date
    },
    props:
    {
        comment: Object
    },
    data()
    {
        return {
            content: this.comment.content,
            update: false,
            userIcon: `${BASE_URL}/api/${this.comment.user_data.persPhotoData}`,//this.comment.user_data.persPhotoData,
            content_change: this.comment.content
        }
    },
    methods:
    {
        async redactComment()
        {
            try{
                const url = `${BASE_URL}/api/update_comment/${this.$route.params.id}`;
                const params = {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authorization": document.cookie.split('session_token=')[1]
                    },
                    body: JSON.stringify({
                        comment_id: this.comment.unique_id,
                        content: this.content_change
                    })
                }

                await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                this.$emit('error', err.status, err.message)
                return;
            }

            this.content = this.content_change
            this.update = false
        },

        errorOperation(status, message)
        {
            this.status_error = status
            this.title_error = message
            this.isInfo = true
            this.isError = true
        }
    }
}
</script>

<style scoped>

    .comment
    {
        width: 100%;
        min-height: 33vh;
        background-color: white;
        margin-top: 40px;
        border-radius: 30px;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        padding: 20px 0;
    }

    .info
    {
        width: 90%;
        height: 6.6vh;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .info > .profile
    {
        height: 100%;
        color: #7C7C7C;
        font-size: 1.5em;
        display: flex;
        align-items: center;
        font-style: italic;
    }

    .info > .profile > img
    {
        height: 100%;
        margin-right: 40px;
        border-radius: 50%;
    }

    .info > .operation
    {
        height: 100%;
        color: #CECECE;
        font-size: 1.5em;
        display: flex;
        align-items: center;
    }

    .content
    {
        width: 90%;
        min-height: 8.3vh;
        color: #303030;
        font-size: 1.5em;
        word-break: break-all;
        margin: 20px 0;
        overflow: visible;
    }

    .button-container
    {
        width: 90%;
        display: flex;
        justify-content: right;
    }

</style>
