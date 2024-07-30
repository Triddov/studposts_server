<template>
    <button><slot></slot></button>
</template>

<script>

export default {
    name: 'my-button',
}
</script>

<style scoped>
    button
    {
        cursor: pointer;
    }

    .addButton
   {
        width: 150px;
        height: 150px;
        border-radius: 100%;
        border: 4px dotted #ad79f0;
        margin-top: 30px;
        cursor: pointer;
        background-color: transparent;
   }

    .hideSearch
    {
        position: relative;
        top: 0;
        left: 47.5%;
        width: 5%;
        height: 50px;
        background-image: url('@/assets/header/dropout.svg');
        background-size: 100% 100%;
        background-color: rgba(0, 0, 0, 0);
        border: none;
        transform: rotate(180deg);
        transition: 0.3s;
    }

    .hideSearchHidden
    {
        transform: rotate(0);
        top: -6vh;
    }
   
   .content__image
   {
        width: 90%;
        max-height: 243px;
        border-radius: 30px;
        margin-top: 50px;
        overflow: hidden;
        position: relative;
        border: none;
        cursor: pointer;
   }

    .morePost
    {
        width: 252px;
        height: 60px;
        border-radius: 30px;
        font-size: 1.6em;
        border: none;
        background-color: white;
        margin-top: 60px;
        transition-duration: 0.1s;
        cursor: pointer;
        box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.2);
    }

    .morePost:hover
    {
        background-color: #ededed
    }

    .morePost:active
    {
        transition-duration: 0.2s;
        background-color: #b152ff;
        color: white;
    }

    .button_regist
    {
        width: 47%;
        height: 60%;
        background-color: #AC2DFE;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 1.9em;
        transition-duration: 0.2s;
    }

    .button_regist:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button_regist:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .button_auth
    {
        width: 47%;
        height: 60%;
        background-color: #AC2DFE;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 1.9em;
        transition-duration: 0.2s;
    }

    .button_auth:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button_auth:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .button_create
    {
        width: 48%;
        height: 4%;
        background-color: #AC2DFE;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 1.7em;
        transition-duration: 0.2s;
        position: relative;
        left: 26.5%;
        margin-top: 10%;
    }

    .button_create:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button_create:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .button_edit
    {
        width: 48%;
        height: 4%;
        background-color: #AC2DFE;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 1.7em;
        transition-duration: 0.2s;
        position: relative;
        left: 26.5%;
        margin-top: 10%;
    }

    .button_edit:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button_edit:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .button_profile
    {
        width: 43%;
        height: 7%;
        background-color: #AC2DFE;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 1.7em;
        transition-duration: 0.2s;
        position: relative;
        margin-top: 7%;
    }

    .button_profile:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button_profile:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .closeinfo
    {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 7.5%;
        height: 15%;
        border: none;
        background-color: rgba(0, 0, 0, 0);
        background-image: url('@/assets/info/xsymbol.svg');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }

    .button-createcomment
    {
        width: 33%;
        height: 100%;
        background-color: #BE30FF;
        color: white;
        border: none;
        border-radius: 50vh;
        font-size: 1.7em;
        transition-duration: 0.2s;
    }

    .button-createcomment:hover
    {
        background-color: #9323dd;
        color: rgb(212, 212, 212);
    }

    
    .button-createcomment:active
    {
        transition-duration: 0.1s;
        background-color: #65169b;
        color: rgb(167, 167, 167);
    }

    .comment-reply
    {
        font-size: 1.5em;
        color: #7C7C7C;
        border: none;
        background-color: rgba(0, 0, 0, 0);
        margin-right: 20px;
    }

    .more-comments
    {
        width: 20%;
        height: 5.5vh;
        color: #8C3CFF;
        background-color: white;
        border-radius: 2.25vh;
        font-size: 1.5em;
        box-shadow: 0px 5px 10px 0px rgba(0, 0, 0, 0.2);
        border: none;
        margin-top: 100px;
        position: relative;
        left: 40%;
        transition-duration: 0.2s;
    }

    .more-comments:hover
    {
        color: #9323dd;
        background-color: rgb(236, 236, 236);
        box-shadow: 0px 7px 15px 0px rgba(0, 0, 0, 0.2);
    }

    .more-comments:active
    {
        transition-duration: 0.1s;
        color: #65169b;
        background-color: rgb(211, 211, 211);
        box-shadow: 0px 5px 5px 0px rgba(0, 0, 0, 0.2);
    }

</style>
    