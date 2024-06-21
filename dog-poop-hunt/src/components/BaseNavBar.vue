<template>
  <nav :class="fixed ? 'bottom-navigation fixed' : 'bottom-navigation'">
    <router-link to="/home" class="nav-item" exact>Home </router-link>
    <router-link to="/map" class="nav-item" exact>Map </router-link>
    <router-link to="/list" class="nav-item" exact>List</router-link>
    <router-link to="/settings" class="nav-item" exact>Settings</router-link>
  </nav>
</template>

<script setup lang="ts">
defineProps({
  fixed: Boolean,
});
</script>

<style scoped>
.bottom-navigation {
  bottom: 0;
  left: 0;
  width: 100%;
  height: 10vh;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 3px;
  z-index: 9999;
  background-color: #56bfea;
}

.nav-item {
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 1.5rem;
}
.fixed {
  position: fixed;
}
</style>

.bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%;
background-color: #333; display: flex; justify-content: space-around; padding:
10px 0; } .nav-item { color: white; text-decoration: none; padding: 10px 20px; }
