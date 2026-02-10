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
        path: "admin/documents/:id/chunks",
        name: "Chunks",
        component: () => import("../pages/admin/Chunks.vue"),
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

  if (!to.meta.public && !isAuthenticated) {
    next({ name: "Login" });
  } else if (to.name === "Login" && isAuthenticated) {
    next({ name: "Home" });
  } else if (to.meta.role === "admin" && auth.user?.username !== "admin") {
    next({ name: "Home" });
  } else {
    next();
  }
});

export default router;
