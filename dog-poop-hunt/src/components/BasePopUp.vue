<template>
  <transition name="popup-fade" @after-enter="startTimer">
    <div class="popup" v-if="showPopup">
      <div class="popup-content">
        <slot></slot>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, onUpdated } from "vue";

const props = defineProps({
  show: Boolean,
});

const emit = defineEmits(["closed"]);

const showPopup = ref(false);

const startTimer = () => {
  setTimeout(() => {
    showPopup.value = false;
    emit("closed");
  }, 2000);
};

onUpdated(() => {
  if (props.show) {
    showPopup.value = true;
    startTimer();
  }
});
</script>

<style scoped>
.popup {
  position: fixed;
  display: flex;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  justify-content: center;
  align-items: center;
}

.popup-content {
  text-align: center;
}

.popup-fade-enter-active,
.popup-fade-leave-active {
  transition: opacity 0.5s;
}

.popup-fade-enter, .popup-fade-leave-to /* .popup-fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
