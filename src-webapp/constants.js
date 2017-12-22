export const WHITE = 0;
export const BLACK = 1;
export const RED = 2;

export const SCREEN_WIDTH = 104;
export const SCREEN_HEIGHT = 212;

const all = { WHITE, BLACK, RED, SCREEN_WIDTH, SCREEN_HEIGHT };
export default all;

export const VueConstantPlugin = {
  install(Vue) {
    Vue.mixin({
      created() {
        for (const [key, value] of Object.entries(all)) {
          this[key] = value;
        }
      }
    });
  }
};
