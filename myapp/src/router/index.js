import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/Layout.vue'
import { exportExcel } from '@/utils/exportExcel'
import { exportWord } from '@/utils/exportWord'

const handleExportExcel = () => {
  exportExcel(list.value, totalPrice.value)
}

const handleExportWord = () => {
  exportWord(list.value, totalPrice.value)
}


const routes = [
  {
    path: '/',
    component: Layout,
    redirect: '/home',
    children: [
      {
        path: 'home',
        component: () => import('@/views/Home.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
