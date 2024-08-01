<template>
    <div>
        <span v-if="checkbox"></span>
    </div>
</template>

<script>

export default {
    name: 'my-checkbox',
    props: 
    {
        checkbox: Boolean
    }
}
</script>

<style scoped>

    .registr_checkbox
    {
        cursor: pointer;
        width: 30px;
        height: 30px;
        background-color: #e9e9e9;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }

    .registr_checkbox > span
    {
        width: 40px;
        height: 40px;
        display: inline-block;
        background-image: url('@/assets/main/check.svg');
        background-size: 100% 100%;
    }

    .registr_checkbox > input
    {
        display: none;
    }

</style>