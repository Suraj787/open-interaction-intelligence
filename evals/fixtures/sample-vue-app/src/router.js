import { createRouter, createWebHistory } from 'vue-router'

import ProjectList from './components/ProjectList.vue'
import ProjectDetail from './components/ProjectDetail.vue'
import Settings from './components/Settings.vue'

const routes = [
  { path: '/', name: 'home', component: ProjectList },
  { path: '/projects', name: 'projects', component: ProjectList },
  { path: '/projects/:id', name: 'project-detail', component: ProjectDetail, props: true },
  { path: '/settings', name: 'settings', component: Settings }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
