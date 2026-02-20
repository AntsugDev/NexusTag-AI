import { defineStore } from "pinia";
import api from "../api/axios";

export const useSchedulerStore = defineStore("scheduler", {
  state: () => ({
    info: null,
    loading: false,
    timerId: null,
  }),

  getters: {
    isRunning: (state) => state.info?.is_running || false,
    remainingSeconds: (state) => state.info?.seconds_to_next || 0,
    formattedRemaining: (state) => {
      const seconds = state.info?.seconds_to_next;
      if (seconds === null || seconds === undefined) return "--:--";
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return `${m}:${s.toString().padStart(2, "0")}`;
    },
  },

  actions: {
    async fetchStatus() {
      try {
        const result = await api.get("/api/jobs/status");
        this.info = result.data.result;
      } catch (e) {
        console.error("Error fetching scheduler status:", e);
      }
    },

    startPolling(interval = 30000) {
      if (this.timerId) return;

      this.fetchStatus();
      this.timerId = setInterval(() => {
        this.fetchStatus();
      }, interval);
    },

    stopPolling() {
      if (this.timerId) {
        clearInterval(this.timerId);
        this.timerId = null;
      }
    },
  },
});
