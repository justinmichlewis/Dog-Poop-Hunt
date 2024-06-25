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
    <BaseActionBar bg-color="#6A98AB"> Navigate </BaseActionBar>
    <BaseNavBar :fixed="false" />
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
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
  },
]);

const loading = ref(false);
const showPopUp = ref(false);

const pickUp = async () => {
  loading.value = true;
  const currentDate = new Date();
  const formattedDate = currentDate.toISOString().split("T")[0];

  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    state: "completed",
    completedDate: formattedDate,
    pickedUserId: userStore.id,
  });

  const requestOptions = {
    method: "POST",
    headers: myHeaders,
    body: raw,
    redirect: "follow",
  };

  const results = await fetch(
    "http://127.0.0.1:5000/api/poops/" + query.poopId,
    requestOptions
  )
    .then((response) => response.text())
    .then((result) => {
      console.log(result);
      loading.value = false;
      showPopUp.value = true;
      setTimeout(() => {
        router.back();
      }, 2000);

      return true;
    })
    .catch((error) => {
      console.error(error);
      loading.value = false;
      return false;
    });
  console.log("Results", results);
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
