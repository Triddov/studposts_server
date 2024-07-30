<template>
  <router-view></router-view>
  <Load class="wait"></Load>
</template>

<script>

import Load from '@/components/Info/Load.vue'

export default {
  name: 'App',
  components:
  {
    Load
  },
  methods:
  {
      closeWait()
      {
        window.onload = () =>
        {
          document.getElementsByClassName('wait')[0].style = "display: none;"
        }
      }
  },
  mounted()
  {
      this.closeWait()
  },
}
</script>

<style>

  *
  {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    outline: 0;
    outline-offset: 0;
    font-family: "Inter", sans-serif;
  }

  #app {
    width: 100%;
    background-image: url("@/assets/main/background.svg");
    background-size: 50%;
    background-repeat: repeat;
    position: relative;
  }

  
  .wait
    {
        width: 20%;
        height: 20%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-radius: 20px;
        background-color: white;
        position: fixed;
        top: 40%;
        left: 40%;
        z-index: 3;
        font-size: 2em;
    }

  @media (max-width: 1745px)
  {
    #app
    {
      font-size: 14px;
    }
  }

  @media (max-width: 1536px)
  {
    #app
    {
      font-size: 12px;
    }
  }

  @media (max-width: 1280px)
  {
    #app
    {
      font-size: 10px;
    }
  }

</style>
