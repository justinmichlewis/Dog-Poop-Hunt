<template>
  <BaseHeader title="Poop List" />
  <BaseFilter @filter-my-dog-poops="filterPoops" />
  <BaseLoader v-show="loading" class="loading-container" />
  <ListsViewListItem
    v-for="(item, index) in items"
    @item-clicked="onItemClicked(item)"
    :title="index + 1"
    :description="item.description"
    :distance="item.distance"
    :age="item.age"
    :bounty="item.bounty"
  />
  <div class="bottom-margin"></div>
  <BaseNavBar :fixed="true" />
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { getPoops } from "@/services/api";
import BaseNavBar from "@/components/BaseNavBar.vue";
import BaseHeader from "@/components/BaseHeader.vue";
import ListsViewListItem from "@/components/ListViewListItem.vue";
import BaseFilter from "@/components/BaseFilter.vue";
import BaseLoader from "@/components/BaseLoader.vue";

interface Item {
  description: string;
  distance: number;
  age: number;
  bounty: number;
  status: string;
  placedUserId: number;
}

const router = useRouter();

const userStore = useUserStore();

let items = ref<Item[]>([]);
let itemsHistory: Item[] = [];
let selectedItem = ref<Item>();
let loading = ref(true);

onMounted(async () => {
  const response = await getPoops();
  if (response.success) {
    items.value = response.res.filter((item: Item) => item.status === "active");
    itemsHistory = items.value;
    loading.value = false;
  } else if (!response.success) {
    console.log("Error", response.res);
  }
});

const filterPoops = (filter: boolean) => {
  items.value = itemsHistory;
  console.log("Filter", filter);
  console.log("Items", items.value);
  if (filter) {
    items.value = items.value.filter(
      (item: Item) =>
        item.placedUserId === userStore.id && item.status === "active"
    );
    console.log("Items", items.value);
  } else {
    items.value = items.value.filter((item: Item) => item.status === "active");
  }
};

const onItemClicked = (item: Item) => {
  selectedItem.value = item;
  router.push({ name: "details", query: item });
};
</script>
<style scoped>
.header-padding {
  margin-top: 60px;
}
.bottom-margin {
  margin-bottom: 100px;
}
</style>
