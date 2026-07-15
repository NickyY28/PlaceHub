<template>
  <div>
    <PageHeader title="Admin Dashboard" subtitle="System Overview" />

    <div class="row">
      <StatCard
        title="Users"
        :value="dashboard.total_users"
        icon="bi bi-people-fill"
      />

      <StatCard
        title="Companies"
        :value="dashboard.total_companies"
        icon="bi bi-building"
      />

      <StatCard
        title="Students"
        :value="dashboard.total_students"
        icon="bi bi-mortarboard-fill"
      />

      <StatCard
        title="Drives"
        :value="dashboard.total_drives"
        icon="bi bi-briefcase-fill"
      />

      <StatCard
        title="Applications"
        :value="dashboard.total_applications"
        icon="bi bi-file-earmark-text-fill"
      />
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import PageHeader from "../../components/common/PageHeader.vue";
import StatCard from "../../components/common/StatCard.vue";
import { getDashboard } from "../../api/admin";

const dashboard = reactive({});

onMounted(async () => {
  const { data } = await getDashboard();
  console.log("Data", data);

  await Object.assign(dashboard, data);
});
</script>
