<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container-fluid">
      <RouterLink to="/" class="navbar-brand"> PlaceHub </RouterLink>

      <div class="ms-auto d-flex align-items-center">
        <span class="text-white me-3">
          {{ auth.user?.name }}
        </span>

        <button class="btn btn-light btn-sm" @click="logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";
const router = useRouter();
const auth = useAuthStore();
const logout = () => {
  auth.logout();
  router.replace("/login");
};
</script>
