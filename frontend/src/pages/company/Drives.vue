<template>
  <div>
    <PageHeader title="Placement Drives" subtitle="Manage all placement drives">
      <template #action>
        <RouterLink to="/company/create-drive" class="btn btn-primary">
          <i class="bi bi-plus-lg"></i>
          Add Drive
        </RouterLink>
      </template>
    </PageHeader>

    <DataTable :columns="columns" :rows="drives">
      <template #actions="{ row }">
        <RouterLink
          :to="`/company/edit-drive/${row.id}`"
          class="btn btn-warning btn-sm me-2"
        >
          Edit
        </RouterLink>

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

import { getDrives, deleteDrive } from "../../api/company";

const drives = ref([]);

const columns = [
  { key: "title", label: "Role" },

  { key: "package", label: "Package" },

  { key: "location", label: "Location" },

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
