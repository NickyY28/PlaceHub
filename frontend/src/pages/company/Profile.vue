<template>
  <div>
    <PageHeader title="Company Profile" subtitle="Manage your profile" />

    <div class="card shadow-sm">
      <div class="card-body">
        <form @submit.prevent="save">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Company Name</label>

              <input
                class="form-control"
                v-model="form.company_name"
                disabled
              />
            </div>

            <div class="col-md-6 mb-3">
              <label>Email</label>

              <input class="form-control" v-model="user.email" disabled />
            </div>

            <div class="col-md-6 mb-3">
              <label>Description</label>

              <input class="form-control" v-model="form.description" />
            </div>

            <div class="col-md-6 mb-3">
              <label>Location</label>

              <input class="form-control" v-model="form.location" />
            </div>

            <div class="col-md-12 mb-3">
              <label>Wbsite URL</label>

              <input class="form-control" v-model="form.website" />
            </div>
          </div>

          <button class="btn btn-primary">Save Changes</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import PageHeader from "../../components/common/PageHeader.vue";
import { getProfile, updateProfile } from "../../api/company";

const form = reactive({});
const user = JSON.parse(localStorage.getItem("user"));

const loadProfile = async () => {
  const { data } = await getProfile();
  Object.assign(form, data);
};

const save = async () => {
  await updateProfile(form);
  alert("Profile Updated");
};

onMounted(loadProfile);
</script>
