<template>
    <div>
        <div class="select"> 
            <img src="@/assets/header/dropout.svg"/><div ref="select">Сначало свежие</div>
        </div>
        <div class="select-list">
            <div class="select-elem" @click="select($event, 'disc')">Сначала свежие</div>
            <div class="select-elem" @click="select($event, 'asc')">Сначала старые</div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'my-select',
    methods:
    {
        select(elem, select)
        {
            this.$refs.select.innerText = elem.target.innerText
            this.$emit('select', select)
        }
    }
}
</script>

<style>
    .select-main
    {
        min-width: 15%;
        max-width: 25%;
        height: 60%;
        background-color: #F3F3F3;
        margin-right: 20px;
        margin-left: 20px;
        text-wrap: nowrap;
        position: relative;
        border-radius: 25px;
        border: none;
        transition-duration: 0.3s;
    }

    .select-main> .select
    {
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        display: flex;
        align-items: center;
        padding-left: 5px;
    }

    .select-main> .select> img
    {
        width: 15%;
        height: 90%;
        transition-duration: 0.3s;
    }

    .select-main> .select> div
    {
        width: 80%;
    }

    .select-main> .select-list
    {
        width: 100%;
        height: 0px;
        overflow: hidden;
        position: absolute;
        transition-duration: 0.3s;
        background-color: #F3F3F3;
        border-radius: 0px 0px 15px 15px;
        z-index: 2;
    }

    .select-main> .select-list> .select-elem
    {
        width: 100%;
        height: 4.6vh;
        display: flex;
        align-items: center;
        padding-left: 15px;
        transition-duration: 0.2s;
    }

    .select-elem:hover
    {
        background-color: #E5E5E5;
    }

    .select-main:hover > .select-list
    {
        width: 100%;
        height: 9.2vh;
    }

    .select-main:hover > .select > img
    {
        transform: rotate(180deg);
    }

    
    .select-main:hover
    {
        transition-duration: 0s;
        border-radius: 15px 15px 0px 0px;
    }

</style>
    