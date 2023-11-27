import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AssignmentOne from '../views/AssignmentOne.vue'
import AssignmentTwo from '../views/AssignmentTwo.vue'
import AssignmentThree from '../views/AssignmentThree.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/AssignmentOne',
      name: 'AssignmentOne',
      component: AssignmentOne
    },
    {
      path: '/AssignmentTwo',
      name: 'AssignmentTwo',
      component: AssignmentTwo
    },
    {
      path: '/AssignmentThree',
      name: 'AssignmentThree',
      component: AssignmentThree
    }
  ]
})

export default router
