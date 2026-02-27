<template>
  <!-- Proposition 1: Design minimaliste avec ligne de séparation -->
  <div class="slidev-layout h-full flex flex-col justify-center items-center text-center px-20">
    <div class="w-full max-w-4xl">
      <!-- Titre principal -->
      <h1 class="text-7xl font-black mb-6">
        <slot />
      </h1>

      <!-- Ligne de séparation élégante -->
      <div class="flex items-center justify-center gap-6 my-8">
        <div class="w-24 h-0.5 bg-current opacity-30"></div>
        <div class="w-3 h-3 rounded-full bg-current opacity-40"></div>
        <div class="w-24 h-0.5 bg-current opacity-30"></div>
      </div>

      <!-- Sous-titre -->
      <p class="text-2xl opacity-70 mb-16">
        {{ $frontmatter.subtitle || 'Une application pour tout comprendre' }}
      </p>

      <!-- Informations en bas -->
      <div class="text-base opacity-60 font-medium">
        {{ $frontmatter.author || 'Bertrand Nau' }} • {{ $frontmatter.event || 'Devoxx France' }} • {{ $frontmatter.date || '22/04/2026' }}
      </div>
    </div>
  </div>
</template>
