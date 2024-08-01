import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import UI from './components/UI'
import Vue3Lottie from 'vue3-lottie'

const app = createApp(App)

UI.forEach(component => {
    app.component(component.name, component)
})


app.use(Vue3Lottie).use(router).mount('#app')
