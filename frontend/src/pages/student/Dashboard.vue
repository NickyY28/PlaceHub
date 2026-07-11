<template>
  <div>
    <h3 class="mb-4">Student Dashboard</h3>

    <div class="row">
      <StatCard
        title="Applied"
        :value="dashboard.applied"
        icon="bi bi-file-earmark-text-fill"
      />

      <StatCard
        title="Pending"
        :value="dashboard.pending"
        icon="bi bi-hourglass-split"
      />

      <StatCard
        title="Shortlisted"
        :value="dashboard.shortlisted"
        icon="bi bi-check-circle-fill"
      />

      <StatCard
        title="Rejected"
        :value="dashboard.rejected"
        icon="bi bi-x-circle-fill"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import StatCard from "../../components/common/StatCard.vue";

const dashboard = reactive({
  applied: 0,
  pending: 0,
  shortlisted: 0,
  rejected: 0,
});
</script>
