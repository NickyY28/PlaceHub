<template>
  <PageHeader title="Companies" subtitle="Registered Companies" />

  <DataTable :columns="columns" :rows="companies">
    <template #is_blocked="{ row }">
      <button v-if="row.is_blocked" class="btn btn-warning btn-sm me-2">
        Yes
      </button>
      <button v-else class="btn btn-success btn-sm me-2">No</button>
    </template>
    <template #actions="{ row }">
      <button
        v-if="!row.is_blocked"
        class="btn btn-warning btn-sm me-2"
        @click="block(row.user_id)"
      >
        Block
      </button>

      <button
        v-else
        class="btn btn-success btn-sm me-2"
        @click="unblock(row.user_id)"
      >
        Unblock
      </button>

      <button class="btn btn-danger btn-sm" @click="remove(row.user_id)">
        Delete
      </button>
    </template>
  </DataTable>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";

import {
  getCompanies,
  blockUser,
  unblockUser,
  deleteUser,
} from "../../api/admin";

const companies = ref([]);

const columns = [
  { key: "company_name", label: "Company" },
  { key: "email", label: "Email" },
  { key: "website", label: "Website" },
  { key: "location", label: "Location" },
  { key: "description", label: "Description" },
  { key: "is_blocked", label: "Block" },
];

const block = async (id) => {
  await blockUser(id);
  load();
};

const unblock = async (id) => {
  await unblockUser(id);
  load();
};

const remove = async (id) => {
  if (!confirm("Delete User?")) return;
  await deleteUser(id);
  load();
};

const load = async () => {
  const { data } = await getCompanies();
  console.log(data.companies);
  companies.value = data.companies;
};

onMounted(load);
</script>
