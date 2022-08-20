import { createApp } from 'vue'
import Antd from 'ant-design-vue';
import App from './App.vue'
import Graph from 'antv-x6-vue'
// import App from './App';
import 'ant-design-vue/dist/antd.css';
import { notification } from 'ant-design-vue';
import { io } from "socket.io-client";
import { ViewStore,CurrentStateStore } from '@/store';
let origin_url: string = window.location.origin
const app = createApp(App)
if (process.env.NODE_ENV == 'development') {
  origin_url = 'http://localhost:5000/'

}
const socket = io(origin_url, {
  withCredentials: true,
  extraHeaders: {
    'Access-Control-Allow-Credentials': true,
  },
  allowEIO3: true,
});

socket.on('emitResult', (data: any) => {
  ViewStore.addLog(data)
})
CurrentStateStore.apiurl = origin_url
notification.config({
  // placement: 'bottomRight',
  bottom: '50px',
  duration: 30,
  maxCount:1,
});
// ts模式下会报错vue3支持use直接传递PluginInstallFunction
// app.use(Graph)
app.use(Graph.install)
  .use(Antd)  
  .mount('#app')


