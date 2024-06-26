import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Login.vue";
import Map from "@/views/Map.vue";
import List from "@/views/List.vue";
import Settings from "@/views/Settings.vue";
import Details from "@/views/Details.vue";
import Mark from "@/views/Mark.vue";

const router = createRouter({
  history: createWebHistory((import.meta as any).env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: Login,
    },
    {
      path: "/map",
      name: "map",
      component: Map,
    },
    {
      path: "/list",
      name: "list",
      component: List,
    },
    {
      path: "/settings",
      name: "settings",
      component: Settings,
    },
    {
      path: "/details",
      name: "details",
      component: Details,
    },
    {
      path: "/mark",
      name: "mark",
      component: Mark,
    },
  ],
});

export default router;
