import Vue from "vue";
import App from "./components/App.vue";
import { VueConstantPlugin } from "./constants";

Vue.use(VueConstantPlugin);
const app = new Vue(App).$mount();
document.body.appendChild(app.$el);
document.getElementById("loading-placeholder").remove();
