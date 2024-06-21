<template>
  <router-view></router-view>
</template>
<script setup lang="ts"></script>
<style>
h1,
h2,
div,
table,
tr,
td,
button {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 400;
}
body {
  margin: 0px !important;
}
html {
  touch-action: manipulation;
  viewport {
    zoom: 1 !important;
    min-zoom: 1 !important;
    max-zoom: 1 !important;
    user-zoom: fixed !important;
  }
}
</style>
