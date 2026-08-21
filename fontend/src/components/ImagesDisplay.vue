<template>
  <div class="image-viewer" ref="container">
    <canvas ref="canvas" @click="onCanvasClick" @dblclick="onCanvasDblClick"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick,defineEmits } from "vue";

// Props: 图片 URL 和框的坐标数组
const props = defineProps({
  url: {
    type: String,
    required: true, // 必填，图片的 URL
  },
  pos: {
    type: Array,
    required: true, // 必填，框的坐标数组
  },
});

// 定义响应式变量
const container = ref(null); // 容器引用
const canvas = ref(null); // Canvas 元素引用
const ctx = ref(null); // Canvas 上下文
const scale = ref({ x: 1, y: 1 }); // 缩放比例
const originalWidth = ref(0); // 图片的原始宽度
const originalHeight = ref(0); // 图片的原始高度

const image = ref(null); // 图片对象

const selectedIndex = ref(-1); // 当前被选中的框索引，初始为 -1 表示未选中

// // 定义一个名为 'child-click' 的事件
// const emit = defineEmits();

// 定义两个事件：单击和双击
const emit = defineEmits(['ChosenOne', 'DblClick']);


// 加载图片并获取原始尺寸
const loadImage = () => {
  const img = new Image();
  img.src = props.url;
  img.onload = () => {
    originalWidth.value = img.width;
    originalHeight.value = img.height;
    image.value = img; // 缓存图片
    resizeCanvas(); // 初始化画布
  };
};

// 动态调整 Canvas 尺寸并绘制图片
const resizeCanvas = () => {
  const containerEl = container.value;
  const canvasEl = canvas.value;

  if (!containerEl || !canvasEl) return;

  // 获取容器的宽高
  const { width, height } = containerEl.getBoundingClientRect();

  // 设置 Canvas 的宽高为容器宽高
  canvasEl.width = width;
  canvasEl.height = height;

  // 计算缩放比例
  scale.value.x = width / originalWidth.value;
  scale.value.y = height / originalHeight.value;

  // 重新绘制图片和框
  drawImage();
};

// 绘制图片和框选区域
const drawImage = () => {
  console.log("drawImage");
  if (!image.value || !ctx.value) return;

  // 清空画布
  ctx.value.clearRect(0, 0, canvas.value.width, canvas.value.height);

  // 绘制图片
  ctx.value.drawImage(image.value, 0, 0, canvas.value.width, canvas.value.height);

  // 绘制框选区域
  props.pos.forEach((area, index) => {
    const [x, y, width, height] = area;
    const scaledX = x * scale.value.x;
    const scaledY = y * scale.value.y;
    const scaledWidth = width * scale.value.x;
    const scaledHeight = height * scale.value.y;

    ctx.value.strokeStyle = selectedIndex.value === index ? "red" : "green";
    ctx.value.lineWidth = 2;
    ctx.value.strokeRect(scaledX, scaledY, scaledWidth, scaledHeight);
  });
};

// 单击 Canvas 时的事件处理
const onCanvasClick = (event) => {
  const { offsetX, offsetY } = event; // 获取鼠标单击的坐标（相对于 canvas）

  let found = false; // 用于标记是否找到框
  props.pos.forEach((area, index) => {
    const [x, y, width, height] = area;

    // 计算缩放后的框的坐标和大小
    const scaledX = x * scale.value.x;
    const scaledY = y * scale.value.y;
    const scaledWidth = width * scale.value.x;
    const scaledHeight = height * scale.value.y;

    // 判断单击的坐标是否在框内
    if (
      offsetX >= scaledX &&
      offsetX <= scaledX + scaledWidth &&
      offsetY >= scaledY &&
      offsetY <= scaledY + scaledHeight
    ) {
      selectedIndex.value = index; // 记录选中的框索引
      found = true; // 标记找到框
    }
  });

  if (!found) {
    selectedIndex.value = -1; // 如果没有找到框，重置选中的索引
  }

  console.log("选择的框索引:", selectedIndex.value);
  drawImage(); // 重新绘制画布
  // 触发 'ChosenOne' 事件，将值传递给父组件
  emit('ChosenOne', selectedIndex.value);

  
};

// 双击 Canvas 时的事件处理
const onCanvasDblClick = (event) => {
  const { offsetX, offsetY } = event; // 获取鼠标双击的坐标（相对于 canvas）

  let found = false; // 用于标记是否找到框
  props.pos.forEach((area, index) => {
    const [x, y, width, height] = area;

    // 计算缩放后的框的坐标和大小
    const scaledX = x * scale.value.x;
    const scaledY = y * scale.value.y;
    const scaledWidth = width * scale.value.x;
    const scaledHeight = height * scale.value.y;

    // 判断双击的坐标是否在框内
    if (
      offsetX >= scaledX &&
      offsetX <= scaledX + scaledWidth &&
      offsetY >= scaledY &&
      offsetY <= scaledY + scaledHeight
    ) {
      selectedIndex.value = index; // 记录选中的框索引
      found = true; // 标记找到框
    }
  });

  if (!found) {
    selectedIndex.value = -1; // 如果没有找到框，重置选中的索引
  }

  console.log("双击选择的框索引:", selectedIndex.value);
  // 触发 'DblClick' 事件，将值传递给父组件
  emit('DblClick', selectedIndex.value);

  drawImage(); // 重新绘制画布
};

/* 
// 监听容器大小变化
const observeContainerResize = () => {
  const containerEl = container.value;
  if (!containerEl) return;

  // 使用 ResizeObserver 监听容器尺寸变化
  const resizeObserver = new ResizeObserver(() => {
    resizeCanvas(); // 当容器尺寸变化时调整 Canvas
  });

  resizeObserver.observe(containerEl);
};

// 监听 Props 的变化
watch(
  () => [props.url, props.pos],
  () => {
    nextTick(() => {
      drawImage();
    });
  },
  { deep: true }
);
*/
// 初始化
onMounted(() => {
  console.log(props.pos);
  const canvasEl = canvas.value;
  ctx.value = canvasEl.getContext("2d"); // 获取 Canvas 上下文
  loadImage(); // 加载图片
  // observeContainerResize(); // 监听容器大小变化
});
</script>

<style scoped>
.image-viewer {
  width: 100%; /* 容器宽度 */
  height: 500px; /* 容器高度 */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  background-color: #f9f9f9;
}

canvas {
  display: block;
  cursor: default;
}
</style>
