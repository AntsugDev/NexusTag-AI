import axios from "axios";
import { useAuthStore } from "../store/auth";
import router from "../router";

const api = axios.create({
  baseURL: "http://localhost:8081/nexus-tag-ai",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor: Attach Token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response Interceptor: Handle Errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const authStore = useAuthStore();
    let message = "Si è verificato un errore imprevisto";

    if (error.response) {
      // Server responded with a status code out of 2xx range
      message =
        error.response.data.error || error.response.data.message || message;

      if (error.response.status === 401) {
        authStore.logout();
        router.push({ name: "Login" });
      }
    } else if (error.request) {
      // Request was made but no response was received
      message = "Il server non risponde. Controlla la tua connessione.";
    } else {
      // Something happened in setting up the request
      message = error.message;
    }

    // We'll use a custom event or a similar mechanism to notify the UI
    // since we don't have direct access to the Vue app instance toast here
    window.dispatchEvent(new CustomEvent("api-error", { detail: message }));

    return Promise.reject(error);
  },
);

export default api;
