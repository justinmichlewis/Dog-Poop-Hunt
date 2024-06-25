<template>
  <BaseHeader title="Settings" />
  <BaseNavBar :fixed="true" />
  <h1>{{ userStore.id }}</h1>
  <button @click="logOut">Log Out</button>
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
<style scoped></style>
