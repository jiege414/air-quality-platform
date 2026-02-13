import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Ranking from '../views/Ranking.vue'
import History from '../views/History.vue'
import Compare from '../views/Compare.vue'
import Warning from '../views/Warning.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/ranking',
    name: 'Ranking',
    component: Ranking
  },
  {
    path: '/history',
    name: 'History',
    component: History
  },
  {
    path: '/compare',
    name: 'Compare',
    component: Compare
  },
  {
    path: '/warning',
    name: 'Warning',
    component: Warning
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
