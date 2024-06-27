<template>
  <BaseHeader title="Poop Details" />
  <DetailsViewInfo
    :description="query.description ? query.description.toString() : ''"
    :age="query.age ? parseInt(query.age.toString()) : 0"
    :bounty="query.bounty ? parseInt(query.bounty.toString()) : 0"
  ></DetailsViewInfo>
  <div class="container-content">
    <BaseLoader v-show="loading" class="loading-container" />
    <BasePopUp :show="showPopUp"> <h2>Poop Picked Up!</h2></BasePopUp>
    <BaseMap :fullHeight="false" :markers="markers" />
    <BaseActionBar bg-color="#EBA557" @click="pickUp">
      Pick Up Poop
    </BaseActionBar>
    <BaseNavBar :fixed="false" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { deletePoop } from "@/services/api";
import BaseHeader from "@/components/BaseHeader.vue";
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseMap from "@/components/BaseMap.vue";
import BaseActionBar from "@/components/BaseActionBar.vue";
import DetailsViewInfo from "@/components/DetailsViewInfo.vue";
import BaseLoader from "@/components/BaseLoader.vue";
import BasePopUp from "@/components/BasePopUp.vue";

const query = useRoute().query;
const router = useRouter();

const userStore = useUserStore();

const markers = reactive([
  {
    latitude: query.latitude,
    longitude: query.longitude,
    poopId: query.poopId,
    description: query.description,
    age: query.age,
  },
]);

const loading = ref(false);
const showPopUp = ref(false);

const pickUp = async () => {
  loading.value = true;
  deletePoop(query.poopId, userStore.id);
  loading.value = false;
  showPopUp.value = true;
  setTimeout(() => {
    router.back();
  }, 2000);
};
</script>

<style scoped>
h2 {
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
