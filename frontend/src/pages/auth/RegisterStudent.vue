<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="text-center mb-4">Student Registration</h3>

            <form @submit.prevent="register">
              <div class="mb-3">
                <label>Name</label>
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
                <label>College</label>
                <input
                  v-model="form.college"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>CGPA</label>
                <input
                  v-model="form.cgpa"
                  type="number"
                  step="0.01"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Skills</label>
                <input
                  v-model="form.skills"
                  type="text"
                  class="form-control"
                  placeholder="React, Node.js, Python"
                  required
                />
              </div>

              <div class="mb-3">
                <label>Resume URL</label>
                <input
                  v-model="form.resume_url"
                  type="text"
                  class="form-control"
                  placeholder="https://..."
                  required
                />
              </div>

              <button class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? "Registering..." : "Register" }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="text-center mt-3">
    <p class="text-muted">
      Already have an account?
      <RouterLink to="/login">Login here</RouterLink>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { registerStudent } from "../../api/auth";
const router = useRouter();
const loading = ref(false);

const form = reactive({
  name: "",
  email: "",
  password: "",
  college: "",
  cgpa: "",
  skills: "",
  resume_url: "",
});

const register = async () => {
  try {
    loading.value = true;
    await registerStudent(form);
    alert("Registration Successful");
    router.push("/login");
  } catch (err) {
    alert(err.response?.data?.error || "Registration Failed");
  } finally {
    loading.value = false;
  }
};
</script>
