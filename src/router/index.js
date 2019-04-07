import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/components/HomePage'
import TheNavBar from '@/components/TheNavBar'
import TheP2APage from '@/components/TheP2APage'
import TheNewsPage from '@/components/TheNewsPage'
import TheVotePage from '@/components/TheVotePage'
import TheTestPage from '@/components/TheTestPage'
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
      name: 'Votepage',
      component: TheVotePage
    },
    {
      path: '/news',
      name: 'News',
      component: TheNewsPage
    },
    {
      path: '/test',
      name: 'Test',
      component: TheTestPage
    }
  ]
})
router.replace({ path: '/home', redirect: '/'})

export default router
