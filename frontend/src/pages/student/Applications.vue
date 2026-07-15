<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <PageHeader
        title="My Applications"
        subtitle="View and export your placement applications"
      />

      <button
        class="btn btn-success"
        :disabled="exporting"
        @click="handleExport"
      >
        <span
          v-if="exporting"
          class="spinner-border spinner-border-sm me-2"
        ></span>

        {{ exporting ? "Exporting..." : "Export CSV" }}
      </button>
    </div>

    <DataTable :columns="columns" :rows="applications">
      <template #status="{ row }">
        <span
          class="badge text-capitalize"
          :class="{
            'bg-primary': row.status === 'applied',
            'bg-warning text-dark': row.status === 'in-touch',
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

import {
  getApplications,
  exportApplications,
  getExportStatus,
  downloadExport,
} from "../../api/student";

const applications = ref([]);
const exporting = ref(false);

const columns = [
  { key: "company", label: "Company" },
  { key: "drive", label: "Drive" },
  { key: "status", label: "Status" },
  { key: "applied_at", label: "Applied At" },
];

const load = async () => {
  try {
    const { data } = await getApplications();
    applications.value = data;
  } catch (error) {
    console.error(error);
  }
};

const handleExport = async () => {
  try {
    exporting.value = true;

    const { data } = await exportApplications();

    await checkExportStatus(data.task_id);
  } catch (error) {
    console.error(error);

    alert(error.response?.data?.error || "Failed to start application export");

    exporting.value = false;
  }
};

const checkExportStatus = (taskId) => {
  const interval = setInterval(async () => {
    try {
      const { data } = await getExportStatus(taskId);

      if (data.status === "completed") {
        clearInterval(interval);

        await downloadCSV(data.filename);

        exporting.value = false;
      } else if (data.status === "failed") {
        clearInterval(interval);

        alert("Application export failed");

        exporting.value = false;
      }
    } catch (error) {
      clearInterval(interval);

      console.error(error);

      alert("Failed to check export status");

      exporting.value = false;
    }
  }, 2000);
};

const downloadCSV = async (filename) => {
  try {
    const response = await downloadExport(filename);

    const blob = new Blob([response.data], {
      type: "text/csv",
    });

    const url = window.URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);

    link.click();

    document.body.removeChild(link);

    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error(error);

    alert("Failed to download CSV");
  }
};

onMounted(load);
</script>
