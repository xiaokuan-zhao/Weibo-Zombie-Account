import Vue from 'vue'
import Router from 'vue-router'
import Description from '@/components/Description'
import Userinfo from '@/components/Userinfo'
import Index from '@/components/Index'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index,
    redirect: '/home',
    children: [{
      path: 'home',
      name: 'Description',
      component: Description,
    },
    {
      path: '/user/:id',
      name: 'Userinfo',
      component: Userinfo

    }]
  },

]

export default new Router({
  mode: "history",
  routes
})
