<template>
  <div
    class="color"
    :class="'bar-style-default' + ' ' + 'background-color'"
    @click="$emit('clicked', true)"
  >
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
defineProps({
  bgColor: String,
});
</script>
<style scoped>
.background-color {
  background-color: v-bind(bgColor);
}
.bar-style-default {
  width: 100vw;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: 300;
}
</style>
