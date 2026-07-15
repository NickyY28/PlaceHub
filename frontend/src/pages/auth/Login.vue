<template>
  <div class="auth-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-xl-9 col-lg-10">
          <div class="card auth-card border-0 shadow-lg overflow-hidden">
            <div class="row g-0">
              <!-- Left Section -->
              <div class="col-md-5 d-none d-md-flex auth-brand-section">
                <div class="brand-content">
                  <div class="brand-icon mb-4">
                    <i class="bi bi-mortarboard-fill"></i>
                  </div>

                  <h1 class="fw-bold mb-3">PlaceHub</h1>

                  <p class="mb-0">
                    Your complete campus placement portal. Connect students,
                    companies, and institutes in one place.
                  </p>
                </div>
              </div>

              <!-- Login Section -->
              <div class="col-md-7">
                <div class="auth-form-section">
                  <!-- Mobile Logo -->
                  <div class="d-md-none text-center mb-4">
                    <div class="mobile-brand-icon">
                      <i class="bi bi-mortarboard-fill"></i>
                    </div>

                    <h3 class="fw-bold text-primary mt-2">PlaceHub</h3>
                  </div>

                  <div class="mb-4">
                    <h2 class="fw-bold mb-2">Welcome Back</h2>

                    <p class="text-muted mb-0">
                      Sign in to continue to your account
                    </p>
                  </div>

                  <form @submit.prevent="login">
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
                          v-model="email"
                          type="email"
                          class="form-control"
                          placeholder="Enter your email"
                          required
                        />
                      </div>
                    </div>

                    <!-- Password -->
                    <div class="mb-4">
                      <label for="password" class="form-label fw-medium">
                        Password
                      </label>

                      <div class="input-group">
                        <span class="input-group-text bg-white">
                          <i class="bi bi-lock"></i>
                        </span>

                        <input
                          id="password"
                          v-model="password"
                          :type="showPassword ? 'text' : 'password'"
                          class="form-control"
                          placeholder="Enter your password"
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

                    <!-- Login Button -->
                    <button
                      type="submit"
                      class="btn btn-primary w-100 py-2"
                      :disabled="loading"
                    >
                      <span
                        v-if="loading"
                        class="spinner-border spinner-border-sm me-2"
                      ></span>

                      {{ loading ? "Signing in..." : "Sign In" }}
                    </button>
                  </form>

                  <!-- Register Section -->
                  <div class="register-section mt-4">
                    <p class="text-muted text-center mb-3">
                      Don't have an account?
                    </p>

                    <div class="row g-2">
                      <div class="col-6">
                        <RouterLink
                          to="/register/student"
                          class="btn btn-outline-primary w-100"
                        >
                          <i class="bi bi-mortarboard me-1"></i>
                          Student
                        </RouterLink>
                      </div>

                      <div class="col-6">
                        <RouterLink
                          to="/register/company"
                          class="btn btn-outline-primary w-100"
                        >
                          <i class="bi bi-building me-1"></i>
                          Company
                        </RouterLink>
                      </div>
                    </div>
                  </div>

                  <div class="text-center mt-4">
                    <small class="text-muted">
                      Placement Portal Application
                    </small>
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
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../../stores/auth";
import { loginUser, getMe } from "../../api/auth";

const router = useRouter();

const auth = useAuthStore();

const email = ref("");

const password = ref("");

const showPassword = ref(false);

const loading = ref(false);

async function login() {
  try {
    loading.value = true;

    const res = await loginUser({
      email: email.value,
      password: password.value,
    });

    const token = res.data.token;

    localStorage.setItem("token", token);

    const me = await getMe();

    auth.setAuth(token, me.data);

    if (me.data.role === "student") {
      router.push("/student/dashboard");
    } else if (me.data.role === "company") {
      router.push("/company/dashboard");
    } else {
      router.push("/admin/dashboard");
    }
  } catch (err) {
    alert(err.response?.data?.error || "Login Failed");
  } finally {
    loading.value = false;
  }
}
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
  min-height: 570px;
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
  padding: 60px 55px;
  background: white;
  min-height: 570px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-control,
.input-group-text,
.input-group .btn {
  min-height: 48px;
}

.form-control:focus {
  box-shadow: none;
  border-color: #0d6efd;
}

.input-group:focus-within .input-group-text {
  border-color: #0d6efd;
}

.register-section {
  padding-top: 10px;
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
  }

  .auth-form-section {
    padding: 40px 25px;
    min-height: auto;
  }

  .auth-card {
    border-radius: 14px;
  }
}
</style>
