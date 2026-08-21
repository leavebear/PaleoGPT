<template>
  <div class="elements">
    <el-form :inline="true" :model="formInline">
      <div class="search-container">
      <el-form-item>
        <!-- <span style="font-size: 16px; font-weight: bold"
          >文件选择:&nbsp;&nbsp;&nbsp;&nbsp;</span
        > -->
        <!-- 文件选择器 -->
        <!-- SVG 图标 -->
        <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32"><path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path></svg>
        <!-- 搜索框 -->
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
    </div>
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

      <el-form-item style="flex: 1; display: flex; flex-direction: column">
        <el-row
          style="flex: 1; display: flex; flex-direction: column; height: 100%"
        >
          <!-- 上方静态文本 -->
          <el-col
            style="
              background: #f5f7fa;
              text-align: left;
              font-size: 16px;
              font-weight: bold;
            "
          >
            <span>大图列表：</span>
          </el-col>

          <!-- 中间的横向图片列表 -->
          <el-col style="background: #f5f7fa; flex: 1">
            <div>
              <ImagesViewer
                :images="imagesList"
                @image-clicked="handleImageClick"
              />
            </div>
          </el-col>
          <!-- 下方的子图片显示 -->
          <el-col style="background: #f5f7fa; flex: 1">
            <!-- 小图组件占位 -->
            <div>
              <ImagesDisplay :url="`/images/Test.png`" :pos="poses" />
            </div>
          </el-col>

          <!-- 小图信息展示 -->
          <el-col style="background: #f5f7fa; flex: 1">
            <ImagesTable
              :initialFigure="imageTable[0]"
              :initialName="imageTable[1]"
              @updateTable="handleUpdateTable"
            />
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import PdfViewer from "../../components/PdfViewer.vue";
import ImagesViewer from "../../components/ImagesViewer.vue";
import ImagesDisplay from "../../components/ImagesDisplay.vue";
import ImagesTable from "../../components/ImagesTable.vue";

import axios from "axios";

const pdfUrl = ref("/pdfes/1.pdf"); // 初始显示 1.pdf

const imgUrl = ref("/images/Test.png");

const pdfList = ref(["1", "2", "3", "Test"]);

//测试图片
//const imagesList = ["1.jpg", "2.jpg", "3.jpg", "Test.png"];

//测试数据
const tableData = [
  { id: 1, name: "张三", description: "描述 1" },
  { id: 2, name: "李四", description: "描述 2" },
  { id: 3, name: "王五", description: "描述 3" },
];

const poses = ref([
  [632, 771, 105, 225],
  [760, 770, 43, 224],
  [476, 509, 122, 539],
  [10, 508, 456, 541],
  [614, 356, 224, 258],
  [554, 338, 30, 112],
  [506, 338, 28, 122],
  [381, 338, 105, 125],
  [134, 325, 106, 125],
  [302, 324, 32, 126],
  [10, 323, 106, 126],
  [254, 322, 31, 119],
  [214, 165, 63, 119],
  [295, 164, 61, 119],
  [420, 163, 26, 119],
  [372, 162, 28, 119],
  [6, 14, 202, 259],
  [485, 8, 27, 114],
  [435, 8, 33, 115],
  [221, 8, 96, 117],
  [539, 6, 309, 328],
  [329, 6, 93, 117],
]);

const imageTable = ref(["1", "化石"], ["2", "小远"]);
const imagesList = ref(["1.jpg", "2.jpg", "3.jpg"]); // 用于存储 tableImg

// 定义获取数据的方法(待调试)
const fetchData = async () => {
  try {
    // 请求体
    const requestData = {
      pdf_id: 0, // 示例请求参数
    };

    // 向后端发送 POST 请求
    const response = await axios.post('http://xxx/api/project/tableExtra', requestData);

    const data = response.data;

    // 处理 pos 数据
    poses.value = data.pos || [];

    // 构造 imageTable，格式为 [ [ocrs[i], child_fig[i]], ... ]
    const ocrs = data.ocrs || [];
    const childFig = data.child_fig || [];
    imageTable.value = ocrs.map((ocr, index) => [ocr, childFig[index]]);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// 在组件挂载时调用 fetchData
onMounted(fetchData);



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

  console.log("上一项"); // 打印选中的文件名
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
  console.log("Selected image in parent component:", selectedImage.value);
};

// 接收子组件保存时的数据
const handleUpdateTable = (data) => {
  console.log("从子组件接收到的表格数据：", data);
};
</script>

<style scoped>

.search-container {
  flex: 1;
  max-width: 400px;
  margin-left: auto;
  position: relative;
}

.search-container .icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

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

.pdf-select :deep(.el-input__wrapper) {
  padding-left: 40px;
  border-radius: 8px;
  background: #e8fafe; /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
}
</style>
