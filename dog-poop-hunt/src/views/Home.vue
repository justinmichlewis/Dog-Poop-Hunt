<template>
  <div class="background">
    <h1>Dog Poop Hunt</h1>
    <h2>Welcome {{ userStore.firstName }}!</h2>
    <div class="flex">
      <div class="section">
        You have {{ userStore.poopsCollected }} poops collected
        <button @click="router.push({ name: 'map' })">Hunt</button>
      </div>

      <div class="section">
        You have a total score of {{ userStore.score }}
        <button @click="router.push({ name: 'mark' })">Mark</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
const userStore = useUserStore();
const router = useRouter();
</script>

<style scoped>
.background {
  background-color: #56bfea;
  padding: 10px;
  text-align: center;
  height: 100vh;
}
.flex {
  display: flex;
  text-align: center;
  justify-content: space-between;
}

.section {
  flex: 1;
}
button {
  background-color: rgb(109, 202, 109);
  border: none;
  border-radius: 3px;
  width: 40vw;
  color: white;
  font-size: larger;
  padding: 5px;
  margin: 10px;
}
</style>

<style scoped></style>
