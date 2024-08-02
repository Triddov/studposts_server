<template>
    <div class="error">
        <img src="@/assets/info/warning.svg"/>
        <div>
            <div class="title">ERROR</div>
            <div class="group">
                <div class="info">
                    Не удалось загрузить запрашиваемый ресурс. Детали:
                </div>
                <div class="content" v-if="this.$route.path == '/error'">
                    Сервер вернул статус 404, сообщение: Not founded
                </div>
                <div class="content" v-else>
                    Ошибка соединения, проверьте подключение к интернету
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'my-button',
    data()
    {
        
    }
}
</script>

<style scoped>

    .error
    {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        background-color: white;
    }

    img
    {
        width: 16vw;
        height: 25vh;
    }

    .title
    {
        font-size: 6em;
        color: #303030;
    }

    .group
    {
        height: 10vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .info
    {
        font-size: 1.5em;
        color: #303030;
    }

    .content
    {
        font-size: 1.5em;
        color: #303030;
    }

</style>