<template>
  <div class="d-flex justify-content-between align-items-center mb-4">
    <div>
      <h2 class="fw-bold mb-1">
        {{ title }}
      </h2>

      <p class="text-muted mb-0">
        {{ subtitle }}
      </p>
    </div>

    <div v-if="$slots.action">
      <slot name="action" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },

  subtitle: {
    type: String,
    default: "",
  },
});
</script>
