<script setup>
// Status is communicated purely through the dot colour.
const props = defineProps({
  status: { type: String, required: true }
})

const colorFor = {
  'on-track': 'bg-success',
  'at-risk': 'bg-warning',
  'blocked': 'bg-danger'
}
</script>

<template>
  <span class="inline-flex items-center">
    <span class="h-3 w-3 rounded-full" :class="colorFor[props.status]"></span>
  </span>
</template>
