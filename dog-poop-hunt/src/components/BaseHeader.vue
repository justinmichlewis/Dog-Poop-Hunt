<template>
  <header class="sticky-header">
    {{ props.title }}
  </header>
</template>

<script setup lang="ts">
const props = defineProps({
  title: String,
});
</script>

<style scoped>
header {
  background-color: #5d676b;
  color: white;
  padding: 15px 0;
  top: 0;
  left: 0;
  width: 100%;
  height: 35px;
  font-size: 25px;
  font-weight: 400;
  z-index: 9999;
  text-align: center;
}
</style>
