<script setup>
import { ref } from 'vue'
import DialogModal from './DialogModal.vue'

const notify = ref(true)
const theme = ref('system')
const showSaved = ref(false)

function save() {
  showSaved.value = true
}
</script>

<template>
  <section>
    <h1 class="mb-4 text-2xl font-semibold">Settings</h1>

    <form class="card grid max-w-md gap-4" @submit.prevent="save">
      <label class="flex items-center justify-between">
        <span>Email notifications</span>
        <input v-model="notify" type="checkbox" />
      </label>

      <label class="grid gap-1">
        <span>Theme</span>
        <select v-model="theme" class="rounded border border-slate-300 px-2 py-1">
          <option value="system">System</option>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
      </label>

      <button
        type="submit"
        class="rounded bg-primary px-4 py-2 text-white outline-none"
      >
        Save changes
      </button>
    </form>

    <DialogModal
      v-if="showSaved"
      heading="Saved"
      body="Your settings were updated."
      @close="showSaved = false"
    />
  </section>
</template>
