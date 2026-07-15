<template>
  <div>
    <PageHeader title="Companies" subtitle="Manage company approvals" />

    <DataTable :columns="columns" :rows="companies">
      <!-- <template #status="{ row }">
        <button
          v-if="row.status !== 'approved'"
          class="btn btn-success btn-sm me-2"
        >
          Approve
        </button>
        <button
          v-else-if="row.status !== 'rejected'"
          class="btn btn-success btn-sm me-2"
        >
          Rejected
        </button>
        <button v-else class="btn btn-success btn-sm me-2">Panding</button>
      </template> -->
      <template #status="{ row }">
        <span
          class="badge"
          :class="{
            'bg-success': row.status === 'approved',
            'bg-danger': row.status === 'rejected',
            'bg-warning text-dark': row.status === 'pending',
          }"
        >
          {{ row.status }}
        </span>
      </template>
      <template #actions="{ row }">
        <button
          v-if="row.status !== 'approved'"
          class="btn btn-success btn-sm me-2"
          @click="updateApproval(row.id, 'approved')"
        >
          Approve
        </button>

        <button
          v-if="row.status !== 'rejected'"
          class="btn btn-danger btn-sm"
          @click="updateApproval(row.id, 'rejected')"
        >
          Reject
        </button>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";
import { getCompanies, updateCompanyApproval } from "../../api/admin";

const companies = ref([]);

const columns = [
  { key: "company_name", label: "Company" },
  { key: "email", label: "Email" },
  { key: "location", label: "Location" },
  { key: "status", label: "Approval Status" },
];

const load = async () => {
  const { data } = await getCompanies();
  companies.value = data.companies;
};

const updateApproval = async (id, status) => {
  await updateCompanyApproval(id, status);
  load();
};

onMounted(load);
</script>
