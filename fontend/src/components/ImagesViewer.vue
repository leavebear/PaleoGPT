<template>
  <el-row style="overflow-x: auto; white-space: nowrap; padding: 10px">
    <div
      v-for="image in props.images"
      :key="image"
      style="display: inline-block; margin-right: 10px; cursor: pointer"
      @click="handleClick(image)"
    >
      <img
        :src="`${image}`"
        :alt="image"
        style="
          width: 100px;
          height: 100px;
          object-fit: cover;
          border: 1px solid #ccc;
        "
      />
    </div>
  </el-row>
</template>

<script setup>
import { onMounted,watch,ref  } from 'vue'
//const images = ["1.jpg", "2.jpg", "3.jpg"]; // 图片文件名数组

const props = defineProps({
  images: {
    type: Array,
    required: true
  }
});


// 定义事件
const emit = defineEmits(['image-clicked']);

//imageName其实是大图的url
const handleClick = (imageName) => {
  emit('image-clicked', imageName); // 触发事件，将图片名称传递到父组件
};

</script>
