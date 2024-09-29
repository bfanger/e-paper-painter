<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { WHITE, BLACK, RED, SCREEN_WIDTH, SCREEN_HEIGHT } from "../constants";
import fileToImage from "../fileToImage";

// eslint-disable-next-line no-undef
const props = defineProps<{
  color: number;
}>();

const canvasRef = ref<HTMLCanvasElement>();
const brush = ref(3);
const scale = ref(3);
const rotated = ref(true);
const width = computed(() => (rotated.value ? SCREEN_HEIGHT : SCREEN_WIDTH));
const height = computed(() => (rotated.value ? SCREEN_WIDTH : SCREEN_HEIGHT));

let previous: { x: number; y: number } | false = false;

let ctx: CanvasRenderingContext2D;
watch(props, () => {
  ctx && setFill(props.color);
});
let canvas: HTMLCanvasElement;
onMounted(() => {
  canvas = canvasRef.value as HTMLCanvasElement;
  ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
  ctx.imageSmoothingEnabled = false;
  setFill(WHITE);
  ctx.fillRect(0, 0, width.value, height.value);
  setFill(props.color);
});
function mousedown(event: MouseEvent) {
  const { top, left } = canvas.getBoundingClientRect();
  const x = Math.floor((event.clientX - left) / scale.value);
  const y = Math.floor((event.clientY - top) / scale.value);
  dot(x, y);
}
function mousemove(event: MouseEvent) {
  if (event.buttons === 0) {
    return false;
  }
  const { top, left } = canvas.getBoundingClientRect(); // @todo only do this on start/mousedown?
  const x = Math.floor((event.clientX - left) / scale.value);
  const y = Math.floor((event.clientY - top) / scale.value);
  lineTo(x, y);
}
function mouseup() {
  previous = false;
}
function touchstart(event: TouchEvent) {
  const touch = event.touches[0];
  const { top, left } = canvas.getBoundingClientRect();
  const x = Math.floor((touch.clientX - left) / scale.value);
  const y = Math.floor((touch.clientY - top) / scale.value);
  dot(x, y);
}
function touchmove(event: TouchEvent) {
  const touch = event.touches[0];
  const { top, left } = canvas.getBoundingClientRect(); // @todo only do this on start/mousedown?
  const x = Math.floor((touch.clientX - left) / scale.value);
  const y = Math.floor((touch.clientY - top) / scale.value);

  lineTo(x, y);
}
function setFill(color: number) {
  switch (color) {
    case BLACK:
      ctx.fillStyle = "#140000";
      break;
    case WHITE:
      ctx.fillStyle = "#dedddb";
      break;
    case RED:
      ctx.fillStyle = "#c81935";
      break;
  }
}
function dot(x: number, y: number) {
  if (brush.value === 1) {
    ctx.fillRect(x, y, 1, 1);
  }
  if (brush.value === 1) {
    ctx.fillRect(x, y, 1, 1);
  }
  if (brush.value === 3) {
    ctx.fillRect(x - 1, y, 3, 1);
    ctx.fillRect(x, y - 1, 1, 3);
  }
  previous = { x, y };
}
function lineTo(x: number, y: number) {
  if (!previous) {
    return;
  }
  const steps = {
    x: Math.max(previous.x, x) - Math.min(previous.x, x),
    y: Math.max(previous.y, y) - Math.min(previous.y, y),
    total: 0,
  };
  steps.total = Math.max(steps.x, steps.y);
  const dx = x > previous.x ? steps.x / steps.total : steps.x / -steps.total;
  const dy = y > previous.y ? steps.y / steps.total : steps.y / -steps.total;
  const start = previous;
  for (let i = 0; i <= steps.total; i++) {
    dot(start.x + Math.round(dx * i), start.y + Math.round(dy * i));
  }
  previous = { x, y };
}

function exportColor(color: number) {
  const { data } = ctx.getImageData(0, 0, width.value, height.value);
  const exportCanvas = document.createElement("canvas") as HTMLCanvasElement;
  exportCanvas.width = SCREEN_WIDTH;
  exportCanvas.height = SCREEN_HEIGHT;
  const target = exportCanvas.getContext("2d") as CanvasRenderingContext2D;
  const threshold = 100;
  const perRow = width.value * 4;
  let fillStyle;
  for (let y = 0; y < height.value; y++) {
    for (let x = 0; x < width.value; x++) {
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
      target.fillStyle = fillStyle as string;
      if (rotated.value) {
        target.fillRect(y, SCREEN_HEIGHT - x, 1, 1);
      } else {
        target.fillRect(x, y, 1, 1);
      }
    }
  }
  return exportCanvas;
}
// eslint-disable-next-line no-undef
defineExpose({ exportColor });

function drop(event: DragEvent) {
  event.preventDefault();
  event.stopPropagation();
  if (!event.dataTransfer || event.dataTransfer.files.length === 0) {
    return;
  }
  fileToImage(event.dataTransfer.files[0]).then((img) => {
    ctx.drawImage(img, 0, 0, width.value, height.value);
  });
}
function dragover(event: DragEvent) {
  event.stopPropagation();
  event.preventDefault();
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = "copy";
  }
}
</script>

<template>
  <canvas
    class="canvas"
    ref="canvasRef"
    :style="{ width: width * scale + 'px' }"
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

<style lang="scss">
.canvas {
  user-select: none;
  cursor: crosshair;
  image-rendering: pixelated;
}
</style>
