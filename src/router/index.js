import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
import TheNavBar from '@/components/TheNavBar'
import TheP2APage from '@/components/TheP2APage'
Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/home',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/politicians',
      name: 'P2A',
      component: TheP2APage
    },
    {
      path: '/vote',
      name: 'NavPage',
      component: TheNavBar
    },
    {
      path: '/news',
      name: 'NavPage',
      component: TheNavBar
    }
  ]
})
router.replace({ path: '/home', redirect: '/'})

export default router
