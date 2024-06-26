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
  <BaseNavBar :fixed="true" />
</template>
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
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
  items.value = await fetch("http://127.0.0.1:5000/api/poops")
    .then((response) => response.json())
    .then((data) => {
      itemsHistory = data.filter((item: Item) => item.status === "active");
      loading.value = false;
      return itemsHistory;
    })
    .catch((error) => console.log("Err", error));
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
.loading-container {
  display: flex;
  position: relative;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
}
</style>
