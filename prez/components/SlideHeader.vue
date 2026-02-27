<script setup lang="ts">
defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
}>()
</script>

<template>
  <div
    v-if="section && sectionName && slideName"
    class="slide-header mb-4 pb-2 border-b border-gray-300"
  >
    <div class="flex items-center gap-3">
      <div class="text-3xl font-700 opacity-20 leading-none">
        {{ section }}
      </div>
      <div class="flex-1">
        <div class="text-xs font-500 uppercase tracking-widest opacity-40">
          {{ sectionName }}
        </div>
        <div class="text-sm font-400 opacity-100 mt-0.5">
          {{ slideName }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.slide-header {
  /* S'assurer que le header a le bon style Apple */
  user-select: none;
}
</style>
