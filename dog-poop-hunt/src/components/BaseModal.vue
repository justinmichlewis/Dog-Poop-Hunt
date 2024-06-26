<template>
  <div class="container">
    <div class="textarea-container">
      <textarea
        v-model="userInput"
        id="userInput"
        placeholder="Enter a brief description to help you locate..."
      ></textarea>
    </div>
    <div class="button-submit-container">
      <button @click="$emit('submitPressed', userInput)">Submit</button>
    </div>
    <div class="button-cancel-container">
      <button @click="$emit('cancelPressed', userInput)">Cancel</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
const userInput = ref("");
const emit = defineEmits(["submitPressed", "cancelPressed"]);
</script>

<style scoped>
.container {
  position: fixed;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: 300;
  z-index: 9999;
}

.textarea-container {
  margin-bottom: 10px;
}

.textarea-container textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button-submit-container {
  margin: 5px;
  text-align: center;
}

.button-submit-container button {
  padding: 10px 20px;
  font-size: 16px;
  width: 30vw;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-cancel-container {
  text-align: center;
}

.button-cancel-container button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #e54919;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
