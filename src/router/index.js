import Vue from 'vue'
import Router from 'vue-router'
import Home from "../pages/Home";
// import HelloWorld from '@/components/HelloWorld'
// import Head from "../components/Head";

//注册组件
Vue.use(Router)

//创建路由实例并export
export default new Router({
  routes: [
    {//映射关系
      path: '/',
      redirect: '/home',
    },
    {
      path: '/home',
      name: 'Home',
      component: Home //路由组件
    }
  ]
})
