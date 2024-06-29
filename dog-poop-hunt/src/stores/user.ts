import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

export const useUserStore = defineStore("user", {
  state: () => ({
    firstName: useStorage("firstName", ""),
    lastName: useStorage("lastName", ""),
    email: useStorage("email", ""),
    id: useStorage("id", 0),
    lat: useStorage("lat", 0),
    lon: useStorage("lon", 0),
  }),
  actions: {
    setUserData(
      firstName: string,
      lastName: string,
      email: string,
      id: number,
      lat: number,
      lon: number
    ) {
      this.firstName = firstName;
      this.lastName = lastName;
      this.email = email;
      this.id = id;
      this.lat = lat;
      this.lon = lon;
    },
    clearUserData() {
      this.firstName = "";
      this.lastName = "";
      this.email = "";
      this.id = 0;
      this.lat = 0;
      this.lon = 0;
    },
  },
});
