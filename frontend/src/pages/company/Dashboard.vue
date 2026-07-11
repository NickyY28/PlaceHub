<template>
  <div>
    <h3 class="mb-4">Company Dashboard</h3>

    <div class="row">
      <StatCard
        title="Drives"
        :value="dashboard.drives"
        icon="bi bi-briefcase-fill"
      />

      <StatCard
        title="Applications"
        :value="dashboard.applications"
        icon="bi bi-file-earmark-text-fill"
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
  drives: 0,
  applications: 0,
  shortlisted: 0,
  rejected: 0,
});
</script>
