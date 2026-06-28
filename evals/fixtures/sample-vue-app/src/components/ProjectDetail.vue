<script setup>
import { ref, computed } from 'vue'
import ConfirmModal from './ConfirmModal.vue'
import ProjectStatus from './ProjectStatus.vue'

const props = defineProps({
  id: { type: [String, Number], required: true }
})

const showConfirm = ref(false)

const project = computed(() => ({
  id: props.id,
  name: `Project #${props.id}`,
  owner: 'Priya N.',
  status: 'at-risk',
  description: 'Cross-team initiative tracked in the Acme portfolio.'
}))

function archiveProject() {
  showConfirm.value = false
}
</script>

<template>
  <section>
    <div class="mb-4 flex items-center gap-3">
      <h1 class="text-2xl font-semibold">{{ project.name }}</h1>
      <ProjectStatus :status="project.status" />
    </div>

    <div class="card mb-4">
      <p class="text-slate-600">{{ project.description }}</p>
      <dl class="mt-3 text-sm">
        <dt class="inline font-medium">Owner:</dt>
        <dd class="inline text-slate-500"> {{ project.owner }}</dd>
      </dl>
    </div>

    <!-- Spinner has no prefers-reduced-motion guard. -->
    <div class="mb-4 flex items-center gap-2 text-sm text-slate-500">
      <span class="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-primary"></span>
      Syncing latest activity...
    </div>

    <button
      type="button"
      class="rounded bg-danger px-4 py-2 text-white focus:outline-none"
      @click="showConfirm = true"
    >
      Archive project
    </button>

    <ConfirmModal
      v-if="showConfirm"
      title="Archive project?"
      message="This will move the project to the archive."
      @confirm="archiveProject"
      @cancel="showConfirm = false"
    />
  </section>
</template>
