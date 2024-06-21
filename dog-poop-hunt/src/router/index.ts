import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Map from "@/views/Map.vue";
import List from "@/views/List.vue";
import Settings from "@/views/Settings.vue";
import Details from "@/views/Details.vue";

const router = createRouter({
  history: createWebHistory((import.meta as any).env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: Login,
    },
    {
      path: "/home",
      name: "home",
      component: Home,
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
  ],
});

export default router;
