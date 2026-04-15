<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'
import Footer from '../components/Footer.vue'

// Dans Slidev, les propriétés du frontmatter sont disponibles directement comme props
const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
  hideFooter?: boolean
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

    <!-- Footer -->
    <Footer v-if="!hideFooter" />
  </div>
</template>
