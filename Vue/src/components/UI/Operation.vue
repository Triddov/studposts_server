<template>
    <div class="operation">
        <div class="operations">
            <div class="operations_block" @click="$router.push(`/editpost/${this.id}`)" v-if="isPost && operation.update">
                <img src="@/assets/operations/edit.svg"/> Изменить
            </div>
            <div class="operations_block" @click="deletePost" v-if="isPost && operation.delete">
                <img src="@/assets/operations/delete.svg"/> Удалить
            </div>
            <div class="operations_block" @click="$emit('redact')" v-if="isComment && operation.update">
                <img src="@/assets/operations/edit.svg"/> Изменить
            </div>
            <div class="operations_block" @click="deleteComment" v-if="isComment && operation.delete">
                <img src="@/assets/operations/delete.svg"/> Удалить
            </div>
            <div class="operations_block" v-if="operation.ban" @click="banIP">
                <img src="@/assets/operations/blockuser.svg"/> Заблокировать
            </div>
        </div>
    </div>
</template>

<script>

import MakeRequest from '../../API/Request.js'
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: "my-operation",
    props:
    {
        id: String,
        modelValue: Boolean,
        isPost: Boolean,
        isComment: Boolean,
        operation: Object
    },
    methods:
    {
        async deletePost()
        {
            try{
                const url = `${BASE_URL}/api/deletePost/${this.id}`;
                const params = {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": document.cookie.split('session_token=')[1]	
                    }
                }

                await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                this.$emit('error', err.status, err.message)
            }

            this.$emit('remove')
            this.$router.push('/home')
        },

        async deleteComment()
        {
            try{
                const url = `${BASE_URL}/api/delete_comment/${this.$route.params.id}`;
                const params = {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": document.cookie.split('session_token=')[1]	
                    },
                    body: JSON.stringify({
                        comment_id: this.id
                    })
                }

                await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                this.$emit('error', "Ошибка", 'Соединение потерянно')
                return;
            }

            this.$emit('remove')
        },

        async banIP()
        {
            let response;
            try{
                const url = `${BASE_URL}/api/ban_ip`;
                const params = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    }
                }

                response = await MakeRequest(url, params);

            //обработка ошибок
            }catch(err){
                response = err;
            }

            //Я хуй знает зачем тебе тут возвращать ошибку в случае успеха
            this.$emit('error', response.status, response.message)
        }
    }
}
</script>

<style scoped>  
    .operation
    {
        width: 10px;
        height: 30px;
        position: relative;
        margin-left: 20px;
        background-image: url('@/assets/operations/options.svg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        cursor: pointer;
        font-size: 0.9em;
    }

    .operation > img
    {
        width: 100%;
        height: 100%;
    }

    .operation:hover > .operations
    {
        opacity: 1;
        z-index: 2;
    }

    .operations
    {
        width: 15vw;
        border-radius: 30px;
        background-color: #F8F8F8;
        overflow: hidden;
        position: absolute;
        top: 0;
        left: -15vw;
        display: flex;
        flex-direction: column;
        opacity: 0;
        z-index: -1;
        transition-duration: 0.2s;
    }

    .operations_block
    {
        width: 100%;
        height: 4.6vh;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 10px;
        transition-duration: 0.2s;
        color: #303030;
    }

    .operations_block > img
    {
        width: 2vw;
        height: 4vh;
        margin-right: 20px;
    }

    .operations_block:hover
    {
        background-color: #E7E7E7;
    }

    .operations_block:active
    {
        transition-duration: 0.1s;
        background-color: #cecece;
    }

</style>