import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "./stores/auth";

// Layouts
import AuthLayout from "./layouts/AuthLayout.vue";
import StudentLayout from "./layouts/StudentLayout.vue";
import CompanyLayout from "./layouts/CompanyLayout.vue";
import AdminLayout from "./layouts/AdminLayout.vue";

// authentication pages
import Login from "./pages/auth/Login.vue";
import RegisterStudent from "./pages/auth/RegisterStudent.vue";
import RegisterCompany from "./pages/auth/RegisterCompany.vue";

// Students Pages
import StudentDashboard from "./pages/student/Dashboard.vue";
import StudentProfile from "./pages/student/Profile.vue";
import StudentDrives from "./pages/student/Drives.vue";
import StudentApplications from "./pages/student/Applications.vue";

// Companies Pages
import CompanyDashboard from "./pages/company/Dashboard.vue";
import CompanyProfile from "./pages/company/Profile.vue";
import CompanyDrives from "./pages/company/Drives.vue";
import CompanyCreateDrive from "./pages/company/CreateDrive.vue";
import CompanyEditDrive from "./pages/company/EditDrive.vue";
import CompanyApplications from "./pages/company/Applications.vue";

// Admin Pages
import AdminDashboard from "./pages/admin/Dashboard.vue";
import Users from "./pages/admin/Users.vue";
import Companies from "./pages/admin/Companies.vue";
import Students from "./pages/admin/Students.vue";
import Drives from "./pages/admin/Drives.vue";

const routes = [
  {
    path: "/",
    component: AuthLayout,
    children: [
      {
        path: "",
        redirect: "/login",
      },

      {
        path: "/login",
        component: Login,
      },

      {
        path: "/register/student",
        component: RegisterStudent,
      },

      {
        path: "/register/company",
        component: RegisterCompany,
      },
    ],
  },
  {
    path: "/student",
    component: StudentLayout,
    meta: {
      requiresAuth: true,
      role: "student",
    },
    children: [
      {
        path: "dashboard",
        component: StudentDashboard,
      },
      {
        path: "profile",
        component: StudentProfile,
      },
      {
        path: "drives",
        component: StudentDrives,
      },
      {
        path: "applications",
        component: StudentApplications,
      },
    ],
  },

  {
    path: "/company",
    component: CompanyLayout,
    meta: {
      requiresAuth: true,
      role: "company",
    },
    children: [
      {
        path: "dashboard",
        component: CompanyDashboard,
      },

      {
        path: "profile",
        component: CompanyProfile,
      },

      {
        path: "drives",
        component: CompanyDrives,
      },

      {
        path: "create-drive",
        component: CompanyCreateDrive,
      },

      {
        path: "edit-drive/:id",
        component: CompanyEditDrive,
      },

      {
        path: "applications",
        component: CompanyApplications,
      },
    ],
  },

  {
    path: "/admin",
    component: AdminLayout,
    meta: {
      requiresAuth: true,
      role: "admin",
    },
    children: [
      {
        path: "dashboard",
        component: AdminDashboard,
      },
      {
        path: "users",
        component: Users,
      },
      {
        path: "companies",
        component: Companies,
      },
      {
        path: "students",
        component: Students,
      },
      {
        path: "drives",
        component: Drives,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return "/login";
  }

  if (to.meta.role && auth.role && auth.role !== to.meta.role) {
    if (auth.role === "student") return "/student/dashboard";
    if (auth.role === "company") return "dashboard";
    if (auth.role === "admin") return "/admin/dashboard";
  }
});

export default router;
