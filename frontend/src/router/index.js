import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../pages/Login.vue"),
    meta: { public: true },
  },
  {
    path: "/",
    component: () => import("../layouts/DefaultLayout.vue"),
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("../pages/Home.vue"),
      },
      {
        path: "admin",
        name: "Admin",
        component: () => import("../pages/admin/Documents.vue"),
        meta: { role: "admin" },
      },
      {
        path: "admin/documents/upload",
        name: "Upload",
        component: () => import("../pages/admin/Upload.vue"),
      },
      {
        path: "admin/documents/:id/chunks",
        name: "Chunks",
        component: () => import("../pages/admin/Chunks.vue"),
        meta: { role: "admin" },
      },
      {
        path: "admin/failed-jobs",
        name: "FailedJobs",
        component: () => import("../pages/admin/FailedJobs.vue"),
        meta: { role: "admin" },
      },
      {
        path: "user",

        name: "User",
        component: () => import("../pages/User.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  const isAuthenticated = auth.isAuthenticated;

  // 1. If the route is public, let them pass
  if (to.meta.public) {
    // If already logged in and trying to access login, send to home
    if (to.name === "Login" && isAuthenticated) {
      next({ name: "Home" });
    } else {
      next();
    }
    return;
  }

  // 2. If not authenticated and not public, force login
  if (!isAuthenticated) {
    next({ name: "Login" });
    return;
  }

  // 3. Admin specific protection
  if (to.meta.role === "admin" && !auth.isAdmin) {
    next({ name: "Home" });
    return;
  }

  // 4. Default: authenticate allowed
  next();
});

export default router;
