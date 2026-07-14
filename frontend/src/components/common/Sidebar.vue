<template>
  <div class="col-md-2 border-end bg-white vh-100 p-0 shadow-sm">
    <div class="list-group list-group-item-action text-start">
      <RouterLink
        v-for="item in menu"
        :key="item.path"
        :to="item.path"
        class="list-group-item list-group-item-action border-0 py-3"
        active-class="active"
      >
        <i :class="item.icon"></i>

        {{ item.name }}
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "../../stores/auth";
import { menus } from "../../utils/menu";
const auth = useAuthStore();
const menu = computed(() => menus[auth.role] || []);
</script>
