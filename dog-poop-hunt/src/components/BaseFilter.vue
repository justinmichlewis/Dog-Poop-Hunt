<template>
  <div>Placed by me</div>
  <input type="checkbox" @change="handleCheckboxChange" />
</template>

<script setup lang="ts">
const emit = defineEmits(["filter-my-dog-poops"]);
const handleCheckboxChange = (event: Event) => {
  if (event.target !== null) {
    const checkbox = event.target as HTMLInputElement;
    emit("filter-my-dog-poops", checkbox.checked);
  }
};
</script>

<style scoped></style>
