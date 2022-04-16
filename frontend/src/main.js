import Vue from 'vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue'
import App from './App.vue'
import store from './store'
import VueSocketIO from 'vue-socket.io'
Vue.config.productionTip = false
Vue.use(Antd)
import VueDraggableResizable from 'vue-draggable-resizable'
// optionally import default styles
import 'vue-draggable-resizable/dist/VueDraggableResizable.css'
Vue.component('vue-draggable-resizable', VueDraggableResizable)
import axios from 'axios'

var origin_url,socketio_cores 

//设置全局变量为$http方便调用
if (process.env.NODE_ENV=="development"){
  origin_url = 'http://localhost:5000/'
  socketio_cores ={
    debug: true,
    credentials: true,
    cors:{
      origin:'http://localhost:8080',
      methods:["GET","POST"]
    },
    extraHeaders: {
      'Access-Control-Allow-Credentials':true
      }
  }
}else{
  origin_url = window.location.origin
  socketio_cores={}
}
Vue.prototype.$apiurl = origin_url

Vue.use(new VueSocketIO({
  connection:origin_url,
  allowEIO3: true,
  vuex: {
      store,
      actionPrefix: 'SOCKET_',
      mutationPrefix: 'SOCKET_'
  },
  ...socketio_cores
}))

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
