<template>
    <textarea :value="modelValue" @input="Input"  ref="input"></textarea>
</template>

<script>

export default {
    name: 'my-textarea',
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
        }
    }
}
</script>

<style scoped>
    textarea
    {
      resize: none;
    }

    .textarea-createpost
    {
        width: 100%;
        min-width: 100%;
        height: 100%;
        min-height: 100%;
        max-height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
        padding: 1em;
    }

    .textarea-createpost::placeholder
    {
        color: #CECECE
    }

    .textarea-editpost
    {
        width: 100%;
        min-width: 100%;
        height: 100%;
        min-height: 100%;
        max-height: 100%;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
        padding: 1em;
    }

    .textarea-editpost::placeholder
    {
        color: #CECECE
    }

    .comment_redact
    {
        width: 90%;
        min-height: 15vh;
        background-color: rgba(0,0,0,0);
        border: none;
        font-size: 1.6em;
    }

</style>
