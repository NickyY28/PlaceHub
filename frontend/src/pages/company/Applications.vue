<template>
  <div>
    <PageHeader title="Applications" subtitle="Manage student applications" />

    <DataTable :columns="columns" :rows="applications">
      <template #status="{ row }">
        <select class="form-select" v-model="row.status" @change="update(row)">
          <option>applied</option>

          <option>in-touch</option>

          <option>shortlisted</option>

          <option>rejected</option>
        </select>
      </template>
    </DataTable>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";
import { getApplications, updateApplicationStatus } from "../../api/company";

const applications = ref([]);

const columns = [
  { key: "student_name", label: "Student" },
  { key: "college", label: "College" },
  { key: "cgpa", label: "CGPA" },
  { key: "status", label: "Status" },
];

const load = async () => {
  const { data } = await getApplications();
  applications.value = data;
};

const update = async (row) => {
  await updateApplicationStatus(row.application_id, { status: row.status });
};

onMounted(load);
</script>
