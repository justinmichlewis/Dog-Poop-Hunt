<template>
  <div class="container">
    <h2>{{ description }}</h2>
    <table class="table">
      <tr>
        <td class="cell">{{ distance }} miles</td>
        <td class="cell">{{ age }} days old</td>
        <td class="cell">{{ bounty }} points</td>
      </tr>
    </table>
  </div>
</template>

<script setup lang="ts">
defineProps({
  description: String,
  distance: Number,
  age: Number,
  bounty: Number,
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
