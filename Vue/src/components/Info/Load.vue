<template>
    <div class="load">
        <Vue3Lottie :animationData="animLoad" class="lottie"></Vue3Lottie>
        <div class="info">
            Подождите, идет загрузка...
        </div>
    </div>
</template>

<script>
    import { Vue3Lottie } from 'vue3-lottie'
    import animLoad from '@/assets/info/load.json'

export default {
    name: 'my-button',
    content:
    {
        Vue3Lottie
    },

    data()
    {
        return {
            animLoad
        }
    }
}
</script>

<style scoped>

    .load
    {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        position: fixed;
        z-index: 3;
        top: 0;
        left: 0;
        background-color: white;
    }

    .lottie
    {
        width: 200px;
        height: 200px;
        margin-bottom: 20px;
    }

    .info
    {
        font-size: 1.5em;
        color: #303030;
    }

</style>