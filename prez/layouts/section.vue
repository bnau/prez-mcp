<script setup>
</script>
<template>
  <!-- Proposition 1: Numéro grand et stylé à gauche -->
  <div class="slidev-layout h-full grid section relative overflow-hidden">
    <div class="my-auto relative z-10">

      <!-- Contenu de la section -->
      <div class="relative px-20">
        <div class="text-6xl font-bold mb-4">
          <span class="text-5xl opacity-40 mr-6">{{ $frontmatter.number }}</span>
          <div v-if="$frontmatter.title"> {{ $frontmatter.title }} </div>
        </div>
        <!-- Sous-titre optionnel -->
        <div v-if="$frontmatter.subtitle" class="text-2xl opacity-70 mt-6">
          {{ $frontmatter.subtitle }}
        </div>
        <div class="w-32 h-1.5 bg-current opacity-30 mt-8"></div>
      </div>
    </div>
  </div>
</template>
