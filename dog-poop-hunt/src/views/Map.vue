<template>
  <BaseHeader title="Poop Map" />
  <BaseLoader v-show="loading" class="loading-container" />
  <BaseModal
    v-show="showModal"
    @submit-pressed="markPoop"
    @cancel-pressed="showModal = false"
  />
  <button id="overlay-button" @click="showModal = true">Mark Poop</button>
  <BaseMap
    @map-loaded="(n) => (loading = !n)"
    @coords="(n) => (coords = n)"
    :fullHeight="true"
    :markers="items"
    :updateMap="updateMap"
  />
  <BaseNavBar :fixed="true" />
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { createPoop, getPoops } from "@/services/api";
import { useUserStore } from "@/stores/user";
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseHeader from "@/components/BaseHeader.vue";
import BaseMap from "@/components/BaseMap.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import BaseModal from "@/components/BaseModal.vue";

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
let showModal = ref(false);
let coords = ref([]);
let updateMap = ref(0);

const userStore = useUserStore();

onMounted(async () => {
  const response = await getPoops();
  if (response.success) {
    items.value = response.res.filter((item: Item) => item.status === "active");
  } else if (!response.success) {
    console.log("Error", response.res);
  }
});

const markPoop = async (description: string) => {
  showModal.value = false;
  loading.value = true;
  await createPoop(
    description,
    userStore.id,
    coords.value[0],
    coords.value[1]
  ).then((response) => {
    if (response.success) {
      items.value.push(response.res.result);
      updateMap.value += 1;
      loading.value = false;
    } else if (!response.success) {
      console.log("Error", response.res);
      loading.value = false;
    }
  });
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
#overlay-button {
  position: absolute;
  width: 25vw;
  height: 5vh;
  top: 10vh;
  left: 70vw;
  z-index: 1000;
  padding: 10px;
  background-color: white;
  border: 1px solid #ccc;
  cursor: pointer;
  box-shadow: 5px 10px 0px rgba(123, 7, 7, 0.1);
}
</style>
