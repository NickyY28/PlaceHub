<template>
  <div>
    <PageHeader
      title="My Applications"
      subtitle="Track all your applications"
    />

    <DataTable :columns="columns" :rows="applications">
      <template #status="{ row }">
        <span
          class="badge"
          :class="{
            'bg-warning': row.status === 'applied',

            'bg-info': row.status === 'in-touch',

            'bg-success': row.status === 'shortlisted',

            'bg-danger': row.status === 'rejected',
          }"
        >
          {{ row.status }}
        </span>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";

import DataTable from "../../components/common/DataTable.vue";

import { getApplications } from "../../api/student";

const applications = ref([]);

const columns = [
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

  {
    key: "applied_at",
    label: "Applied At",
  },
];

const load = async () => {
  const { data } = await getApplications();

  applications.value = data;
};

onMounted(load);
</script>
