<template>
  <div>
    <PageHeader title="Admin Dashboard" subtitle="System Overview" />

    <div class="row">
      <StatCard
        title="Users"
        :value="dashboard.total_users"
        icon="bi bi-people-fill"
      />

      <StatCard
        title="Companies"
        :value="dashboard.total_companies"
        icon="bi bi-building"
      />

      <StatCard
        title="Students"
        :value="dashboard.total_students"
        icon="bi bi-mortarboard-fill"
      />

      <StatCard
        title="Drives"
        :value="dashboard.total_drives"
        icon="bi bi-briefcase-fill"
      />

      <StatCard
        title="Applications"
        :value="dashboard.total_applications"
        icon="bi bi-file-earmark-text-fill"
      />
    </div>

    <!-- Monthly Report -->
    <div class="card shadow-sm mt-4">
      <div class="card-body d-flex justify-content-between align-items-center">
        <div>
          <h5 class="card-title mb-1">Monthly Activity Report</h5>

          <p class="text-muted mb-0">
            Generate and download the current month's placement activity report.
          </p>
        </div>

        <button
          class="btn btn-primary"
          :disabled="generatingReport"
          @click="handleGenerateReport"
        >
          <span
            v-if="generatingReport"
            class="spinner-border spinner-border-sm me-2"
          ></span>

          {{ generatingReport ? "Generating..." : "Generate Report" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import StatCard from "../../components/common/StatCard.vue";

import {
  getDashboard,
  generateMonthlyReport,
  getReportStatus,
  downloadReport,
} from "../../api/admin";

const dashboard = reactive({});

const generatingReport = ref(false);

// Load Dashboard
const loadDashboard = async () => {
  try {
    const { data } = await getDashboard();

    Object.assign(dashboard, data);
  } catch (error) {
    console.error("Failed to load dashboard:", error);
  }
};

// Generate Monthly Report
const handleGenerateReport = async () => {
  try {
    generatingReport.value = true;

    const { data } = await generateMonthlyReport();

    checkReportStatus(data.task_id);
  } catch (error) {
    console.error(error);

    alert(error.response?.data?.error || "Failed to generate report");

    generatingReport.value = false;
  }
};

// Check Celery Task Status
const checkReportStatus = (taskId) => {
  const interval = setInterval(async () => {
    try {
      const { data } = await getReportStatus(taskId);

      if (data.status === "completed") {
        clearInterval(interval);

        await downloadMonthlyReport(data.filename);

        generatingReport.value = false;
      } else if (data.status === "failed") {
        clearInterval(interval);

        alert(data.error || "Report generation failed");

        generatingReport.value = false;
      }
    } catch (error) {
      clearInterval(interval);

      console.error(error);

      alert(error.response?.data?.error || "Failed to check report status");

      generatingReport.value = false;
    }
  }, 2000);
};

// Download HTML Report
const downloadMonthlyReport = async (filename) => {
  try {
    const response = await downloadReport(filename);

    const blob = new Blob([response.data], {
      type: "text/html",
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

    alert("Failed to download report");
  }
};

onMounted(() => {
  loadDashboard();
});
</script>
