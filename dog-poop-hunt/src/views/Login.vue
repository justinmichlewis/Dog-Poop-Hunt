<template>
  <div class="container">
    <h1>Dog Poop Hunt</h1>
    <form @submit.prevent>
      <label for="username">Username:</label>
      <input type="text" id="username" name="username" v-model="userName" />
      <button type="submit" @click="logIn">Login</button>
    </form>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";

const userName = ref("");
const router = useRouter();
const userStore = useUserStore();

const logIn = async () => {
  const userData = await getUser();
  const achievmentsData = await getAchievements();

  userStore.setUserData(
    userData.firstName,
    userData.lastName,
    userData.email,
    achievmentsData.totalPoopsPicked,
    -1,
    achievmentsData.totalPoints,
    Number(userName.value)
  );
  router.push({ name: "map" });
};

const getUser = async () => {
  return await fetch("http://127.0.0.1:5000/api/users/" + userName.value)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
    });
};

const getAchievements = async () => {
  return await fetch("http://127.0.0.1:5000/api/achievements/" + userName.value)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<style scoped>
h1 {
  text-align: center;
  font-size: 3em;
}
form {
  width: 50vw;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 20vh;
}
input {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border-color: rgb(213, 213, 213);
  border-radius: 10px;
}
button {
  background-color: rgb(109, 202, 109);
  border: none;
  border-radius: 3px;
  width: 40vw;
  color: white;
  font-size: larger;
  padding: 5px;
  margin: 10px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
label {
  display: block;
  text-align: center;
  font-size: 1.5em;
  margin-top: 20px;
  margin-bottom: 10px;
}
.container {
  background-color: #56bfea;
  padding: 10px;
  text-align: center;
  height: 100vh;
}
</style>
