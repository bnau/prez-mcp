<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'
import Footer from '../components/Footer.vue'

const props = defineProps<{
  section?: string
  sectionName?: string
  slideName?: string
  image?: string
  backgroundSize?: 'contain' | 'cover'
}>()
</script>

<template>
  <div class="slidev-layout image-with-header">
    <!-- Header -->
    <SlideHeader
      :section="section"
      :sectionName="sectionName"
      :slideName="slideName"
    />

    <!-- Image Container -->
    <div class="image-container flex items-center justify-center mt-8 px-8 pb-8">
      <img
        v-if="image"
        :src="image"
        :style="{
          objectFit: backgroundSize || 'contain',
          maxWidth: '100%',
          maxHeight: '100%',
          width: 'auto',
          height: 'auto'
        }"
        alt="Slide image"
      />
    </div>

    <!-- Optional content slot -->
    <div class="content-overlay">
      <slot />
    </div>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<style scoped>
.image-with-header {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.image-container {
  flex: 1;
  overflow: hidden;
}

.content-overlay {
  position: absolute;
  bottom: 2rem;
  left: 2rem;
  right: 2rem;
}
</style>
