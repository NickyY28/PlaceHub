<template>
  <PageHeader title="Students" subtitle="Registered Students" />

  <DataTable :columns="columns" :rows="students" />
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";

import { getStudents } from "../../api/admin";

const students = ref([]);

const columns = [
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "college", label: "College" },
  { key: "cgpa", label: "CGPA" },
  { key: "skills", label: "Skills" },
];

const load = async () => {
  const { data } = await getStudents();
  students.value = data;
};

onMounted(load);
</script>
