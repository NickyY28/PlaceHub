<template>
  <nav v-if="totalPages > 1">
    <ul class="pagination justify-content-end mb-0">
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <button class="page-link" @click="$emit('change', currentPage - 1)">
          Previous
        </button>
      </li>

      <li
        v-for="page in totalPages"
        :key="page"
        class="page-item"
        :class="{ active: page === currentPage }"
      >
        <button class="page-link" @click="$emit('change', page)">
          {{ page }}
        </button>
      </li>

      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <button class="page-link" @click="$emit('change', currentPage + 1)">
          Next
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
defineProps({
  currentPage: Number,

  totalPages: Number,
});

defineEmits(["change"]);
</script>
