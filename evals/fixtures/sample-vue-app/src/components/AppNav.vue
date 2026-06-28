<script setup>
import { RouterLink } from 'vue-router'

const links = [
  { to: '/projects', label: 'Projects' },
  { to: '/settings', label: 'Settings' }
]
</script>

<template>
  <header class="bg-primary text-white">
    <nav class="mx-auto flex max-w-5xl items-center gap-6 px-4 py-3">
      <RouterLink to="/" class="text-lg font-semibold">Acme Projects</RouterLink>
      <ul class="flex gap-4">
        <li v-for="link in links" :key="link.to">
          <RouterLink :to="link.to" class="brand-link text-white/90 hover:text-white">
            {{ link.label }}
          </RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>
