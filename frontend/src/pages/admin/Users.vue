<template>
  <div>
    <PageHeader title="Users" subtitle="Manage users" />

    <DataTable :columns="columns" :rows="users">
      <template #actions="{ row }">
        <button
          v-if="!row.is_blocked"
          class="btn btn-warning btn-sm me-2"
          @click="block(row.id)"
        >
          Block
        </button>

        <button
          v-else
          class="btn btn-success btn-sm me-2"
          @click="unblock(row.id)"
        >
          Unblock
        </button>

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

import { getUsers, blockUser, unblockUser, deleteUser } from "../../api/admin";

const users = ref([]);

const columns = [
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "role", label: "Role" },
];

const load = async () => {
  const { data } = await getUsers();
  users.value = data.users;
};

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

onMounted(load);
</script>
