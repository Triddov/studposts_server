<template>
    <div class="photo" id="pictureBlock">
        <img src="@/assets/PhotoBlocks/inputpicture.svg" ref="picture" class="picture" @click="emitPhoto" id="picture" crossorigin="anonymous"/>
        <div class="buttons">
            <span class="deletePhoto" @click="deletePhoto"></span>
            <span class="changePhoto" @click="$refs.input.click()"><input type="file" @change="changePhoto" ref="input" style="display: none;"/></span>
        </div>
    </div>
</template>

<script>

export default {
    name: "photo-block",
    props: 
    {
        picture: String
    },

    data()
    {
        return {
            
        }
    },

    methods:
    {
        deletePhoto()
        {
            this.$emit('deletePhoto', '')
        },

        changePhoto()
        {
            this.staticImg = false
            let file = event.target.files[0];
            let picture = this.$refs.picture;
            if(file)
            {
                let reader = new FileReader();
                reader.onload = function(e) {
                    picture.src = e.target.result
                    picture.click()
                }; 
                reader.readAsDataURL(file);
            }
        },

        emitPhoto()
        {
            this.$emit('changePhoto', this.$refs.picture.src)
        }
    },

    watch:
    {
        picture()
        {
            this.$refs.picture.src = this.picture
        },
    }
}
</script>

<style scoped>
    .photo
    {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 30px;
        position: relative;
    }

    .photo > img
    {
        max-width: 100%;
        max-height: 100%;
        transition-duration: 0.2s;
        border-radius: 20px;
    }
    
    .buttons
    {
        width: 250px;
        height: 114px;
        position: absolute;
        top: 55%;
        left: calc(50% - 125px);
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: white;
        border-radius: 30px;
        opacity: 0;
        transition-duration: 0.2s;
        z-index: -1;
    }

    .photo:hover > .picture
    {
        filter: brightness(40%);
        background-color: white;
    }

    .photo:hover > .buttons
    {
        z-index: 2;
        opacity: 1;
        top: calc(50% - 57px);
    }

    .deletePhoto
    {
        width: 64px;
        height: 64px;
        display: inline-block;
        background: url('@/assets/PhotoBlocks/delete.svg') no-repeat;
        background-size: cover;
        transition-duration: 0.2s;
    }

    .deletePhoto:hover
    {
        filter: brightness(70%);
    }

    .changePhoto
    {
        width: 62px;
        height: 64px;
        display: inline-block;
        background: url('@/assets/PhotoBlocks/change.svg') no-repeat;
        background-size: cover;
        transition-duration: 0.2s;
    }

    .changePhoto:hover
    {
        filter: brightness(70%);
    }



</style>