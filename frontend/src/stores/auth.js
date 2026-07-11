import { defineStore } from "pinia";

const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: JSON.parse(localStorage.getItem("user")) || null,
    role: localStorage.getItem("role") || "",
    isLoggedIn: !!localStorage.getItem("token"),
  }),

  actions: {
    setAuth(token, user) {
      this.token = token;
      this.user = user;
      this.role = user.role;
      this.isLoggedIn = true;
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
      localStorage.setItem("role", user.role);
    },
    logout() {
      this.token = "";
      this.user = null;
      this.role = "";
      this.isLoggedIn = false;
      localStorage.clear();
    },
  },
});

export { useAuthStore };
