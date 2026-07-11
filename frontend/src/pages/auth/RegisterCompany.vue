<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="text-center mb-4">Company Registration</h3>

            <form @submit.prevent="register">
              <div class="mb-3">
                <label>Company Name</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Email</label>
                <input
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Password</label>
                <input
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Website</label>
                <input
                  v-model="form.website"
                  type="url"
                  class="form-control"
                  placeholder="https://company.com"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Location</label>
                <input
                  v-model="form.location"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  rows="4"
                  required
                ></textarea>
              </div>

              <button class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? "Registering..." : "Register" }}
              </button>
            </form>

            <div class="text-center mt-3">
              <RouterLink to="/login"> Already have an account? </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { registerCompany } from "../../api/auth";
const router = useRouter();
const loading = ref(false);
const form = reactive({
  name: "",
  email: "",
  password: "",
  website: "",
  location: "",
  description: "",
});

const register = async () => {
  try {
    loading.value = true;
    await registerCompany(form);
    alert("Company Registered Successfully");
    router.push("/login");
  } catch (err) {
    alert(err.response?.data?.error || "Registration Failed");
  } finally {
    loading.value = false;
  }
};
</script>
