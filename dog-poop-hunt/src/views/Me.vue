<template>
  <BaseHeader title="About Me" />
  <div class="background">
    <h1>Dog Poop Hunt</h1>
    <h2>Welcome {{ userStore.firstName }}!</h2>
    <div class="flex">
      <div class="section">
        You have {{ achievements.totalPoopsPicked }} poops collected
      </div>
      <div class="section">
        You have a total score of {{ achievements.totalPoints }}
      </div>
    </div>
  </div>
  <div class="container-content">
    <BaseActionBar bg-color="#84C877" @click="logOut"> Log Out </BaseActionBar>
    <BaseNavBar />
  </div>
</template>
<script setup lang="ts">
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseHeader from "@/components/BaseHeader.vue";
import BaseActionBar from "@/components/BaseActionBar.vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { getAchievements } from "@/services/api";

const userStore = useUserStore();
const router = useRouter();
let achievements = ref({ totalPoopsPicked: 0, totalPoints: 0 });

onMounted(async () => {
  achievements.value = await getAchievements(userStore.id);
  console.log(achievements.value);
});

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
.container-content {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 9999;
}
</style>
