<template>
    <div class="operation">
        <div class="operations">
            <div class="operations_block" @click="$router.push(`/home/editpost/${this.id}`)" v-if="isPost && operation.update">
                <img src="@/assets/operations/edit.svg"/> Изменить
            </div>
            <div class="operations_block" @click="deletePost" v-if="isPost && operation.delete">
                <img src="@/assets/operations/delete.svg"/> Удалить
            </div>
            <div class="operations_block" @click="$emit('redact')" v-if="isComment && operation.update">
                <img src="@/assets/operations/edit.svg"/> Изменить
            </div>
            <div class="operations_block" @click="deleteComment" v-if="isComment && operation.delete">
                <img src="@/assets/operations/delete.svg"/> Удалить
            </div>
            <div class="operations_block" v-if="operation.ban" @click="banIP">
                <img src="@/assets/operations/blockuser.svg"/> Заблокировать
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "my-operation",
    props:
    {
        id: String,
        modelValue: Boolean,
        isPost: Boolean,
        isComment: Boolean,
        operation: Object
    },
    methods:
    {
        async deletePost()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/deletePost/${this.id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": document.cookie.split('session_token=')[1]	
                },
            })
            if(!response)
            {
                alert("Error")
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.$emit('remove')
                this.$router.push('/home')
            }
            else
            {
                alert(data.message)
            }
        },

        async deleteComment()
        {
            console.log(this.id)
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/delete_comment/${this.$route.params.id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": document.cookie.split('session_token=')[1]	
                },
                body: JSON.stringify({
                    comment_id: this.id
                })
            })
            if(!response)
            {
                alert("Error")
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                this.$emit('remove')
            }
            else
            {
                alert(data.message)
            }
        },

        async banIP()
        {
            const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/ban_ip`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
            })
            if(!response)
            {
                alert("Error")
            }
            const data = await response.json()
            if(/2../.test(String(data.status)))
            {
                alert(data.message)
            }
            else
            {
                alert(data.message)
            }
        }
    }
}
</script>

<style scoped>  
    .operation
    {
        width: 10px;
        height: 30px;
        position: relative;
        margin-left: 20px;
        background-image: url('@/assets/operations/options.svg');
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        cursor: pointer;
        font-size: 0.9em;
    }

    .operation > img
    {
        width: 100%;
        height: 100%;
    }

    .operation:hover > .operations
    {
        opacity: 1;
        z-index: 2;
    }

    .operations
    {
        width: 15vw;
        border-radius: 30px;
        background-color: #F8F8F8;
        overflow: hidden;
        position: absolute;
        top: 0;
        left: -15vw;
        display: flex;
        flex-direction: column;
        opacity: 0;
        z-index: -1;
        transition-duration: 0.2s;
    }

    .operations_block
    {
        width: 100%;
        height: 4.6vh;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding-left: 10px;
        transition-duration: 0.2s;
        color: #303030;
    }

    .operations_block > img
    {
        width: 2vw;
        height: 4vh;
        margin-right: 20px;
    }

    .operations_block:hover
    {
        background-color: #E7E7E7;
    }

    .operations_block:active
    {
        transition-duration: 0.1s;
        background-color: #cecece;
    }

</style>