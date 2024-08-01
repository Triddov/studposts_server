<template>
    <div class="info" @click.self="close">
        <div class="infoBlock">
            <div class="status">
                {{ this.status }}
            </div>
            <div class="title">
                {{ this.title }}
            </div>
            <div class="image">

            </div>
            <my-button class="closeinfo" @click="close"> 
            </my-button>
        </div>
    </div>
</template>

<script>

export default {
    name: 'my-info',
    props:
    {
        status: String,
        title: String,
        modelValue: Boolean,
    },
    methods:
    {
        close()
        {
            this.$emit('update:modelValue', false)
        }
    }
}

</script>

<style scoped>
    .info
    {
        width: 100%;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.3);
        position: fixed;
        display: flex;
        justify-content: center;
        align-items: center;
        top: 0;
        z-index: 2;
    }

    .infoBlock
    {
        width: 25%;
        min-height: 20%;
        max-height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        border-radius: 20px;
        background-color: white;
        position: fixed;
    }

    .status
    {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2em;
        color: rgb(117, 28, 105);
    }

    .Error .status
    {
        color: #FF5C76;
    }

    .Atent .status
    {
        color: #AF5CFF;
    }

    .image
    {
        width: 50px;
        height: 50px;
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }

    .Error .image
    {
        background-image: url('@/assets/info/error.svg');
    }

    .Atent .image
    {
        background-image: url('@/assets/info/info-icon.svg');
    }

    .title
    {
        width: 90%;
        display: flex;
        font-size: 1.5em;
        color: #303030;
    }

</style>