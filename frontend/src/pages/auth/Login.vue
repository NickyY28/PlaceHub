<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="text-center mb-4">PlaceHub Login</h3>

            <form @submit.prevent="login">
              <div class="mb-3">
                <label>Email</label>

                <input v-model="email" type="email" class="form-control" />
              </div>

              <div class="mb-3">
                <label>Password</label>

                <input
                  v-model="password"
                  type="password"
                  class="form-control"
                />
              </div>

              <button class="btn btn-primary w-100">Login</button>
            </form>
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

async function login() {
  try {
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
  }
}
</script>
