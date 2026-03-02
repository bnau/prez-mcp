<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'

const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
}>()
</script>

<template>
  <div class="slidev-layout center h-full flex flex-col">
    <!-- Header -->
    <div class="flex-shrink-0">
      <SlideHeader
        :section="section"
        :sectionName="sectionName"
        :slideName="slideName"
      />
    </div>

    <!-- Content centré verticalement -->
    <div class="flex-1 flex items-center justify-center">
      <div class="w-full px-16">
        <slot />
      </div>
    </div>
  </div>
</template>
