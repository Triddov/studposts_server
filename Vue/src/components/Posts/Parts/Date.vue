<template>
    <div>{{this.date}}</div>
</template>

<script>
export default {
    name: "date-block",
    props:
    {
        pdate: String
    },

    data()
    {
        return {
            date: this.pdate,
            months: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
        }
    },

    methods:
    {
        handleDate()
        {
            let date = Date.parse(this.date)
            date = new Date(date)
            date = `${date.getDate()} ${this.months[date.getMonth()]} ${date.getFullYear()} ${date.getHours()}:${date.getMinutes() < 10 ? 0 : ''}${date.getMinutes()}`
            this.date = date
        }   
    },

    mounted()
    {
        this.handleDate()
    }
}
</script>

<style scoped>  

</style>