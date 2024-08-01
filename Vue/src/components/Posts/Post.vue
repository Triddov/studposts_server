<template>
    <Header></Header>
    <div class="post">
        <div class="postinfo">
            <Date :pdate="this.date" v-if="this.date"></Date><my-operation :id="this.$route.params.id" :isPost="true" :operation="this.post.operations" v-if="this.post.operations"></my-operation>
        </div>
        <h1 class="posttitle">
            <span>"</span>{{this.post.title}}<span>"</span>
        </h1>
        <div class="tags">
            {{this.post.tags}}
        </div>
        <div class="profile">
            <img :src="userIcon"/>
            <div class="profile-name">
                {{this.user_data.surName}} {{this.user_data.firstName}} {{this.user_data.middleName}}
            </div>
        </div>
        <div class="pictures" v-if="this.post.imageData">
            <img :src="this.post.imageData"/>
        </div>
        <div class="content">
            {{this.post.content}}
        </div>
        <div class="rates">
                <span class="info__icon_char info__icon_char_view"></span> {{this.post.viewCount}} / <span class="info__icon_char info__icon_char_like" :class="{info__icon_char_like: this.post.reaction != 'like', info__icon_char_like_action: this.post.reaction == 'like'}" @click="like" ref="like"></span><Vue3Lottie :animationData="animLikes" style="display: none" ref="anim"></Vue3Lottie> {{this.post.likesCount}} / <span class="info__icon_char info__icon_char_dislike" :class="{info__icon_char_dislike: this.post.reaction != 'dislike', info__icon_char_dislike_action: this.post.reaction == 'dislike'}" @click="dislike" ref="dislike"></span> {{this.post.dislikesCount}}
        </div>
    </div>
    <div class="sort">
        Сортировать по: <my-select class="select-main" @select="filterBy"></my-select>
    </div>
    <div class="create-comments">
        <my-input placeholder="Поделитесь своим мнением...." class="input-createcomment" v-model="commentContent" :limit="5000" ref="input"></my-input>
        <div class="public">
            <span :class="{active_er: commentContent.length >= 5000}">
                {{commentContent.length}}/5000
            </span>
            <my-button class="button-createcomment" @click="addComment">Добавить комментарий</my-button>
        </div>
    </div>
    <div class="comments-list">
        <Comment v-for="comment in comments" :key="comment.unique_id" :comment="comment" @remove="removeComment" @reply="replyComment"></Comment>
    </div>
    <my-button class="more-comments" @click="getNewComments"><span v-if="!loadMore">Еще комментарии</span><Vue3Lottie :animationData="animLoad" v-else></Vue3Lottie></my-button>
    <Info :status="status_error" :title="title_error" v-model="isInfo" v-if="isInfo" :class="{Error: isError, Atent: !isError}"></Info>
    <Footer></Footer>
</template>

<script>

import Header from '@/components/Parts/Header.vue'
import Footer from '@/components/Parts/Footer.vue'
import Comment from '@/components/Posts/Parts/Comment.vue'
import Date from '@/components/Posts/Parts/Date.vue'
import { Vue3Lottie } from 'vue3-lottie'
import animLikes from '@/assets/post/data.json'
import animLoad from '@/assets/post/loadsmall.json'
import Info from '@/components/Info/Info.vue'

export default {
    name: "post-block",
    components: {
        Header,
        Footer,
        Comment,
        Date,
        Vue3Lottie,
        Info
    },

    data()
    {
        return {
            post: {},
            date: '',
            comments: [],
            page: 1,
            commentContent: '',
            totalComments: Number,
            animLikes,
            filter: '',
            loadMore: false,
            animLoad,
            status_error: '',
            title_error: '',
            isError: false,
            isInfo: false,
            userIcon: '',
            user_data: {},
        }
    },

    methods: 
    {
        async getPostInfo()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/post/${this.$route.params.id}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authorization": document.cookie.split('session_token=')[1]	
                    }
                }
            )
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = await response.json()
            data.post.imageData = `${process.env.VUE_APP_BASE_URL}/${data.post.imageData}`
            data.post.user_data.persPhotoData = `${process.env.VUE_APP_BASE_URL}/${data.post.user_data.persPhotoData}`
            this.post = data.post
            this.date = this.post.createdAt
            console.log(this.post)
            this.user_data = this.post.user_data
            this.userIcon = this.post.user_data.persPhotoData //QW
        },

        async getStartComments()
        {
            this.loadMore = true
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/comments/${this.$route.params.id}?limit=3&page=${this.page}&orderByDate=${this.filter}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authorization": document.cookie.split('session_token=')[1]	
                    }
                })
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            this.page+=1;
            const data = await response.json()
            this.totalComments = data.totalComments
            this.comments = data.comments
            this.loadMore = false
        },

        async getNewComments()
        {
            this.loadMore = true
            if(Math.ceil(this.totalComments / 3) >= this.page)
            {
                const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/comments/${this.$route.params.id}?limit=3&page=${this.page}&orderByDate=${this.filter}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        "Authorization": document.cookie.split('session_token=')[1]	
                    }
                })
                this.page+=1
                const data = await response.json()
                data.comments.forEach( post => {
                    this.comments.push(post)
                })
                if(!response)
                {
                    this.status_error = "Ошибка"
                    this.title_error = "Запрос не прошел"
                    this.isInfo = true
                    this.isError = true
                    return
                }
                if(data.status)
                {
                    this.loadMore = false
                }
            }
            else
            {
                this.status_error = "Внимание"
                this.title_error = "Комментариев больше нет"
                this.isInfo = true
                this.isError = false
                this.loadMore = false
            }
        },

        async getOneComments()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/comments/${this.$route.params.id}?limit=1`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": document.cookie.split('session_token=')[1]	
                }
            })
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = await response.json()
            data.comments.forEach( post => {
                this.comments.unshift(post)
            })
        },

        async addComment()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/add_comment/${this.$route.params.id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": document.cookie.split('session_token=')[1]	
                },
                body: JSON.stringify({
                    content: this.commentContent
                })
            })
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.commentContent = ""
                this.getOneComments()
            }
        },

        removeComment(comment)
        {
            this.comments = this.comments.filter( item => item.unique_id !== comment.unique_id)
        },

        replyComment(comment)
        {
            this.commentContent = `@${comment}, `
            document.getElementsByClassName("input-createcomment")[0].focus()
        },

        filterBy(select)
        {
            this.comments = []
            this.filter = select
            this.page = 1
            this.getStartComments()
        },

        async like()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/rate/${this.$route.params.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": document.cookie.split('session_token=')[1]
                },
                body: JSON.stringify({
                    action: "like"
                })
            })
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.getRates()
            }
        },

        async dislike()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/rate/${this.$route.params.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": document.cookie.split('session_token=')[1]	
                },
                body: JSON.stringify({
                    action: "dislike"
                })
            })
            if(!response)
            {
                this.status_error = "Ошибка"
                this.title_error = "Запрос не прошел"
                this.isInfo = true
                this.isError = true
                return
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.getRates()
            }
        },

        async getRates()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/get_rates/${this.$route.params.id}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": document.cookie.split('session_token=')[1]
                }
            })
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.post.likesCount = data.likes_count
                this.post.dislikesCount = data.dislikes_count
                this.post.reaction = data.reaction
            }
        }
    },

    mounted()
    {
        this.getPostInfo()
        this.getStartComments()
    }   
}
</script>

<style scoped>
    .post
    {
        width: 70%;
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

    .postinfo
    {
        width: 95%;
        display: flex;
        justify-content: right;
        align-items: center;
        font-size: 1.5em;
        color: #CECECE;
        margin-top: 40px;
    }

    .posttitle
    {
        width: 95%;
        color: #303030;
        font-size: 4.3em;
        margin-top: 20px;
    }

    .tags
    {
        width: 95%;
        color: #7C7C7C;
        font-size: 1.5em;
        margin-top: 10px;
    }

    .profile
    {
        width: 30%;
        height: 12.5vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        margin-top: 40px;
    }

    .profile > img
    {
        width: 17.5%;
        border-radius: 100%;
    }

    .profile-name
    {
        font-size: 1.5em;
        color: #7C7C7C;
    }

    .pictures > img {
        width: 100%;
        border-radius: 5%;
    }

    .pictures
    {
        width: 85%;
        margin-top: 40px;
        border-radius: 50px;
        background-color: #f5f5f5;
    }

    .content
    {
        width: 85%;
        font-size: 1.7em;
        color: #303030;
        margin-top: 60px;
        tab-size: 10px;
        word-break: break-all;
    }

    .rates
   {
        width: 90%;
        height: 60px;
        display: flex;
        justify-content: right;
        align-items: center;
        color: #CECECE;
        font-size: 1.4em;
        font-weight: 900;
        margin-top: 30px;
        margin-bottom: 30px;
   }

   .info__icon_char
   {
        display: inline-block; /* Сделать span блочным элементом */
        width: 60px; /* Ширина иконки */
        height: 60px; /* Высота иконки */
        background-size: cover; /* Растянуть изображение по размерам блока */
        background-repeat: no-repeat; /* Не повторять изображение */
        /* Дополнительные стили для красоты */
        background-position: center; /* Выравнивание по вертикали */
        vertical-align: middle;
        position: relative;
   }

   .info__icon_char_view
   {
        background-image: url('@/assets/post/view.svg'); /* Путь к изображению */
   }

   .info__icon_char_like
   {
        background-size: 200%;
        background-image: url('@/assets/post/like_before.svg'); /* Путь к изображению */
        position: relative;
        top: -6px;
   }

   .info__icon_char_dislike
   {
        background-image: url('@/assets/post/dislike_before.svg'); /* Путь к изображению */
   }

   .info__icon_char_like_action
   {
        background-size: 200%;
        background-image: url('@/assets/post/like_after.svg'); /* Путь к изображению */
        position: relative;
        top: -6px;
   }

   .info__icon_char_dislike_action
   {
        background-image: url('@/assets/post/dislike_after.svg'); /* Путь к изображению */
   }

   .sort
   {
        width: 70%;
        height: 7vh;
        position: relative;
        left: 15%;
        display: flex;
        justify-content: right;
        align-items: center;
        font-size: 1.5em;
        color: #CECECE;
        margin-top: 40px;
        background-color: white;
        border-radius: 3.5vh;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
   }

   .sort > .select-main
   {
        width: 22%;
   }

   .create-comments
   {
        width: 70%;
        height: 23vh;
        position: relative;
        left: 15%;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        color: #CECECE;
        margin-top: 40px;
        border-radius: 3.5vh;
        background-color: white;
        box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
   }

   .create-comments > .public
   {
        width: 90%;
        height: 29%;
        display: flex;
        justify-content: right;
        align-items: center;
   }

   .public > span
   {
        font-size: 1.5em;
        margin-right: 20px;
   }

   .active_er
   {
        color: red;
   }

   .comments-list
   {
        width: 70%;
        position: relative;
        left: 15%;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
   }

</style>