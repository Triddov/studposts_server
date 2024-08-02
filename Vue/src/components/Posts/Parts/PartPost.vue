<template>
    <div class="post">
        <div class="info">
            <div>
                <img class="profile__icon" :src="userIcon" /> {{this.post.user_data.surName}} {{this.post.user_data.firstName}} {{this.post.user_data.middleName}}
            </div> 
            <div>
               <Date :pdate="this.date"></Date><my-operation @error="errorOperation" :id="this.post.unique_id" :isPost="true" @remove="$emit('remove', post)" :operation="this.post.operations" v-if="this.post.operations"></my-operation>
            </div>
        </div>
        <div class="title">
            <span>"</span>{{this.post.title}}<span>"</span>
        </div>
        <div class="content__text">
            {{this.content}}
        </div>
        <my-button class="content__image" @click="$router.push(`/post/${this.post.unique_id}`)">
            <img :src="postIcon"/>
            <div></div>
            <div class="button-post">Читать</div>
        </my-button>
        <div class="rates">
            <span class="rates__info">
                <span class="info__icon_char info__icon_char_view"></span> {{this.post.viewCount}} / <span class="info__icon_char info__icon_char_like" :class="{info__icon_char_like: this.post.reaction != 'like', info__icon_char_like_action: this.post.reaction == 'like'}"></span> {{this.post.likesCount}} / <span class="info__icon_char info__icon_char_dislike" :class="{info__icon_char_dislike: this.post.reaction != 'dislike', info__icon_char_dislike_action: this.post.reaction == 'dislike'}"></span> {{this.post.dislikesCount}}
             </span>
        </div>
    </div>
</template>

<script>

import Date from '@/components/Posts/Parts/Date.vue';
import { BASE_URL } from '../../../BaseURL.js'

export default {
    name: "PartPost",
    props: 
    {
          post: Object
    },

    components:
    {
        Date,
    },

    data()
    {
          return {
               date: this.post.createdAt,
               content: "",
               userIcon: `${BASE_URL}/api/${this.post.user_data.persPhotoData}`,
               postIcon: `${BASE_URL}/api/${this.post.imageData}`
          }
    },

    methods:
    {
          handdleContent()
          {
               if(this.post.content.length > 100)
               this.content = this.post.content.substr(0, 100) + "...";
               else
               this.content = this.post.content
          },
          errorOperation(status, message)
          {
               this.$emit('error', status, message)
          } 
    },

    mounted()
    {
          this.handdleContent();
    },
}
</script>

<style scoped>

     .profile__icon{
          border-radius: 100%;
     }

     .post
     {
          width: 1000px;
          background-color: white;
          margin-top: 60px;
          border-radius: 50px;
          display: flex;
          flex-direction: column;
          align-items: center;
          box-shadow: 0px 10px 15px 0px rgba(0, 0, 0, 0.2);
     }

   .post> .info
     {
          width: 90%;
          height: 71px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          font-size: 1.2em;
          margin-top: 40px;
     }

   .post> .info> div:nth-child(1)
   {
        display: flex;
        align-items: center;
        font-size: 1.4em;
   }

   .post> .info> div:nth-child(1)> img
   {
        width: 71px;
        height: 71px;
        margin-right: 15px;
   }

   .post> .info> div:nth-child(2)
   {
        display: flex;
        align-items: center;
        color: #CECECE;
        font-size: 1.2em;
   }

   .post> .title
   {
        width: 80%;
        font-size: 2.3em;
        align-items: right;
        font-weight: 700;
        margin-top: 40px;
        font-family: "Montserrat", sans-serif;
   }

   .post> .content__text
   {
        width: 70%;
        font-size: 1.8em;
        margin-top: 40px;
        word-break: break-all;
   }

   .post> .content__image> img
   {
        width: 100%;
   }

   .button-post
    {
        width: 252px;
        height: 60px;
        border-radius: 30px;
        font-size: 1.6em;
        position: absolute;
        border: none;
        background-color: white;
        left: calc(50% - 126px);
        bottom: 0px;
        color: #8C3CFF;
        font-weight: 700;
        opacity: 0;
        transition: all .33s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: center;
    }

   .post> .content__image> div:nth-child(2)
   {
        width: 100%;
        height: 100%;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(255, 255, 255, 0.4));
        border-radius: 30px;
        position: absolute;
        opacity: 0.5;
        top: 0;
        transition: opacity 0.33s ease-in-out;
   }

   .content__image:hover > div:nth-child(2)
   {
        opacity: 1;
   }

   .content__image:hover > .button-post
   {
        opacity: 1;
        transform: translateY(-20px);
   }

   .post> .rates
   {
        width: 90%;
        height: 60px;
        display: flex;
        justify-content: right;
        align-items: center;
        color: #CECECE;
        font-size: 1.25em;
        font-weight: 900;
        margin-top: 30px;
        margin-bottom: 30px;
   }

   .info__icon_char
   {
        display: inline-block; /* Сделать span блочным элементом */
        width: 40px; /* Ширина иконки */
        height: 40px; /* Высота иконки */
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
          background-image: url('@/assets/post/like_before.svg'); /* Путь к изображению */
          background-size: 200%;
          position: relative;
          top: -3px;  
   }

   .info__icon_char_like_action
   {
          background-image: url('@/assets/post/like_after.svg'); /* Путь к изображению */
          background-size: 200%;
          position: relative;
          top: -3px;  
   }

   .info__icon_char_dislike
   {
          background-image: url('@/assets/post/dislike_before.svg'); /* Путь к изображению */
   }

   .info__icon_char_dislike_action
   {
          background-image: url('@/assets/post/dislike_after.svg'); /* Путь к изображению */
   }

   @media (max-width: 1366px)
  {
    .post
    {
        width: 600px;
    }
  }
</style>