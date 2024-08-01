<template>
    <span class="question"><div class="answer"><slot></slot></div></span> 
</template>

<script>

export default {
    name: 'my-question',
}
</script>

<style scoped>
    .question
    {
        display: inline-block;
        height: 20px;
        width: 20px;
        margin-left: 15px;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        vertical-align: middle;
        position: relative;
        background-image: url('@/assets/question/info.svg');
        font-size: 0.8em;
    }

    .answer
    {
        width: 200px;
        padding: 10px;
        position: absolute;
        background-color: rgb(255, 225, 251);
        border-radius: 25px;
        left: 20px;
        display: none;
        transition-duration: 0.5s;
        z-index: 2;
    }

    .question:hover .answer
    {
        display: inline-block;
    }
</style>