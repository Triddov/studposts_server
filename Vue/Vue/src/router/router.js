import { createRouter, createWebHistory } from "vue-router"
import Main from '@/components/Main.vue'
import Posts from '@/components/Posts/Posts.vue'
import Registration from '@/components/Auth_Regist/Registration.vue'
import Authorization from '@/components/Auth_Regist/Authorization.vue'
import CreatePosts from '@/components/Posts/CreatePost.vue'
import EditPost from '@/components/Posts/EditPost.vue'
import Profile from '@/components/Profile/Profile.vue'
import Post from '@/components/Posts/Post.vue'
import AboutUs from '@/components/AboutUs/AboutUs.vue'
import Error from '@/components/Info/Error.vue'
import Load from '@/components/Info/Load.vue'
import Policy from '@/components/Agree/Policy.vue'
import Rules from '@/components/Agree/Rules.vue'

const routes = [
    {
      path: '/home',
      component: Main,
      children: [
          {
            path: '/home',
            component: Posts
          },
          {
            path: '/createpost',
            component: CreatePosts
          },
          {
            path: '/editpost/:id',
            component: EditPost
          },
          {
            path: '/profile',
            component: Profile
          },
          {
            path: '/post/:id',
            component: Post
          }
        ]
    },
    {
      path: '/aboutus',
      component: AboutUs
    },
    {
      path: '/policy',
      component: Policy
    },
    {
      path: '/rules',
      component: Rules
    },
    {
      path: '/auth',
      component: Authorization,
    },
    {
      path: '/regist',
      component: Registration
    },
    {
      path: '/load',
      component: Load
    },
    {
      path: '/error',
      component: Error
    },
    {
      path: '/:catchAll(.*)',
      redirect: '/error'
    }
  ];

const router = createRouter({
    routes,
    history: createWebHistory()
})

export default router