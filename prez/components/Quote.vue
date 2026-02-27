<template>
  <div class="quote-container">
    <div class="quote-text">
      <slot />
    </div>
    <div class="quote-author" v-if="author">
      {{ author }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  author: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.quote-container {
  position: relative;
  padding: 1rem;
  margin: 1rem 0;
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.quote-text {
  font-style: italic;
  font-size: 1.5rem;
  line-height: 1.8;
  color: #333;
  margin-bottom: 2rem;
}

.quote-text::before {
  content: '"';
  font-size: 3rem;
  color: #ccc;
  position: absolute;
  left: 0;
  top: 0;
  line-height: 1;
}

.quote-text::after {
  content: '"';
  font-size: 3rem;
  color: #ccc;
  position: absolute;
  right: 0;
  bottom: 0;
  line-height: 1;
}

.quote-author {
  text-align: right;
  font-style: normal;
  font-weight: 500;
  color: #666;
  margin-top: auto;
}

.quote-author::before {
  content: '— ';
}

/* Mode sombre */
.dark .quote-text {
  color: #e0e0e0;
}

.dark .quote-text::before,
.dark .quote-text::after {
  color: #555;
}

.dark .quote-author {
  color: #999;
}
</style>
