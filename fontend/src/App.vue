<script setup>
import { reactive, provide } from 'vue';
import globalState from './globalState'; // 确保路径正确

// 使用reactive包装全局状态，使其响应式
const state = reactive(globalState);

// 提供全局状态
provide('globalState', state);
</script>

<template>
  <router-view></router-view>
</template>