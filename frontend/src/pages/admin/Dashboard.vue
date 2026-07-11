<template>
  <div>
    <h3 class="mb-4">Admin Dashboard</h3>

    <div class="row">
      <StatCard
        title="Users"
        :value="dashboard.users"
        icon="bi bi-people-fill"
      />

      <StatCard
        title="Companies"
        :value="dashboard.companies"
        icon="bi bi-building"
      />

      <StatCard
        title="Students"
        :value="dashboard.students"
        icon="bi bi-mortarboard-fill"
      />

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
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import StatCard from "../../components/common/StatCard.vue";

const dashboard = reactive({
  users: 0,
  companies: 0,
  students: 0,
  drives: 0,
  applications: 0,
});
</script>
