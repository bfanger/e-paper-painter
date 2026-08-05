import { existsSync } from "node:fs";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: existsSync("/.dockerenv")
    ? { host: true, watch: { usePolling: true, interval: 1000 } }
    : undefined,
});
