import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

export const useUserStore = defineStore("user", {
  state: () => ({
    firstName: useStorage("firstName", ""),
    lastName: useStorage("lastName", ""),
    email: useStorage("email", ""),
    id: useStorage("id", 0),
  }),
  actions: {
    setUserData(
      firstName: string,
      lastName: string,
      email: string,
      id: number
    ) {
      this.firstName = firstName;
      this.lastName = lastName;
      this.email = email;
      this.id = id;
    },
    clearUserData() {
      this.firstName = "";
      this.lastName = "";
      this.email = "";
      this.id = 0;
    },
  },
});
