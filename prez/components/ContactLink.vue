<script setup lang="ts">
defineProps<{
  href: string
  icon: string
  label: string
  iconColor?: string
}>()
</script>

<template>
  <div class="flex items-center gap-3">
    <div v-html="icon" :style="iconColor ? `color: ${iconColor}` : ''" class="w-5 h-5 flex-shrink-0" />
    <a :href="href" :target="href.startsWith('http') ? '_blank' : undefined">{{ label }}</a>
  </div>
</template>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}

a:hover {
  text-decoration: underline;
}
</style>
