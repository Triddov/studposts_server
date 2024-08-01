<template>
    <Header :isProfile="true" :isSearchSort="true" @select="filterBy" @input="Input"></Header>
    <div class="posts">
        <div class="addPost">
            <h1>
                Делитесь своими идеями, мыслями и историями - всем, о чем сейчас думаете
            </h1>
            <my-button class="addButton" @click="$router.push('/createpost')"><Vue3Lottie :animationData="animButton"/></my-button>
            <h2>
                Добавить публикацию
            </h2>
        </div>
       <PartPost v-for="post in posts" :key="post.unique_id" :post="post" @remove="removePost" @error="errorOperation"></PartPost>

        <my-button class="morePost" @click="getNewPost">
            <span v-if="!loadMore">Еще посты</span><Vue3Lottie :animationData="animLoad" v-else></Vue3Lottie>
        </my-button>
    </div>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError, Atent: !isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Header from '../Parts/Header.vue';
import Footer from '../Parts/Footer.vue';
import { Vue3Lottie } from 'vue3-lottie'
import animButton from '@/assets/main/data.json'
import PartPost from '@/components/Posts/Parts/PartPost.vue';
import animLoad from '@/assets/post/loadsmall.json'
import Info from '../Info/Info.vue'
import MakeRequest from '../../API/Request.js'
import { BASE_URL } from '../../BaseURL.js'

export default {
    name: 'posts-block',
    components: {
        Header,
        Vue3Lottie,
        Footer,
        PartPost,
        Info
    },
    data()
    {
        return {
            animButton,
            posts: [],
            page: 1,
            totalPosts: Number,
            filter: 'disk',
            search: '',
            loadMore: false,
            animLoad,
            isInfo: false,
            status_error: '',
            title_error: '',
            isError: false
        }
    },
    methods: {
        async startPosts()
        {
            if(!sessionStorage.getItem('filter'))
            {
                sessionStorage.setItem('filter', this.filter)
            }
            this.loadMore = true
            let response;
            try{
                const url = `${BASE_URL}/api/allposts?limit=5&page=${this.page}&search=${this.search}&orderByDate=${sessionStorage.getItem('filter')}`;
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
            this.page+=1
            this.totalPosts = data.totalPosts
            this.posts = data.posts;
            this.loadMore = false
        },

        async getNewPost()
        {
            if(!sessionStorage.getItem('filter'))
            {
                sessionStorage.setItem('filter', this.filter)
            }
            this.loadMore = true
            if(Math.ceil(this.totalPosts / 5) >= this.page)
            {
                let response;
                try{
                    const url = `${BASE_URL}/api/allposts?limit=5&page=${this.page}&search=${this.search}&orderByDate=${sessionStorage.getItem('filter')}`;
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
                this.page+=1
                const data = response;
                data.posts.forEach( post => {
                    this.posts.push(post)
                })

                this.loadMore = false
            }
            else
            {
                this.loadMore = false
                this.status_error = "Внимание"
                this.title_error = "Постов не осталось"
                this.isInfo = true
                this.isError = false
            }
        },

        removePost(post)
        {
            this.loadMore = false
            this.status_error = "Внимание"
            this.title_error = "Публикация удалена"
            this.isInfo = true
            this.isError = false
            this.posts = this.posts.filter(p => p.unique_id !== post.unique_id)
        },

        filterBy(select)
        {
            this.posts = []
            this.filter = select
            sessionStorage.setItem('filter', select)
            this.page = 1
            this.startPosts()
        },

        Input(search)
        {
            this.search = search
            this.posts = []
            this.page = 1
            this.startPosts()
        },

        errorOperation(status, message)
        {
        this.status_error = status
        this.title_error = message
        this.isInfo = true
        this.isError = false
        }
    },

    mounted()
    {
        this.startPosts()
    }
}
</script>

<style scoped>

   .posts
   {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
   }

   .addPost
    {
        width: 1000px;
        height: 340px;
        background-color: white;
        border-radius: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
        border: none;
    }

   .addPost> h1
   {
        width: 900px;
        font-weight: 400;
        font-size: 1.7em;
        margin-top: 3%;
        text-align: left;
   }

   .addPost> h2
   {
        font-weight: 400;
        font-size: 1.4em;
        margin-top: 2%;
        color: #8A8989;
   }

   @media (max-width: 1366px)
  {

    .addPost
    {
        width: 600px;
    }

    .addPost> h1
    {
        width: 500px
    }

  }


</style>
