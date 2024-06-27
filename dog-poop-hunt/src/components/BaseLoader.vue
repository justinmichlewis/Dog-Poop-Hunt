<template>
  <div class="lspinner-overlay loading-container">
    <div class="spinner"></div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="css" scoped>
.spinner-overlay {
  position: absolute;
  top: 0;
  left: 0px;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 9999;
}

.spinner {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid #ffffff;
  border-top-color: #56bfea;
  border-radius: 50%;
  animation: spin 1s ease-in-out infinite;
}
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
