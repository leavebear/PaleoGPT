<template>
  <div class="elements">
    <el-form :inline="true" :model="formInline">
      <el-form-item>
        <span style="font-size: 16px; font-weight: bold"
          >文件选择:&nbsp;&nbsp;&nbsp;&nbsp;</span
        >
        <!-- 文件选择器 -->
        <el-select
          v-model="selectedPdf"
          @change="handlePdfChange"
          placeholder="请选择PDF文件"
          class="pdf-select"
          :options="pdfList"
        >
          <el-option
            v-for="pdf in pdfList"
            :key="pdf"
            :label="pdf"
            :value="pdf"
          />
        </el-select>
      </el-form-item>
      <!--单选框-->
      <el-form-item>
        <el-radio-group v-model="radio1" class="ml-4">
          <el-radio label="1" size="large">精确</el-radio>
          <el-radio label="2" size="large">不精确</el-radio>
        </el-radio-group>
      </el-form-item>
      <!--上下按钮-->
      <el-form-item>
        <el-button type="primary" size="small" @click="LastItem">
          上一项
        </el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="small" @click="NextItem">
          下一项
        </el-button>
      </el-form-item>
    </el-form>

    <el-form
      :inline="true"
      :model="formInline"
      style="display: flex; gap: 10px; align-items: flex-start"
    >
      <el-form-item style="margin: 0; padding: 0">
        <!-- 按钮 -->
        <el-button
          type="primary"
          size="small"
          style="margin-top: 0; z-index: 100"
          @click="pdfVisible"
        >
          {{ buttonText }}
        </el-button>
      </el-form-item>
      <el-form-item style="margin: 0; padding: 0; margin-right: 10px">
        <div class="pdf-content" v-show="isPdfVisible">
          <PdfViewer :pdf-url="pdfUrl" />
        </div>
      </el-form-item>

      <el-form-item style="flex: 1">
        <el-row style="flex-direction: column">
          <!-- 上方静态文本 -->
          <el-col
            style="
              background: #f5f7fa;
              text-align: left;
              font-size: 16px;
              font-weight: bold;
            "
          >
            <span>表格选择：</span>
          </el-col>
          <!-- 中间的横向图片列表 -->
          <el-col style="background: #f5f7fa">
            <div>
              <ImagesViewer
                :images="imagesList"
                @image-clicked="handleImageClick"
              />
            </div>
          </el-col>
          <!-- 下方的大表格 -->
          <el-col style="background: #f5f7fa">
            <!-- 操作按钮 -->
            <el-row style="margin-bottom: 10px">
              <el-button type="primary" size="small" @click="updateTableData"
                >改变表格</el-button
              >
            </el-row>

            <!-- 表格  handleSaveTable是保存表格数据的函数 -->
            <PdfTable
              :initialData="tableData"
              @save-table="handleSaveTable"
              ref="tableRef"
            />
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import PdfViewer from "../../components/PdfViewer.vue";
import ImagesViewer from "../../components/ImagesViewer.vue";
import PdfTable from "../../components/PdfTable.vue";

import axios from "axios"



const pdfUrl = ref("/pdfes/1.pdf"); // 初始显示 1.pdf

const pdfList = ref(["1", "2", "3"]);

const radio1 = ref("1");

const tableRef = ref(null); // 使用 Vue 的 ref 来定义 tableRef

//测试图片
//const imagesList = ["1.jpg", "2.jpg", "3.jpg"];

// 默认的表格尺寸 [行数, 列数]
const tableData = ref([
  ['列 1', '列 2', '列 3'], // 第一行是列头
  ['数据 1-1', '数据 1-2', '数据 1-3'],
  ['数据 2-1', '数据 2-2', '数据 2-3'],
]);

// 响应式变量
const imagesList = ref(["1.jpg", "2.jpg", "3.jpg"]); // 用于存储 tableImg
const tableList = ref([]); // 用于存储 table


// 定义POST请求接口的函数
const fetchTableData = async (pdfId) => {
  try {
    const requestData = {
      pdf_id: pdfId, // 请求体
    };

    // 发送 POST 请求
    const response = await axios.post("http://xxx/api/project/tableExtra", requestData);

    // 解析响应
    const { data } = response.data;

    if (response.data.status_code === 0 && data.tableList) {
      // 遍历 tableList，将 tableImg 和 table 分开存储
      imagesList.value = data.tableList.map((item) => item.tableImg);
      tableList.value = data.tableList.map((item) => item.table);

      console.log("Images List:", imagesList.value);
      console.log("Table List:", tableList.value);
    } else {
      console.error("Error: Invalid status_code or tableList missing in response.");
    }
  } catch (error) {
    console.error("Error fetching table data:", error);
  }
};

// 监听保存事件
const handleSaveTable = (savedData) => {
  console.log("保存的表格数据:", savedData);
};
// 主动更新表格内容
const updateTableData = () => {
  const newData = [
    { col0: "Dave", col1: "40", col2: "Developer" },
    { col0: "Eve", col1: "28", col2: "Product Manager" },
  ];
  tableRef.value.updateTableData(newData); // 调用子组件暴露的方法
};

// 选择的 PDF 文件名
const selectedPdf = ref("");

const isPdfVisible = ref(true); // 控制 PDF 容器显示状态
const buttonText = ref("-"); // 按钮上的文本

// 切换 PDF 显示状态的方法
const pdfVisible = () => {
  isPdfVisible.value = !isPdfVisible.value; // 切换显示状态
  buttonText.value = isPdfVisible.value ? "-" : "+"; // 动态更新按钮文本
};

// 监听文件选择变化
const handlePdfChange = (selectedFileName) => {
  // 这里生成对应的 PDF URL
  const pdfPath = `/pdfes/${selectedFileName}.pdf`; // 这里的路径应与你的文件存放路径一致
  // 更新 pdfUrl
  pdfUrl.value = pdfPath;
};

const LastItem = () => {
  const currentIndex = pdfList.value.indexOf(selectedPdf.value);
  // 计算下一个 PDF 的索引（循环）
  const nextIndex =
    (currentIndex - 1 + pdfList.value.length) % pdfList.value.length;
  // 更新选中值
  selectedPdf.value = pdfList.value[nextIndex];
  handlePdfChange(selectedPdf.value);

  console.log("上一项", nextIndex); // 打印选中的文件名
};
const NextItem = () => {
  const currentIndex = pdfList.value.indexOf(selectedPdf.value);
  // 计算下一个 PDF 的索引（循环）
  const nextIndex = (currentIndex + 1) % pdfList.value.length;
  // 更新选中值
  selectedPdf.value = pdfList.value[nextIndex];
  handlePdfChange(selectedPdf.value);
  console.log("下一项"); // 打印选中的文件名
};

//图片列表点击事件
const selectedImage = ref("");

const handleImageClick = (imageName) => {
  selectedImage.value = imageName;
  console.log("Selected image in parent component:", imageName);
};
</script>

<style scoped>
.pdf-read {
  padding: 20px;
}

.radio-container {
  margin-bottom: 20px;
  text-align: left;
}

.pdf-content {
  position: relative;
  /*  width: 100%;  */
  height: 100%;
  overflow: auto;
  /* 这里可以放置你的 PDF 展示区域的样式 */
}

.pdf-select {
  width: 400px; /* 设置选择器的宽度 */
}
</style>
