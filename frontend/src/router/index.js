import Vue from 'vue'
import VueRouter from 'vue-router'
import IndexView from '@/views/Index.vue'

Vue.use(VueRouter)

const routes = [
  {
      path: '/',
      name: 'IndexView',
      component: IndexView
  },
  {
    path: '/hist',
    name: 'HistoricoView',
    component: () => import('../views/Historico.vue')
  },
  {
    path: '/eventos',
    name: 'EventosView',
    component: () => import('../views/Evento.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
