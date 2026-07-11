<template>
  <div>
    <PageHeader
      title="Student Dashboard"
      subtitle="Welcome back to PlaceHub 👋"
    />

    <div class="row mb-4">
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

    <div class="row">
      <div class="col-lg-6">
        <DataTable
          :columns="applicationColumns"
          :rows="dashboard.recent_applications"
        />
      </div>

      <div class="col-lg-6">
        <DataTable :columns="driveColumns" :rows="dashboard.latest_drives" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import StatCard from "../../components/common/StatCard.vue";
import DataTable from "../../components/common/DataTable.vue";

import { getDashboard } from "../../api/student";

const dashboard = reactive({
  applied: 0,

  pending: 0,

  shortlisted: 0,

  rejected: 0,

  recent_applications: [],

  latest_drives: [],
});

const applicationColumns = [
  {
    key: "company",
    label: "Company",
  },

  {
    key: "drive",
    label: "Drive",
  },

  {
    key: "status",
    label: "Status",
  },
];

const driveColumns = [
  {
    key: "company",
    label: "Company",
  },

  {
    key: "title",
    label: "Role",
  },

  {
    key: "package",
    label: "Package",
  },
];

const loadDashboard = async () => {
  try {
    const { data } = await getDashboard();

    Object.assign(dashboard, data);
  } catch (err) {
    console.log(err);
  }
};

onMounted(loadDashboard);
</script>
