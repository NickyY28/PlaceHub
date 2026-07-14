<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="fw-bold mb-1">Company Dashboard</h3>
        <p class="text-muted mb-0">
          Welcome back! Here's an overview of your placement activities.
        </p>
      </div>

      <RouterLink to="/company/create-drive" class="btn btn-primary">
        <i class="bi bi-plus-circle me-2"></i>
        Create Drive
      </RouterLink>
    </div>

    <!-- Stats -->
    <div class="row g-4 mb-4">
      <StatCard
        title="Job Drives"
        :value="dashboard.total_drives"
        icon="bi bi-briefcase-fill"
      />

      <StatCard
        title="Applications"
        :value="dashboard.total_applications"
        icon="bi bi-file-earmark-text-fill"
      />

      <StatCard
        title="Shortlisted"
        :value="dashboard.shortlisted"
        icon="bi bi-check-circle-fill"
      />

      <StatCard
        title="Rejected"
        :value="dashboard.rejected"
        icon="bi bi-x-circle-fill"
      />
    </div>

    <div class="row">
      <!-- Recent Jobs -->
      <div class="col-lg-8 mb-4">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-white fw-semibold">Recent Job Posts</div>

          <div class="card-body p-0">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-light">
                <tr>
                  <th>Title</th>
                  <th>Location</th>
                  <th>Package</th>
                  <th>Applications</th>
                </tr>
              </thead>

              <tbody v-if="recentDrives.length">
                <tr v-for="drive in recentDrives" :key="drive.id">
                  <td>{{ drive.title }}</td>
                  <td>{{ drive.location }}</td>
                  <td>{{ drive.package }} LPA</td>
                  <td>{{ drive.no_of_applications }}</td>
                </tr>
              </tbody>

              <tbody v-else>
                <tr>
                  <td colspan="4" class="text-center text-muted py-4">
                    No job posts yet.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import StatCard from "../../components/common/StatCard.vue";
import { getDashboard } from "../../api/company";

const dashboard = reactive({});
const recentDrives = ref([]);

onMounted(async () => {
  const { data } = await getDashboard();
  console.log("Data :", data);
  await Object.assign(dashboard, data);
  recentDrives.value = await data.recent_drives;
});
</script>
