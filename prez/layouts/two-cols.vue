<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'

const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
  class?: string
  layoutClass?: string
}>()
</script>

<template>
  <div class="slidev-layout two-cols-comparison">
    <!-- Header -->
    <SlideHeader
      :section="section"
      :sectionName="sectionName"
      :slideName="slideName"
    />

    <!-- Content with two columns -->
    <div class="w-full grid grid-cols-2 gap-8 mt-8 px-16" :class="props.layoutClass">
      <div class="col-left" :class="props.class">
        <slot />
        <slot name="left" />
      </div>
      <div class="col-right" :class="props.class">
        <slot name="right" />
      </div>
    </div>
  </div>
</template>
