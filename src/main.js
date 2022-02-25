// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import Vuex from 'vuex'
Vue.use(Vuex)

import axios from 'axios'
import VueAxios from "vue-axios";
axios.defaults.baseURL = "/api"
axios.defaults.withCredentials = true
Vue.use(VueAxios,axios);

import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import * as showdown from 'showdown'

Vue.config.productionTip = false
Vue.use(ElementUI);
// 配置showdown
Vue.prototype.converter = new showdown.Converter()

// Create a new store instance.
const store = new Vuex.Store({
  state: {
    count: 0,
    navigation : ["博客"],
    content : 0 ,//0为查看文章，1为查看图表
  },
  mutations: {
    increment (state) {
      state.count++
    },
    postSelected(state,name){
      state.navigation.push(name)
    },
    getCharts(state){
      state.navigation.push("数据统计")
      state.content = 1
    }
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,//挂载
  components: { App },
  template: '<App/>',
  render: h=>h(App), //由Element教程引入
  store              //vuex中的store
})
