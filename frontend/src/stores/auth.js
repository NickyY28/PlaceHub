import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: null,
    role: "",
    isLoggedIn: !!localStorage.getItem("token"),
  }),

  actions: {
    setAuth(token, user) {
      this.token = token;
      this.user = user;
      this.role = user.role;
      this.isLoggedIn = true;
      localStorage.setItem("token", token);
    },

    logout() {
      this.token = "";
      this.user = null;
      this.role = "";
      this.isLoggedIn = false;
      localStorage.removeItem("token");
    },
  },
});
