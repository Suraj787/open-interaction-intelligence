<script setup>
defineProps({
  title: { type: String, default: 'Confirm' },
  message: { type: String, default: '' }
})
const emit = defineEmits(['confirm', 'cancel'])
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="card w-full max-w-sm">
      <h2 class="text-lg font-semibold">{{ title }}</h2>
      <p class="mt-2 text-sm text-slate-600">{{ message }}</p>
      <div class="mt-4 flex justify-end gap-2">
        <button
          type="button"
          class="rounded px-3 py-1.5 text-slate-600"
          @click="emit('cancel')"
        >
          Cancel
        </button>
        <button
          type="button"
          class="rounded bg-danger px-3 py-1.5 text-white"
          @click="emit('confirm')"
        >
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>
