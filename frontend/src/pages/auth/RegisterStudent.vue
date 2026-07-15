<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-11">
          <div class="card auth-card border-0 shadow-lg overflow-hidden">
            <div class="row g-0">
              <!-- Left Branding Section -->
              <div class="col-md-5 d-none d-md-flex auth-brand-section">
                <div class="brand-content">
                  <div class="brand-icon mb-4">
                    <i class="bi bi-mortarboard-fill"></i>
                  </div>

                  <h1 class="fw-bold mb-3">PlaceHub</h1>

                  <h4 class="mb-3">Start your career journey.</h4>

                  <p class="mb-0">
                    Create your student profile, discover placement
                    opportunities, apply to company drives, and track your
                    applications in one place.
                  </p>
                </div>
              </div>

              <!-- Registration Form -->
              <div class="col-md-7">
                <div class="auth-form-section">
                  <!-- Mobile Branding -->
                  <div class="d-md-none text-center mb-4">
                    <div class="mobile-brand-icon">
                      <i class="bi bi-mortarboard-fill"></i>
                    </div>

                    <h3 class="fw-bold text-primary mt-2">PlaceHub</h3>
                  </div>

                  <!-- Heading -->
                  <div class="mb-4">
                    <h2 class="fw-bold mb-2">Student Registration</h2>

                    <p class="text-muted mb-0">
                      Create your account and explore placement opportunities
                    </p>
                  </div>

                  <form @submit.prevent="register">
                    <!-- Name -->
                    <div class="mb-3">
                      <label for="name" class="form-label fw-medium">
                        Full Name
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-person"></i>
                        </span>

                        <input
                          id="name"
                          v-model="form.name"
                          type="text"
                          class="form-control"
                          placeholder="Enter your full name"
                          required
                        />
                      </div>
                    </div>

                    <!-- Email -->
                    <div class="mb-3">
                      <label for="email" class="form-label fw-medium">
                        Email Address
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-envelope"></i>
                        </span>

                        <input
                          id="email"
                          v-model="form.email"
                          type="email"
                          class="form-control"
                          placeholder="Enter your email"
                          required
                        />
                      </div>
                    </div>

                    <!-- Password -->
                    <div class="mb-3">
                      <label for="password" class="form-label fw-medium">
                        Password
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-lock"></i>
                        </span>

                        <input
                          id="password"
                          v-model="form.password"
                          :type="showPassword ? 'text' : 'password'"
                          class="form-control"
                          placeholder="Create a password"
                          required
                        />

                        <button
                          type="button"
                          class="btn btn-outline-secondary"
                          @click="showPassword = !showPassword"
                        >
                          <i
                            :class="
                              showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'
                            "
                          ></i>
                        </button>
                      </div>
                    </div>

                    <!-- College -->
                    <div class="mb-3">
                      <label for="college" class="form-label fw-medium">
                        College
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-building"></i>
                        </span>

                        <input
                          id="college"
                          v-model="form.college"
                          type="text"
                          class="form-control"
                          placeholder="Enter your college name"
                          required
                        />
                      </div>
                    </div>

                    <!-- CGPA + Skills -->
                    <div class="row">
                      <div class="col-md-4 mb-3">
                        <label for="cgpa" class="form-label fw-medium">
                          CGPA
                        </label>

                        <input
                          id="cgpa"
                          v-model="form.cgpa"
                          type="number"
                          step="0.01"
                          min="0"
                          max="10"
                          class="form-control"
                          placeholder="8.50"
                          required
                        />
                      </div>

                      <div class="col-md-8 mb-3">
                        <label for="skills" class="form-label fw-medium">
                          Skills
                        </label>

                        <div class="input-group">
                          <span class="input-group-text bg-white">
                            <i class="bi bi-code-slash"></i>
                          </span>

                          <input
                            id="skills"
                            v-model="form.skills"
                            type="text"
                            class="form-control"
                            placeholder="React, Node.js, Python"
                            required
                          />
                        </div>
                      </div>
                    </div>

                    <!-- Resume URL -->
                    <div class="mb-4">
                      <label for="resume" class="form-label fw-medium">
                        Resume URL
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-file-earmark-person"></i>
                        </span>

                        <input
                          id="resume"
                          v-model="form.resume_url"
                          type="url"
                          class="form-control"
                          placeholder="https://example.com/resume.pdf"
                          required
                        />
                      </div>

                      <small class="text-muted">
                        Add a publicly accessible link to your resume.
                      </small>
                    </div>

                    <!-- Register Button -->
                    <button
                      type="submit"
                      class="btn btn-primary w-100 py-2"
                      :disabled="loading"
                    >
                      <span
                        v-if="loading"
                        class="spinner-border spinner-border-sm me-2"
                      ></span>

                      {{ loading ? "Creating Account..." : "Register Student" }}
                    </button>
                  </form>

                  <!-- Login -->
                  <div class="login-section text-center mt-4">
                    <span class="text-muted"> Already have an account? </span>

                    <RouterLink
                      to="/login"
                      class="text-decoration-none fw-medium ms-1"
                    >
                      Sign In
                    </RouterLink>
                  </div>

                  <!-- Company Registration -->
                  <div class="text-center mt-3">
                    <small class="text-muted"> Are you a company? </small>

                    <RouterLink
                      to="/register/company"
                      class="text-decoration-none ms-1"
                    >
                      Register as Company
                    </RouterLink>
                  </div>
                </div>
              </div>
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

import { registerStudent } from "../../api/auth";

const router = useRouter();

const loading = ref(false);

const showPassword = ref(false);

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

<style scoped>
.auth-page {
  min-height: 100vh;
  /* background: #f4f7fb; */
  display: flex;
  align-items: center;
  padding: 40px 0;
}

.auth-card {
  border-radius: 18px;
}

.auth-brand-section {
  min-height: 750px;
  background: linear-gradient(135deg, #0d6efd, #084298);
  color: white;
  align-items: center;
  justify-content: center;
  padding: 50px 40px;
}

.brand-content {
  max-width: 320px;
}

.brand-content h1 {
  font-size: 42px;
}

.brand-content p {
  line-height: 1.7;
  opacity: 0.9;
}

.brand-icon {
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 34px;
}

.auth-form-section {
  padding: 45px 55px;
  background: white;
  min-height: 750px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-control,
.input-group-text,
.input-group .btn {
  min-height: 46px;
}

.form-control:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.input-group:focus-within .input-group-text {
  border-color: #0d6efd;
}

.login-section {
  padding-top: 18px;
  border-top: 1px solid #eee;
}

.mobile-brand-icon {
  width: 55px;
  height: 55px;
  margin: auto;
  border-radius: 14px;
  background: #0d6efd;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 27px;
}

@media (max-width: 767px) {
  .auth-page {
    padding: 20px 10px;
    align-items: flex-start;
  }

  .auth-form-section {
    padding: 35px 25px;
    min-height: auto;
  }

  .auth-card {
    border-radius: 14px;
  }
}
</style>
