<template>
    <footer>
        <div class="about">
            <div>
                Проект разработан студентами Северо-Кавказкого Федерального Университета кафедры Инфокоммуникаций в рамках девопс практики от Ростелекома 
            </div>
            <div>
                Обратная связь <a href="mailto:wildcat2k21@gmail.com">wildcat2k21@gmail.com</a>
            </div>
        </div>
        <div class="support">
            <img src="@/assets/main/ncfu.svg"/> <img src="@/assets/main/rostelecom.svg"/> <img src="@/assets/main/infocom.svg"/>
        </div>
        <div class="copyright">
            Ставрополь 2024 год
        </div>
    </footer>
</template>


<script>

export default {
    name: 'footer-block',
}

</script>

<style scoped>
    footer
    {
        margin-top: 100px;
        width: 100%;
        height: 42vh;
        background-color: #F7F7F7;
        position: relative;
        bottom: 0;
        border-top: 2px solid #C7C3C3;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .about
    {
        height: 28%;
        width: 80%;
        color: #454A44;
        font-size: 1.6em;
        display: flex;
        flex-direction: column;
        position: relative;
        justify-content: space-between;
        text-align: center;
        margin-top: 87px;
    }

    .support
    {
        width: 30%;
        height: 23%;
        display: flex;
        justify-content: space-between;
        margin-top: 40px;
    }

    .support> img
    {
        width: 25%;
        height: 100%;
    }

    .support> img:nth-child(3)
    {
        width: 23%;
    }

    .copyright
    {
        color: #3C3C3C;
        margin-top: 40px;
        font-size: 1.25em;
    }
</style>