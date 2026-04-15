<template>
  <div class="slidev-footer">
    <img src="/images/devoxx.png" alt="Devoxx France" class="devoxx-logo" />
  </div>
</template>

<style scoped>
.slidev-footer {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 10;
}

.devoxx-logo {
  height: 40px;
  width: auto;
  opacity: 0.9;
}

/* Ajustement pour l'affichage en mode présentation */
@media print {
  .slidev-footer {
    bottom: 15px;
    right: 15px;
  }

  .devoxx-logo {
    height: 35px;
  }
}
</style>
