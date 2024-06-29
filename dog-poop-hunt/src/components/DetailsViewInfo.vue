<template>
  <div class="container">
    <h2>{{ description }}</h2>
    <table class="table">
      <tr>
        <td class="cell">Distance: {{ distance }} mi</td>
        <td class="cell">Age: {{ age }}</td>
        <td class="cell">Bounty: {{ bounty }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps({
  description: String,
  age: Number,
  bounty: Number,
  distance: Number,
});
</script>

<style scoped>
h2 {
  font-size: 1.5em;
}
.container {
  margin: 1em;
}
.table {
  width: 100%;
  text-align: center;
  margin: 5px 0;
  font-size: 1.25em;
}
</style>
