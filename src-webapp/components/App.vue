<template>
    <div>
      <PaintCanvas ref="canvas" :color="color"/>
      <div class="app__colors">
        <div class="app__color app__color--white" :class="{'app__color--active': color == WHITE}" @click="color = WHITE"></div>
        <div class="app__color app__color--black" :class="{'app__color--active': color == BLACK}" @click="color = BLACK"></div>
        <div class="app__color app__color--red" :class="{'app__color--active': color == RED}" @click="color = RED"></div>
      </div>
      <button @click="save">Save</button>
      <div ref="output"></div>
    </div>
</template>

<script>
import PaintCanvas from "./Canvas.vue";
import { BLACK, RED } from "../constants";
export default {
  data: () => ({
    color: BLACK
  }),
  components: { PaintCanvas },
  methods: {
    async save() {
      const black = this.$refs.canvas.export(BLACK);
      const red = this.$refs.canvas.export(RED);
      const response = await fetch("api/print", {
        method: "POST",
        body: JSON.stringify({
          black: black.toDataURL(),
          red: red.toDataURL()
        }),
        headers: { "Content-Type": "application/json" }
      });
      const result = await response.json();
      console.log(result);
    }
  }
};
</script>

<style lang="scss">
html {
  background: darkgreen;
}
.app__colors {
  display: flex;
  flex-direction: row;
}
.app__color {
  border: 2px solid black;
  width: 30px;
  height: 30px;
  margin-right: 10px;
  cursor: pointer;
}
.app__color--active {
  border-color: orange;
}
.app__color--white {
  background: rgb(255, 255, 255);
}
.app__color--black {
  background: rgb(0, 0, 0);
}
.app__color--red {
  background: rgb(220, 0, 0);
}
</style>
