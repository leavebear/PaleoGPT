<template>
  <div class="operation-panel">
    <el-row :gutter="20" type="flex" justify="start" align="middle">
      <!-- 标题 -->
      <el-col :span="24">
        <h3 style="margin: 0px 0px 10px 5px;">操作面板</h3>
      </el-col>

      <!-- 输入序号 -->
      <el-col :span="12" style="padding: 0px; margin-bottom: 5px;">
        <el-form-item label="选择序号" style="padding-left: 10px; margin-right: 0px;">
          <el-input v-model="figure" placeholder="请输入序号" style="width: 90%;" />
        </el-form-item>
      </el-col>

      <!-- 输入名称 -->
      <el-col :span="12" style="padding: 0px; margin-bottom: 5px;">
        <el-form-item label="选择名称" style="padding-left: 10px; margin-right: 0px;">
          <el-input v-model="name" placeholder="请输入名称" style="width: 90%;" />
        </el-form-item>
      </el-col>

      <!-- 比例尺选择 -->
      <el-col :span="24" style="padding: 0px; margin-bottom: 5px;">
        <el-form-item label="选择比例尺" style="padding-left: 10px; margin-right: 0px; width: 100%;">
          <el-select 
            v-model="selectedScale" 
            placeholder="选择标尺" 
            style="margin-left: 10px; width: 120px;"
            @change="handleScaleChange"
          >
            <el-option
              v-for="(scale, index) in savedScales"
              :key="index"
              :label="scale.name" 
              :value="index"
            />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12" style="padding: 0px;">
        <el-form-item label="化石宽度" style="padding-left: 10px; margin-right: 0px;">
          <el-input v-model="width" placeholder="宽度" style="width: 60%;" />
          <el-select
            v-model="widthUnit"
            placeholder="Select"
            style="width: 30%"
          >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
          </el-select>

        </el-form-item>
      </el-col>

      <el-col :span="12" style="padding: 0px;">
        <el-form-item label="化石长度" style="padding-left: 10px; margin-right: 0px;">
          <el-input v-model="height" placeholder="长度" style="width: 60%;" />
          <el-select
            v-model="heightUnit"
            placeholder="Select"
            style="width: 30%"
          >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
          </el-select>
        </el-form-item>
      </el-col>


      <!-- 保存按钮 -->
      <el-col :span="24" style="margin-top: 20px;">
        <el-button type="primary" plain @click="saveChanges" style="width: 150px; margin: 0px 0px 5px 10px;">
          保存更改
        </el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { defineProps, defineEmits, defineExpose } from "vue";



// Props：主页面传入选择序号、选择名称，是否准确可选
const props = defineProps({
  initialFigure: {
    type: String,
    default: "", // 默认序号为空
  },
  initialName: {
    type: String,
    default: "", // 默认名称为空
  },
  initialWidth: {
    type: Object,
    default: () => ({ value: null, unit: null }), // 默认宽度为空对象
  },
  initialHeight: {
    type: Object,
    default: () => ({ value: null, unit: null }), // 默认高度为空对象
  },
  savedScales: {
    type: Array,
    default: () => [],
  },
  initialSelectedScale: {
    type: Number,
    default: null,
  },
  currentRect: {
    type: Array,
    default: () => [],
  }
});

// Emit 事件：通知主页面数据更新
const emit = defineEmits(["updateData", "update:selectedScale"]);
const selectedScale = ref(props.initialSelectedScale);

// 响应式数据：序号、名称、是否准确
const figure = ref("");
const name = ref("");

const width = ref("");
const height = ref("");
const widthUnit = ref('cm');
const heightUnit = ref('cm');

const options = [
  {
    value: 'mm',
    label: 'mm',
  },
  {
    value: 'cm',
    label: 'cm',
  },
  {
    value: 'dm',
    label: 'dm',
  },
  {
    value: 'm',
    label: 'm',
  },
]

// 处理比例尺变化
const handleScaleChange = (index) => {
  const selectedScale = props.savedScales[index];
  if (!selectedScale) return;

  // 更新长度和宽度单位
  widthUnit.value = selectedScale.unit; // 假设标尺单位与宽度单位一致
  heightUnit.value = selectedScale.unit; // 假设标尺单位与高度单位一致

  // 计算化石尺寸
  if (props.currentRect && props.currentRect.length === 4) {
    const rect = props.currentRect;
    const widthPixels = rect[2];
    const heightPixels = rect[3];

    // 首先将实际长度转换为厘米
    let actualLengthInCm = parseFloat(selectedScale.actualLength);
    if (selectedScale.unit === 'mm') {
      actualLengthInCm /= 10;
    } else if (selectedScale.unit === 'm') {
      actualLengthInCm *= 100;
    } else if (selectedScale.unit === 'inch') {
      actualLengthInCm *= 2.54;
    }

    // 计算比例
    const scaleValue = parseFloat(selectedScale.pixelLength) / actualLengthInCm;

    // 计算化石尺寸
    const fossilLengthCm = heightPixels / scaleValue;
    const fossilWidthCm = widthPixels / scaleValue;

    // 转换为用户选择的单位
    let lengthConversion = 1;
    let widthConversion = 1;

    switch (heightUnit.value) {
      case 'mm': lengthConversion = 10; break;
      case 'm': lengthConversion = 0.01; break;
      case 'inch': lengthConversion = 0.393701; break;
    }

    switch (widthUnit.value) {
      case 'mm': widthConversion = 10; break;
      case 'm': widthConversion = 0.01; break;
      case 'inch': widthConversion = 0.393701; break;
    }

    height.value = (fossilLengthCm * lengthConversion).toFixed(2);
    width.value = (fossilWidthCm * widthConversion).toFixed(2);
  }
};

watch(() => props.initialSelectedScale, (newVal) => {
  selectedScale.value = newVal;
});

watch(selectedScale, (newVal) => {
  emit("update:selectedScale", newVal);
});


// 监听单位变化重新计算
watch([widthUnit, heightUnit], () => {
  if (selectedScale.value !== null) {
    handleScaleChange(selectedScale.value);
  }
});

// 保存数据到本地存储
const saveData = () => {
  localStorage.setItem(`region_${props.initialFigure}`, JSON.stringify({
    figure: figure.value,
    name: name.value,
    width: { value: width.value, unit: widthUnit.value },
    height: { value: height.value, unit: heightUnit.value },
  }));
};

// 恢复数据
const loadData = () => {
  const savedData = localStorage.getItem(`region_${props.initialFigure}`);
  console.log("从本地存储获取的数据:", savedData);  // 打印从 localStorage 获取的原始数据
  
  if (savedData) {
    const data = JSON.parse(savedData);
    
    figure.value = data.figure;
    name.value = data.name;
    width.value = data.width?.value || "";
    height.value = data.height?.value || "";
    widthUnit.value = data.width?.unit || "cm";
    heightUnit.value = data.height?.unit || "cm";
  } else {
    figure.value = props.initialFigure;
    name.value = props.initialName;
    width.value = props.initialWidth?.value || "";
    height.value = props.initialHeight?.value || "";
    widthUnit.value = props.initialWidth?.unit || "cm";
    heightUnit.value = props.initialHeight?.unit || "cm";
  }
};


// 监听 props 变化
watch(() => props.initialFigure, () => {
  loadData();
  console.log(width)
});

// 挂载时加载数据
onMounted(() => {
  loadData();
});


// 保存按钮的点击事件
const saveChanges = () => {
  saveData();
  emit("updateData", {
    figure: figure.value,
    name: name.value,
    width: { value: width.value, unit: widthUnit.value },
    height: { value: height.value, unit: heightUnit.value },
  });
};

// 动态设置数据的方法：供主页面调用
const setTableData = (newFigure, newName, newWidth = "", newHeight = "", newWidthUnit = "cm", newHeightUnit = "cm") => {
  figure.value = newFigure || "";
  name.value = newName || "";
  width.value = newWidth || "";
  height.value = newHeight || "";
  widthUnit.value = newWidthUnit || "cm";
  heightUnit.value = newHeightUnit || "cm";
};

defineExpose({
  setTableData,
});
// const setTableData = ( newFigure, newName, newWidth, newHeight) => {
//   console.log('开始显示选中的数据newFigure：', newFigure);
//   console.log('开始显示选中的数据newName：', newName);
//   console.log('开始显示选中的数据newWidth：', newWidth);
//   console.log('开始显示选中的数据newHeight：', newHeight);
//   figure.value = newFigure || ""; // 如果未提供值，则保持为空
//   name.value = newName || ""; // 如果未提供值，则保持为空
//   width.value = newWidth || ""; // 如果未提供值，则保持为空
//   height.value = newHeight || ""; // 如果未提供值，则保持为空
// };

// // 暴露方法给主页面
// defineExpose({
//   setTableData,
// });
</script>

<style scoped>
.operation-panel {
  padding: 10px;
  /* border: 1px solid #ccc; */
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  /* border-radius: 8px; */
  background-color: #f9f9f9;
}
</style>
