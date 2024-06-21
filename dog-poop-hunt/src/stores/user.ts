import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

export const useUserStore = defineStore("user", {
  state: () => ({
    firstName: useStorage("firstName", ""),
    lastName: useStorage("lastName", ""),
    email: useStorage("email", ""),
    poopsCollected: useStorage("poopsColleded", 0),
    poopsMissed: useStorage("poopsMissed", 0),
    score: useStorage("score", 0),
    id: useStorage("id", 0),
  }),
  actions: {
    setUserData(
      firstName: string,
      lastName: string,
      email: string,
      poopsCollected: number,
      poopsMissed: number,
      score: number,
      id: number
    ) {
      this.firstName = firstName;
      this.lastName = lastName;
      this.email = email;
      this.poopsCollected = poopsCollected;
      this.poopsMissed = poopsMissed;
      this.score = score;
      this.id = id;
    },
    clearUserData() {
      this.firstName = "";
      this.lastName = "";
      this.email = "";
      this.poopsCollected = 0;
      this.poopsMissed = 0;
      this.score = 0;
      this.id = 0;
    },
  },
});
