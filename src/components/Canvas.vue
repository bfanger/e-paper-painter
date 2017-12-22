<template>
    <canvas
      class="canvas" 
      :style="{width: (width * scale) + 'px'}" 
      :width="width" 
      :height="height" 
      @mousedown="mousedown"
      @mousemove="mousemove"
      @mouseup="mouseup"
      @drop="drop"
      @dragover="dragover"
      @touchstart.prevent="touchstart"
      @touchmove.prevent="touchmove"
    />
</template>

<script>
import { WHITE, BLACK, RED, SCREEN_WIDTH, SCREEN_HEIGHT } from "../constants";
import fileToImage from "../fileToImage";
export default {
  props: {
    color: Number
  },
  data: () => ({
    brush: 3,
    scale: 3,
    rotated: true
  }),
  watch: {
    color(color) {
      this.setFill(color);
    }
  },
  computed: {
    width() {
      return this.rotated ? SCREEN_HEIGHT : SCREEN_WIDTH;
    },
    height() {
      return this.rotated ? SCREEN_WIDTH : SCREEN_HEIGHT;
    }
  },
  mounted() {
    this.ctx = this.$el.getContext("2d");
    this.ctx.imageSmoothingEnabled = false;
    this.setFill(WHITE);
    this.ctx.fillRect(0, 0, this.width, this.height);
    this.setFill(this.color);
  },
  methods: {
    mousedown(event) {
      const { top, left } = this.$el.getBoundingClientRect();
      const x = Math.floor((event.clientX - left) / this.scale);
      const y = Math.floor((event.clientY - top) / this.scale);
      this.dot(x, y);
    },
    mousemove(event) {
      if (event.buttons === 0) {
        return false;
      }
      const { top, left } = this.$el.getBoundingClientRect(); // @todo only do this on start/mousedown?
      const x = Math.floor((event.clientX - left) / this.scale);
      const y = Math.floor((event.clientY - top) / this.scale);

      this.lineTo(x, y);
    },
    mouseup() {
      this.previous = false;
    },
    touchstart(event) {
      const touch = event.touches[0];
      const { top, left } = this.$el.getBoundingClientRect();
      const x = Math.floor((touch.clientX - left) / this.scale);
      const y = Math.floor((touch.clientY - top) / this.scale);
      this.dot(x, y);
    },
    touchmove(event) {
      const touch = event.touches[0];
      const { top, left } = this.$el.getBoundingClientRect(); // @todo only do this on start/mousedown?
      const x = Math.floor((touch.clientX - left) / this.scale);
      const y = Math.floor((touch.clientY - top) / this.scale);

      this.lineTo(x, y);
    },
    setFill(color) {
      switch (color) {
        case BLACK:
          this.ctx.fillStyle = "#140000";
          break;
        case WHITE:
          this.ctx.fillStyle = "#dedddb";
          break;
        case RED:
          this.ctx.fillStyle = "#c81935";
          break;
      }
    },
    dot(x, y) {
      if (this.brush === 1) {
        this.ctx.fillRect(x, y, 1, 1);
      }
      if (this.brush === 1) {
        this.ctx.fillRect(x, y, 1, 1);
      }
      if (this.brush === 3) {
        this.ctx.fillRect(x - 1, y, 3, 1);
        this.ctx.fillRect(x, y - 1, 1, 3);
      }
      this.previous = { x, y };
    },
    lineTo(x, y) {
      if (!this.previous) {
        return;
      }
      const steps = {
        x: Math.max(this.previous.x, x) - Math.min(this.previous.x, x),
        y: Math.max(this.previous.y, y) - Math.min(this.previous.y, y),
        total: 0
      };
      steps.total = Math.max(steps.x, steps.y);
      const dx =
        x > this.previous.x ? steps.x / steps.total : steps.x / -steps.total;
      const dy =
        y > this.previous.y ? steps.y / steps.total : steps.y / -steps.total;
      const start = this.previous;
      for (let i = 0; i <= steps.total; i++) {
        this.dot(start.x + Math.round(dx * i), start.y + Math.round(dy * i));
      }
      this.previous = { x, y };
    },
    export(color) {
      const { data } = this.ctx.getImageData(0, 0, this.width, this.height);

      const canvas = document.createElement("canvas");
      canvas.width = SCREEN_WIDTH;
      canvas.height = SCREEN_HEIGHT;
      const ctx = canvas.getContext("2d");
      const threshold = 100;
      const perRow = this.width * 4;
      let fillStyle;
      for (let y = 0; y < this.height; y++) {
        for (let x = 0; x < this.width; x++) {
          const offset = y * perRow + x * 4;
          if (color === BLACK) {
            fillStyle = data[offset] < threshold ? "black" : "white"; // no red? must be black
          }
          if (color === RED) {
            if (data[offset] < threshold) {
              // no red? must be black
              fillStyle = "white";
            } else if (
              data[offset + 1] < threshold &&
              data[offset + 2] < threshold
            ) {
              // no green & blue? must be red
              fillStyle = "black";
            } else {
              // probably white
              fillStyle = "white";
            }
          }
          ctx.fillStyle = fillStyle;
          if (this.rotated) {
            console.log();
            ctx.fillRect(y, SCREEN_HEIGHT - x, 1, 1);
          } else {
            ctx.fillRect(x, y, 1, 1);
          }
        }
      }
      return canvas;
    },

    drop(event) {
      event.preventDefault();
      event.stopPropagation();
      if (!event.dataTransfer || event.dataTransfer.files.length === 0) {
        return;
      }
      fileToImage(event.dataTransfer.files[0]).then(img => {
        this.ctx.drawImage(img, 0, 0, this.width, this.height);
      });
    },
    dragover(event) {
      event.stopPropagation();
      event.preventDefault();
      event.dataTransfer.dropEffect = "copy";
    }
  }
};
</script>

<style lang="scss">
.canvas {
  user-select: none;
  cursor: crosshair;
  image-rendering: pixelated;
}
</style>
