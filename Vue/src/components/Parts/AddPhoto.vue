<template>
    <div class="addPhoto">
        <input class="input-picture" type="file" @change="loadPicture($event)"/>
        <div class="user-post-anim" v-if="isPost">
            <Vue3Lottie :animationData="animPostPhoto"/>
        </div>
        <div v-if="isProfile" class="user-prof-anim">
            <Vue3Lottie :animationData="animProfilePhoto"/>
        </div>
        <img ref="loadPictureContainer" v-show="false" @click="emitPhoto"/>
    </div>
</template>

<script>
import { Vue3Lottie } from 'vue3-lottie'
import animProfilePhoto from '@/assets/regist_auth/profile_anim.json'
import animPostPhoto from '@/assets/PhotoBlocks/stone.json'
export default {
    name: "add-photo",

    props: 
    {
        isProfile: Boolean,
        isPost: Boolean,
        modelValue: String
    },

    components: 
    {
        Vue3Lottie
    },

    data()
    {
        return{
            picture: "",
            animProfilePhoto,
            animPostPhoto
        }
    },

    methods:
    {
        loadPicture(event)
        {   
            let file = event.target.files[0];
            let loadPictureContainer = this.$refs.loadPictureContainer;
            if(file)
            {
                let reader = new FileReader();
                reader.onload = function(e) {
                    loadPictureContainer.src = e.target.result
                    loadPictureContainer.click()
                }; 
                reader.readAsDataURL(file);
            }
        },

        emitPhoto()
        {
            this.$emit('update:modelValue', this.$refs.loadPictureContainer.src)
        }
    },

    watch:
    {

    }
}
</script>

<style scoped>

    .addPhoto
    {
        display: flex;
        width: 100%;
        height: 100%;
        border-radius: 15px;
        border: 3px #E0E0E0 dashed;
        position: relative;
        align-items: center;
        justify-content: center;
    }

    .user-prof-anim{
        width: 55%;
    }

    .addPhoto > .user-post-anim
    {
        position: absolute;
        width: 95%;
        height: 95%;
        top: 2.5%;
        left: 2.5%;
        z-index: 1;
    }

    .addPhoto::after
    {
        content: "Выберите или перетащите";
        position: absolute;
        top: 100%;
        font-size: 1.4em;
        left: 0;
        color: #E0E0E0;
        width: 100%;
        text-align: center;
        margin-top: 10px;
    }

    .input-picture
    {
        cursor: pointer;
        position: absolute;
        width: 100%;
        height: 100%;
        opacity: 0;
        z-index: 2;
    }

</style>