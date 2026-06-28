<template>
  <div class="grid grid-cols-3 gap-4">
    <section class="card rounded-2xl p-4 bg-surface">
      <h2 class="text-sm">Throughput</h2><span class="rounded-full px-2 text-xs">on track</span>
    </section>
    <section class="card rounded-2xl p-4"><table class="w-full"><tr><td>Queue depth</td></tr></table></section>
    <section class="card rounded-2xl p-4"><ul><li>Pending approvals</li></ul></section>
  </div>
</template>
<style scoped>.card{border:1px solid var(--color-surface)}</style>
