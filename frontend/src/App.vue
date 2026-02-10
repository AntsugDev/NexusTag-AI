<script setup>
import { onMounted, onUnmounted } from 'vue';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const handleError = (event) => {
  toast.add({ severity: 'error', summary: 'Errore', detail: event.detail, life: 5000 });
};

onMounted(() => {
  window.addEventListener('api-error', handleError);
});

onUnmounted(() => {
  window.removeEventListener('api-error', handleError);
});
</script>

<template>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
  <Toast />
  <ConfirmDialog />
</template>

<style>
/* App styles are in main.css */
</style>
