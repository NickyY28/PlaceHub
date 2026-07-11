<template>
  <div>
    <PageHeader title="Placement Drives" subtitle="Browse available drives" />

    <DataTable :columns="columns" :rows="drives">
      <template #actions="{ row }">
        <button class="btn btn-success btn-sm" @click="apply(row.id)">
          Apply
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";

import DataTable from "../../components/common/DataTable.vue";

import { getDrives, applyDrive } from "../../api/student";

const drives = ref([]);

const columns = [
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

  {
    key: "location",
    label: "Location",
  },
];

const load = async () => {
  const { data } = await getDrives();

  drives.value = data;
};

const apply = async (id) => {
  await applyDrive(id);

  alert("Applied Successfully");
};

onMounted(load);
</script>
