<template>
  <div>
    <PageHeader title="Applications" subtitle="Manage student applications" />

    <DataTable :columns="columns" :rows="applications">
      <!-- Status -->
      <template #status="{ row }">
        <span class="badge text-capitalize" :class="getStatusClass(row.status)">
          {{ row.status }}
        </span>
      </template>

      <!-- Actions -->
      <template #actions="{ row }">
        <button class="btn btn-primary btn-sm" @click="openModal(row)">
          Update Status
        </button>
      </template>
    </DataTable>

    <!-- Status Modal -->
    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update Application Status</h5>

            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <div class="modal-body">
            <p class="mb-2">
              What do you want to do with
              <strong>{{ selectedApplication?.student_name }}</strong
              >'s application?
            </p>

            <p class="text-muted mb-4">
              Current Status:
              <span
                class="badge text-capitalize"
                :class="getStatusClass(selectedApplication?.status)"
              >
                {{ selectedApplication?.status }}
              </span>
            </p>

            <div class="d-grid gap-2">
              <button
                class="btn btn-info"
                :disabled="updating"
                @click="changeStatus('in-touch')"
              >
                Mark In Touch
              </button>

              <button
                class="btn btn-success"
                :disabled="updating"
                @click="changeStatus('shortlisted')"
              >
                Shortlist
              </button>

              <button
                class="btn btn-danger"
                :disabled="updating"
                @click="changeStatus('rejected')"
              >
                Reject
              </button>
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              :disabled="updating"
              @click="closeModal"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

import PageHeader from "../../components/common/PageHeader.vue";
import DataTable from "../../components/common/DataTable.vue";

import { getApplications, updateApplicationStatus } from "../../api/company";

const applications = ref([]);

const showModal = ref(false);

const selectedApplication = ref(null);

const updating = ref(false);

const columns = [
  {
    key: "student_name",
    label: "Student",
  },
  {
    key: "college",
    label: "College",
  },
  {
    key: "cgpa",
    label: "CGPA",
  },
  {
    key: "status",
    label: "Status",
  },
  {
    key: "actions",
    label: "Actions",
  },
];

const load = async () => {
  try {
    const { data } = await getApplications();

    applications.value = data;
  } catch (error) {
    console.error("Failed to load applications:", error);
  }
};

const openModal = (row) => {
  selectedApplication.value = row;

  showModal.value = true;
};

const closeModal = () => {
  if (updating.value) return;

  showModal.value = false;

  selectedApplication.value = null;
};

const changeStatus = async (status) => {
  if (!selectedApplication.value) return;

  try {
    updating.value = true;

    await updateApplicationStatus(selectedApplication.value.application_id, {
      status: status,
    });

    selectedApplication.value.status = status;

    showModal.value = false;

    selectedApplication.value = null;
  } catch (error) {
    console.error("Failed to update application:", error);

    alert(error.response?.data?.error || "Failed to update application status");
  } finally {
    updating.value = false;
  }
};

const getStatusClass = (status) => {
  switch (status) {
    case "applied":
      return "bg-primary";

    case "in-touch":
      return "bg-info text-dark";

    case "shortlisted":
      return "bg-success";

    case "rejected":
      return "bg-danger";

    default:
      return "bg-secondary";
  }
};

onMounted(load);
</script>
