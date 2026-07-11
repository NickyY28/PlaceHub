<template>
  <PageHeader title="Companies" subtitle="Registered Companies" />

  <DataTable :columns="columns" :rows="companies" />
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";

import { getCompanies } from "../../api/admin";

const companies = ref([]);

const columns = [
  { key: "company_name", label: "Company" },
  { key: "email", label: "Email" },
  { key: "website", label: "Website" },
  { key: "location", label: "Location" },
];

const load = async () => {
  const { data } = await getCompanies();
  companies.value = data;
};

onMounted(load);
</script>
