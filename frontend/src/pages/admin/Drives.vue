<template>
  <div>
    <PageHeader title="Placement Drives" subtitle="All Placement Drives" />

    <DataTable :columns="columns" :rows="drives">
      <template #actions="{ row }">
        <button class="btn btn-danger btn-sm" @click="remove(row.id)">
          Delete
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";

import { getDrives, deleteDrive } from "../../api/admin";

const drives = ref([]);

const columns = [
  { key: "company", label: "Company" },
  { key: "title", label: "Role" },
  { key: "package", label: "Package" },
  { key: "deadline", label: "Deadline" },
];

const load = async () => {
  const { data } = await getDrives();
  drives.value = data;
};

const remove = async (id) => {
  if (!confirm("Delete Drive?")) return;
  await deleteDrive(id);
  load();
};

onMounted(load);
</script>
