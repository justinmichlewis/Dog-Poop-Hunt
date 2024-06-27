<template>
  <div class="container">
    <h1>Dog Poop Hunt</h1>
    <form @submit.prevent>
      <label for="username">Email:</label>
      <input type="email" id="email" name="email" v-model="email" />
      <label for="password">Password:</label>
      <input type="password" id="password" name="password" v-model="password" />
      <button type="submit" @click="logIn">Login</button>
    </form>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { getAchievements, getUser, authenticateUser } from "@/services/api";
import CryptoJS from "crypto-js";

const email = ref("");
const password = ref("");
const router = useRouter();
const userStore = useUserStore();

const logIn = async () => {
  var passphrase = "kldiki990dlkl2k2990dlsls";
  var iv = CryptoJS.lib.WordArray.random(16); // 16 bytes IV for AES-128

  // Encrypt
  var encrypted = CryptoJS.AES.encrypt(
    password.value,
    CryptoJS.enc.Utf8.parse(passphrase),
    {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7,
    }
  );

  // Convert IV and encrypted data to Base64
  var ivBase64 = CryptoJS.enc.Base64.stringify(iv);
  var encryptedBase64 = encrypted.toString();

  // Prepare data to send to Flask server
  var requestData = {
    iv: ivBase64,
    encrypted_message: encryptedBase64,
  };

  const response = await authenticateUser(email.value, requestData);

  console.log(response);

  // const userData = await getUser(userName.value);
  // const achievmentsData = await getAchievements(userName.value);

  // userStore.setUserData(
  //   userData.firstName,
  //   userData.lastName,
  //   userData.email,
  //   achievmentsData.totalPoopsPicked,
  //   -1,
  //   achievmentsData.totalPoints,
  //   Number(userName.value)
  // );
  // router.push({ name: "map" });
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
