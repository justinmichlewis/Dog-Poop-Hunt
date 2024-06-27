<template>
  <BaseHeader title="Settings" />
  <div class="background">
    <h1>Dog Poop Hunt</h1>
    <h2>Welcome {{ userStore.firstName }}!</h2>
    <div class="flex">
      <div class="section">
        You have {{ userStore.poopsCollected }} poops collected
      </div>
      <div class="section">You have a total score of {{ userStore.score }}</div>
    </div>
    <h1>{{ userStore.id }}</h1>
    <button @click="logOut">Log Out</button>
  </div>
  <BaseNavBar :fixed="true" />
</template>
<script setup lang="ts">
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseHeader from "@/components/BaseHeader.vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();

const logOut = () => {
  userStore.clearUserData();
  router.push({ name: "login" });
};
</script>
<style scoped>
.background {
  background-color: #6a98ab;
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
