<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import ProjectStatus from './ProjectStatus.vue'

const projects = ref([
  { id: 1, name: 'Atlas Migration', owner: 'Priya N.', status: 'on-track' },
  { id: 2, name: 'Billing Revamp', owner: 'Marco D.', status: 'at-risk' },
  { id: 3, name: 'Mobile Redesign', owner: 'Lena K.', status: 'blocked' },
  { id: 4, name: 'Data Warehouse', owner: 'Sam T.', status: 'on-track' }
])
</script>

<template>
  <section>
    <div class="mb-4 flex items-center justify-between">
      <h1 class="text-2xl font-semibold">Projects</h1>
      <!-- Fixed pixel width instead of a layout/spacing token. -->
      <input
        type="search"
        placeholder="Search projects"
        class="w-[327px] rounded border border-slate-300 px-3 py-1.5"
      />
    </div>

    <ul class="grid gap-3">
      <li v-for="project in projects" :key="project.id" class="card flex items-center justify-between">
        <div>
          <RouterLink
            :to="`/projects/${project.id}`"
            class="text-[#3b7] font-medium hover:underline"
          >
            {{ project.name }}
          </RouterLink>
          <p class="text-sm text-slate-500">{{ project.owner }}</p>
        </div>
        <ProjectStatus :status="project.status" />
      </li>
    </ul>
  </section>
</template>
