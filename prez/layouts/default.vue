<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'

// Dans Slidev, les propriétés du frontmatter sont disponibles directement comme props
const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
}>()
</script>

<template>
  <div class="slidev-layout default">
    <!-- Header -->
    <SlideHeader
      :section="section"
      :sectionName="sectionName"
      :slideName="slideName"
    />

    <!-- Content -->
    <slot />
  </div>
</template>
