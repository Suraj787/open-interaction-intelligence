<script setup>
defineProps({
  heading: { type: String, default: 'Dialog' },
  body: { type: String, default: '' }
})
const emit = defineEmits(['close'])
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="card w-full max-w-sm">
      <h2 class="text-lg font-semibold">{{ heading }}</h2>
      <p class="mt-2 text-sm text-slate-600">{{ body }}</p>
      <div class="mt-4 flex justify-end gap-2">
        <button
          type="button"
          class="rounded bg-primary px-3 py-1.5 text-white"
          @click="emit('close')"
        >
          OK
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Hard-coded brand colour rather than a token. */
.dialog-accent {
  border-top: 3px solid #2563eb;
}
</style>
