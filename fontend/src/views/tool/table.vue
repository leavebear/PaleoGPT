<template>
  <div class="elements">
    <el-form :inline="true" :model="formInline">
      <el-form-item  style="width: 100%; padding-top: 5px;padding-bottom: 20px; margin: 0;">
        <!-- 文件选择器 -->
        <!-- <div style="width: 4%;margin-top: 5px; margin-left: 10px;">
          <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32"><path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path></svg>
        </div> -->
        <div class="header">
          <span class="title">表格抽取
            <svg t="1742114718842" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4650" width="32" height="32"><path d="M508.3392 0h57.173333v1024h-57.173333zM1023.9232 512a44.544 44.544 0 0 0-44.8-44.8H638.301867v89.6h340.821333A44.544 44.544 0 0 0 1023.9232 512zM895.4112 32H748.893867c-24.917333 0-44.8 19.797333-44.8 44.8s19.797333 44.8 44.8 44.8h146.517333a39.253333 39.253333 0 0 1 38.997333 38.997333V307.2c0 24.917333 19.797333 44.8 44.8 44.8A44.629333 44.629333 0 0 0 1024.008533 307.2V160.682667c0-71.082667-57.6-128.682667-128.597333-128.682667zM979.208533 672.085333a44.544 44.544 0 0 0-44.8 44.8v146.517334c0 21.76-17.92 38.997333-38.997333 38.997333H748.893867c-24.917333 0-44.8 19.797333-44.8 44.8s19.797333 44.8 44.8 44.8h146.517333c70.997333 0 128.597333-57.6 128.597333-128.682667V716.8a44.544 44.544 0 0 0-44.8-44.714667z" fill="#407CD5" p-id="4651"></path><path d="M392.541867 179.797333a21.077333 21.077333 0 0 1 16.298666-6.741333h116.138667V32H114.184533C82.525867 32 55.645867 43.52 33.544533 65.621333a110.08 110.08 0 0 0-33.621333 80.64v731.477334c0 32.682667 11.52 58.538667 33.621333 80.64 22.101333 22.101333 48.981333 33.621333 80.64 33.621333h410.794667v-91.221333H408.840533a21.077333 21.077333 0 0 1-16.298666-6.741334c-3.84-2.901333-5.717333-9.557333-5.717334-16.298666V742.4c0-6.741333 1.962667-12.458667 5.717334-17.322667a24.064 24.064 0 0 1 16.298666-5.717333h116.138667V628.138667H408.840533a21.077333 21.077333 0 0 1-16.298666-6.741334 22.528 22.528 0 0 1-5.802667-16.298666V468.821333c0-6.741333 1.962667-11.52 5.717333-16.298666 4.778667-4.778667 9.557333-5.717333 16.298667-5.717334h116.138667v-91.306666h-116.053334a21.077333 21.077333 0 0 1-16.298666-6.741334 22.357333 22.357333 0 0 1-5.802667-16.298666V196.181333c0-6.741333 1.962667-11.52 5.802667-16.384z m-96.938667 697.941334c0 6.741333-1.962667 13.482667-5.717333 16.298666a23.210667 23.210667 0 0 1-17.237334 6.741334H114.184533c-6.741333 0-12.458667-1.962667-16.298666-6.741334-4.778667-2.901333-6.741333-9.557333-6.741334-16.298666V742.4a23.04 23.04 0 0 1 6.741334-17.322667 22.442667 22.442667 0 0 1 16.298666-5.717333h158.378667c6.741333 0 12.458667 1.962667 17.237333 5.717333a27.050667 27.050667 0 0 1 5.802667 17.322667v135.338667z m0-272.64a22.869333 22.869333 0 0 1-5.717333 16.298666 23.210667 23.210667 0 0 1-17.322667 6.741334H114.184533c-6.741333 0-12.458667-1.962667-16.298666-6.741334-4.864-3.84-6.741333-9.557333-6.741334-16.298666V468.821333c0-6.741333 1.877333-11.52 6.741334-16.298666 3.84-4.778667 9.642667-5.717333 16.298666-5.717334h158.378667c6.741333 0 12.458667 1.962667 17.237333 5.717334a24.064 24.064 0 0 1 5.717334 16.298666v136.277334z m0-272.64a22.869333 22.869333 0 0 1-5.717333 16.298666 23.210667 23.210667 0 0 1-17.322667 6.741334H114.184533c-6.741333 0-12.458667-1.962667-16.298666-6.741334-4.864-3.754667-6.741333-9.557333-6.741334-16.298666V196.181333c0-6.741333 1.877333-11.52 6.741334-16.298666 3.84-4.778667 9.642667-6.741333 16.298666-6.741334h158.378667a23.04 23.04 0 0 1 17.237333 6.741334 24.149333 24.149333 0 0 1 5.802667 16.298666v136.277334z" fill="#407CD5" p-id="4652"></path></svg>
          </span>
          <div class="search-container">
        <el-select
          v-model="selectedPdf"
          @change="handlePdfChange"
          placeholder="文件选择"
          class="pdf-select"
          :options="pdfList"
          size="large"
          style="width:80%;"
        >
        <template #prefix>
        <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32">
          <path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path>
        </svg>
        </template>
          <el-option
            v-for="pdf in pdfList"
            :key="pdf"
            :label="pdf"
            :value="pdf"
          />
        </el-select>
      </div>
    </div>
    <el-button 
        type="primary" 
        round
        plain
        @click="LastItem" 
        style="margin-left: 20px; height: 40px;  width: 6%;"
        >
          上一项
        </el-button>
        <el-button 
        type="primary" 
        round
        plain
        @click="NextItem"
        style="height: 40px; width: 6%;"
        >
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
      <el-form-item style="margin: 0; padding: 0; margin-right: 20px">
        <div class="pdf-content" style="width: 100%;" v-show="isPdfVisible">
          <PdfViewer  
            :pdf-url="pdfUrl" 
            ref="pdfViewRef"  
          />
        </div>
      </el-form-item>

      <el-form-item style="flex: 1; display: flex; flex-direction: column; margin: 0;">
        <el-col style="display: flex; flex-direction: column; width: 100%; height: 100%;">
          <!-- 上方静态文本 -->
          <el-row
            style="
              background: #f5f7fa;
              text-align: left;
              font-size: 16px;
              font-weight: bold;
              white-space: nowrap;
            "
          >
            <span>表格选择：</span>
          </el-row>
          <!-- 中间的横向图片列表 -->
          <el-row style="background: #f5f7fa ;padding: 10px 0;">
            <div>
              <ImagesViewer
                :images="imagesList"
                @image-clicked="handleImageClick"
              />
            </div>
          </el-row>
          <!-- 下方的大表格 -->
          <el-row style="background: #f5f7fa">
            <!-- 操作按钮 -->
            <el-col style="margin-bottom: 10px">
              <el-button
              type="primary" 
              plain
              size="small" 
              @click="updateTableData"
              style="height: 40px;  width: 10%;"
                >改变表格</el-button
              >
            </el-col>

            <!-- 表格  handleSaveTable是保存表格数据的函数 -->
            <PdfTable
              :initialData="tableData"
              :pdfName="selectedPdf"
  :tableIndex="chosenTable"
  @save-table="handleSaveTable"
  ref="tableRef"
  style="width: 100%; height: 100%;"
            />
          </el-row>
        </el-col>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, watch ,onMounted} from "vue";
import PdfViewer from "../../components/PdfViewer.vue";
import ImagesViewer from "../../components/ImagesViewer.vue";
import PdfTable from "../../components/PdfTable.vue";
import globalState from '../../globalState.js';
 
import axios from "axios"



const pdfUrl = ref("/pdfes/1.pdf"); // 初始显示 1.pdf

const pdfList = ref(["1", "01zjcTest", "3"]);

const radio1 = ref("1");

const tableRef = ref(null); // 使用 Vue 的 ref 来定义 tableRef
const pdfViewRef = ref(null); // 使用 Vue 的 ref 来定义 pdfViewRef

//测试图片
//const imagesList = ["1.jpg", "2.jpg", "3.jpg"];

// 默认的表格尺寸 [行数, 列数]
const tableData = ref([
  ['Isolation source', 'Oil- contaminated', '(Waste water)', '(Fresh water)'],
  ['Growth at 45°C', 'soil +', '+', '-'],
  ['pH range', '5.59.0', '5.08.0', '5.510.0'],
  ['Highest salt tolerance (%, w/v)', '1.0', '4.0', '6.0'],
  ['Hydrolysis of', '', '', ''],
  ['Casein', '-', '-', '+'],
  ['Tyrosine', 'W', 'w', '+'],
  ['Aesculin', 'W', '-', '-'],
  ['Gelatin', 'W', '+', '-'],
  ['Enzyme activity (API ZYM)', '', '', ''],
  ['Alkaline phosphatase', 'W', '+', 'w'],
  ['Lipase (C 14)', '-', '+', '+'],
  ['Cystine arylamidase', 'w', '-', '-'],
  ['Trypsin', 'W', '-', 'w'],
  ['α-Chymotrypsin', '+', '-', '+'],
  ['Acid phosphatase', '-', '-', '一'],
  ['Napthol-AS-BI- phosphohydrolase', '-', '-', '-'],
  ['Assimilation from (API 20NE and API ID 32', '', '', ''],
  ['GN) Maltose', '-', '-', '+'],
  ['Sucrose', '-', '-', '-'],
  ['L-Histidine', '+', '-', '-'],
  ['L-Proline', '+', '-', '-'],
  ['DNA G+C content (mol%)', '37.2', '(32.3)', '(38.6)']
]);


const chosenTable=ref();

// 响应数据的存储变量
const imagesList = ref(); // 用于存储 tableImg
const tableList = ref(); // 用于存储 table



// 定义POST请求接口的函数
const fetchTableData = async (pdfId) => {
  try {
    const requestData = {
      pdf_id: "a", // 请求体
    };

    // 发送 POST 请求
    const response = await axios.post("http://localhost:8000/api/project/tableExtra", requestData);

     // 获取返回的数据
    const data = response.data.data;

     // 设置 pdfUrl
    // pdfUrl.value = data.pdfDownloadUrl;
    // console.log("pdfUrl.value:",pdfUrl.value);  // "a"

    // pdfViewRef.value.changePdf(pdfUrl.value); // 调用子组件暴露的方法

    // 清空现有的数据
    imagesList.value = [];
    tableList.value = [];

    // 遍历 tableList，将数据分别存储到 imagesList 和 tableList
    data.tableList.forEach(item => {
      imagesList.value.push(item.tableImg);
      tableList.value.push(item.table);
    });

    console.log("imagesList:",imagesList.value);  // "a"


    } catch (error) {
      console.error('请求失败:', error);
    }
};

// 监听保存事件
const handleSaveTable = (savedData) => {
  console.log("保存的表格数据:", savedData);
  console.log("该表格对应的图片url为:", imagesList.value[chosenTable.value]);

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


//发送POST请求(1)
// 监听文件选择变化
const handlePdfChange = (selectedFileName) => {
  // 这里生成对应的 PDF URL
  const pdfPath = `pdfes/${selectedFileName}.pdf`; // 这里的路径应与你的文件存放路径一致
  pdfUrl.value = pdfPath;
  pdfViewRef.value.changePdf("/src/assets/01zjcTest.pdf");
  // 访问全局状态
  //console.log(globalState.pdf_id);  // "a"
  //console.log(globalState.pdf_ids_list);  // []
  //发送POST请求(pdf_id)
  fetchTableData("a");



  // 更新 pdfUrl
  //pdfUrl.value = pdfPath;
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

//发送POST请求(2)
//图片列表点击事件
const selectedImage = ref("");
onMounted(() => {
  // 页面加载时自动选择第二个文件
  if (pdfList.value.length > 1) {
    selectedPdf.value = pdfList.value[1]; // 选择第二个文件
    handlePdfChange(selectedPdf.value); // 触发文件选择逻辑
  }
});


const handleImageClick = (imageName) => {
  selectedImage.value = imageName;
  console.log("Selected image in parent component:", imageName);
// 遍历 imagesList
  for (let i = 0; i < imagesList.value.length; i++) {
    // 如果找到了匹配的图像名称
    if (imagesList.value[i] === imageName) {
      // 获取对应的 table 数据
      //tableData = tableList.value[i];
      chosenTable.value=i;
      console.log("updateTableData:", tableList.value[chosenTable.value]);
      tableRef.value.updateTableData(tableList.value[chosenTable.value]); // 调用子组件暴露的 updateTableData 方法
      break; // 跳出循环
    }
  }
};


//初始化页面
// 初始化表格数据



</script>

<style scoped>
.elements {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  gap: 140px;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 8px;
}
.icon {
  width: 32px; /* 图标的宽度 */
  height: 32px; /* 图标的高度 */
  fill: currentColor; /* 图标颜色 */
}

.search-container {
  flex: 1;
  max-width: 500px;
  margin-left: auto;
  position: relative;
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

.pdf-select:deep(.el-select__wrapper){
  width: 500px; /* 设置选择器的宽度 */
  border-radius: 8px;
  background: #e8fafe; /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
  height: 20px; /* 设置选择框的高度 */
  line-height: 20px; /* 保持文字垂直居中 */
  padding: 0 10px; /* 调整左右内边距 */
}

.pdf-select .el-select__prefix {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px; /* 根据需要调整间距 */
}

/* 调整内部输入框的样式 */
.pdf-select .el-input__inner {
  height: 20px; /* 确保内部输入框高度一致 */
  line-height: 20px;
  border-radius: 4px; /* 可选：调整圆角 */
}

/* 响应式优化 */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-container {
    width: 100%;
    max-width: none;
  }
}
</style>
