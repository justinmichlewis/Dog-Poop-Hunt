<template>
  <BaseHeader title="Poop Map" />
  <BaseLoader v-show="loading" class="loading-container" />
  <button @click="markPoop">Mark Poop</button>
  <BaseMap
    @map-loaded="(n) => (loading = !n)"
    :fullHeight="true"
    :markers="items"
  />
  <BaseNavBar :fixed="true" />
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseHeader from "@/components/BaseHeader.vue";
import BaseMap from "@/components/BaseMap.vue";
import BaseLoader from "@/components/BaseLoader.vue";

interface Item {
  description: string;
  distance: number;
  age: number;
  bounty: number;
  status: string;
  placedUserId: number;
}

let items = ref<Item[]>([]);
let loading = ref(true);

onMounted(async () => {
  items.value = await fetch("http://127.0.0.1:5000/api/poops")
    .then((response) => response.json())
    .then((data) => {
      return data.filter((item: Item) => item.status === "active");
    })
    .catch((error) => console.log("Err", error));
});

const markPoop = async () => {
  console.log("Marking poop");
};
</script>
<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
}
</style>
