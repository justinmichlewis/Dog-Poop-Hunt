<template>
  <div>
    <div class="card" @click="$emit('itemClicked')">
      <div class="title">Poop {{ props.title }}</div>
      <div class="body">{{ props.description }}</div>
      <table class="table">
        <tr>
          <td class="cell">{{ props.distance }} miles</td>
          <td class="cell">{{ props.age }} days old</td>
          <td class="cell">{{ props.bounty }} points</td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: Number,
  description: String,
  distance: Number,
  age: Number,
  bounty: Number,
});
</script>

<style scoped>
.card {
  border-style: solid;
  border-color: #d9d9d9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin: 10px;
  padding: 10px;
  position: relative;
}
.title {
  font-size: 20px;
  font-weight: bold;
  margin: 5px;
}
.body {
  margin: 5px;
}
.table {
  width: 100%;
  text-align: center;
  margin: 5px 0;
}
</style>
