<template>
  <div>
    <PageHeader title="My Profile" subtitle="Manage your profile" />

    <div class="card shadow-sm">
      <div class="card-body">
        <form @submit.prevent="save">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Name</label>

              <input class="form-control" v-model="form.name" disabled />
            </div>

            <div class="col-md-6 mb-3">
              <label>Email</label>

              <input class="form-control" v-model="form.email" disabled />
            </div>

            <div class="col-md-6 mb-3">
              <label>College</label>

              <input class="form-control" v-model="form.college" />
            </div>

            <div class="col-md-6 mb-3">
              <label>CGPA</label>

              <input class="form-control" v-model="form.cgpa" />
            </div>

            <div class="col-md-12 mb-3">
              <label>Skills</label>

              <input class="form-control" v-model="form.skills" />
            </div>

            <div class="col-md-12 mb-3">
              <label>Resume URL</label>

              <input class="form-control" v-model="form.resume" />
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

import { getProfile, updateProfile } from "../../api/student";

const form = reactive({});

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
