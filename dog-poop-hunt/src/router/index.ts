import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Login.vue";
import Map from "@/views/Map.vue";
import List from "@/views/List.vue";
import Me from "@/views/Me.vue";
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
      path: "/me",
      name: "me",
      component: Me,
    },
    {
      path: "/details",
      name: "details",
      component: Details,
    },
  ],
});

export default router;
