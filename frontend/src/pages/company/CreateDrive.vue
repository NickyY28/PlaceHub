<template>
  <div>
    <PageHeader title="Create Drive" subtitle="Create new placement drive" />

    <div class="card shadow-sm">
      <div class="card-body">
        <form @submit.prevent="save">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Title</label>

              <input class="form-control" v-model="form.title" />
            </div>

            <div class="col-md-6 mb-3">
              <label>Package</label>

              <input class="form-control" v-model="form.package" />
            </div>

            <div class="col-md-6 mb-3">
              <label>Location</label>

              <input class="form-control" v-model="form.location" />
            </div>

            <div class="col-md-6 mb-3">
              <label>Deadline</label>

              <input type="date" class="form-control" v-model="form.deadline" />
            </div>

            <div class="col-md-12 mb-3">
              <label>Eligibility</label>

              <input class="form-control" v-model="form.eligibility" />
            </div>

            <div class="col-md-12 mb-3">
              <label>Description</label>

              <textarea
                rows="5"
                class="form-control"
                v-model="form.description"
              />
            </div>
          </div>

          <button class="btn btn-primary">Create Drive</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { useRouter } from "vue-router";
import PageHeader from "../../components/common/PageHeader.vue";
import { createDrive } from "../../api/company";

const router = useRouter();

const form = reactive({
  title: "",
  description: "",
  package: "",
  location: "",
  deadline: "",
  eligibility: "",
});

const save = async () => {
  await createDrive(form);
  router.push("/company/drives");
};
</script>
