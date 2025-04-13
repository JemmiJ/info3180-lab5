<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <div class="page-layout">
    <AppHeader />
    <main class="page-content">
      <RouterView />
    </main>
    <AppFooter />
  </div>
</template>

<style>
body {
  padding-top: 75px;
}
.page-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>