<template>
  <div class="container">
    <BaseLoader v-show="showLoader" />
    <div v-show="!showLoader">
      <h1>Dog Poop Hunt</h1>
      <form @submit.prevent>
        <label for="username">Email:</label>
        <input type="email" id="email" name="email" v-model="email" />
        <label for="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          v-model="password"
        />
        <button type="submit" @click="logIn">Login</button>
      </form>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user";
import { authenticateUser } from "@/services/api";
import CryptoJS from "crypto-js";
import BaseLoader from "@/components/BaseLoader.vue";

const email = ref("");
const password = ref("");
const router = useRouter();
const userStore = useUserStore();
const showLoader = ref(false);

const logIn = async () => {
  showLoader.value = true;
  var passphrase = "kldiki990dlkl2k2990dlsls";
  var iv = CryptoJS.lib.WordArray.random(16);

  var encrypted = CryptoJS.AES.encrypt(
    password.value,
    CryptoJS.enc.Utf8.parse(passphrase),
    {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7,
    }
  );

  var ivBase64 = CryptoJS.enc.Base64.stringify(iv);
  var encryptedBase64 = encrypted.toString();

  var requestData = {
    iv: ivBase64,
    encrypted_message: encryptedBase64,
  };

  const response = await authenticateUser(email.value, requestData);
  console.log(response.data);
  if (response.success) {
    userStore.setUserData(
      response.data.firstName,
      response.data.lastName,
      response.data.email,
      response.data.id,
      0,
      0
    );
    router.push({ name: "map" });
  } else {
    alert("Invalid email or password");
  }
  showLoader.value = false;
};
</script>

<style scoped>
h1 {
  text-align: center;
  font-size: 3em;
  margin-top: 1em;
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
