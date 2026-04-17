<script setup lang="ts">
import SlideHeader from '../components/SlideHeader.vue'
import Footer from '../components/Footer.vue'
</script>

<template>
  <div class="slidev-layout section-with-header h-full flex flex-col relative overflow-hidden">
    <!-- Header -->
    <SlideHeader
      :section="$frontmatter.section"
      :sectionName="$frontmatter.sectionName"
      :slideName="$frontmatter.slideName"
    />

    <!-- Contenu centré verticalement comme dans section.vue -->
    <div class="flex-1 flex items-center">
      <div class="relative px-20 w-full">
        <div class="text-6xl font-bold mb-4">
          <div v-if="$frontmatter.title">{{ $frontmatter.title }}</div>
        </div>
        <!-- Sous-titre optionnel -->
        <div v-if="$frontmatter.subtitle" class="text-2xl opacity-70 mt-6">
          {{ $frontmatter.subtitle }}
        </div>
        <div class="w-32 h-1.5 bg-current opacity-30 mt-8"></div>
      </div>
    </div>

    <!-- Footer -->
    <Footer />
  </div>
</template>
