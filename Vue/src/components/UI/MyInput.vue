<template>
    <input :value="modelValue" @input="Input" ref="input"/>
</template>

<script>

export default {
    name: 'my-input',
    props:{
        modelValue: [String, Number],
        limit: Number
    },
    methods:
    {
        
        Input(event)
        {
            if(this.limit)
            {
                if(this.$refs.input.value.length > this.limit)
                {
                    this.$refs.input.value = this.$refs.input.value.substr(0, this.limit)
                }
            }
            this.$emit('update:modelValue', event.target.value)
        },
    },
}
</script>

<style scoped>

    .input-main
    {
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        padding-left: 5px;
        padding-right: 10px;
        font-size: 1em;
        color: #000;
    }

    .input-main::placeholder
    {
        color: #000;
    }

    .input-profile
    {       
        width: 94%;
        height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
        padding-left: 1em;
        padding-right: 1em;
    } 
    
    .input-profile::placeholder
    {
        color: #CECECE
    }

    .input_profile_error{
        color: red;
    }

    .input-profile
    {       
        width: 94%;
        height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
        padding-left: 1em;
        padding-right: 1em;
    } 

    .input-post
    {       
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
        padding-left: 1em;
        padding-right: 1em;
    } 

    .input-post::placeholder
    {
        color: #CECECE
    }
    
    .input-auth::placeholder
    {
        color: #CECECE
    }

    .input-createcomment
    {
        width: 90%;
        height: 29%;
        background-color: #FCFCFC;
        border: none;
        border-bottom: 2px solid #D67DFF;
        font-size: 1.6em;
        padding-left: 1em;
        padding-right: 1em;
        color: #303030;
    }

    .input-createcomment::placeholder
    {
        color: #CECECE
    }

</style>
    