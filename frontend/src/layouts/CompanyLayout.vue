<template>
  <div>
    <Navbar />

    <div class="container-fluid">
      <div class="row pt-1">
        <Sidebar />

        <main class="col-md-10 p-4">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from "../components/common/Navbar.vue";
import Sidebar from "../components/common/Sidebar.vue";
</script>
