<template>
  <div class="elements">
    <el-form :inline="true" :model="formInline">
      <el-form-item style="width: 100%; padding-top: 5px;padding-bottom: 20px; margin: 0;">
        <!-- <div style="width: 3.5%;margin-top: 6px; margin-left: 10px;">
          <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32"><path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path></svg>
        </div> -->
        <!-- 文件选择器 -->
        <div class="header">
          <span class="title">图片抽取
            <svg t="1742107488367" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
              p-id="7921" width="32" height="32">
              <path
                d="M977 961V273M422.9 587.5V55H51.3v899.1h0.1v4.9h912.1V587.5H422.9zM843.5 839H171.4v-4.9h-0.1V175h131.5v532.5h540.6V839z"
                fill="#487FFF" p-id="7922"></path>
              <path d="M526 56.3h434.2v432.6H526z" fill="#487FFF" p-id="7923"></path>
            </svg>
          </span>
          <div class="search-container">
            <el-select v-model="selectedPdf" @change="handlePdfChange" placeholder="请选择PDF文件" class="pdf-select"
              :options="pdfList" size="large" style="width:80%;">
              <template #prefix>
                <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1"
                  xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32">
                  <path
                    d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z"
                    fill="#1296db" p-id="2297"></path>
                </svg>
              </template>
              <el-option v-for="pdf in pdfList" :key="pdf" :label="pdf" :value="pdf" />
            </el-select>
          </div>
        </div>
        <el-button type="primary" round plain @click="LastItem" style="margin-left: 20px; height: 40px;  width: 6%;">
          上一项
        </el-button>
        <el-button type="primary" round plain @click="NextItem" style="height: 40px; width: 6%;">
          下一项
        </el-button>
      </el-form-item>
      <!--上下按钮
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
      -->
    </el-form>

    <el-form :inline="true" :model="formInline" style="display: flex; gap: 10px; align-items: flex-start">
      <el-form-item style="margin: 0; padding: 0">
        <!-- 按钮 -->
        <el-button type="primary" size="small" style="margin-top: 0; z-index: 100" @click="pdfVisible">
          {{ buttonText }}
        </el-button>
      </el-form-item>
      <el-form-item style="margin: 0; padding: 0; margin-right: 20px; ">
        <div class="pdf-content" style="width: 100%;" v-show="isPdfVisible">
          <PdfViewer :pdf-url="pdfUrl" ref="pdfViewRef" />
        </div>
      </el-form-item>

      <el-form-item style="flex: 1; display: flex; flex-direction: column; margin: 0;">
        <el-row style="flex: 1; display: flex; flex-direction: column; height: 100%">
          <!-- 上方静态文本 -->
          <el-col style="
              background: #f5f7fa;
              text-align: left;
              font-size: 16px;
              font-weight: bold;
              padding: 10px ;
            ">
            <span>大图列表：</span>
          </el-col>

          <!-- 中间的横向图片列表 -->
          <el-col style="background: #f5f7fa; flex: 1; padding: 10px;">
            <div>
              <!-- 大图列表组件 -->
              <ImagesViewer :images="imagesList" @image-clicked="handleImageClick" />
            </div>
          </el-col>
          <!-- 下方的子图片显示 -->
          <el-col style="background: #f5f7fa; flex: 1; padding: 10px;">
            <!-- 小图组件占位 -->
            <div>
              <!-- 小图列表组件 -->
              <ImagesDisplay :url="selectedImage" :pos="poses[selectedImageIndex]" @ChosenOne="handleSingleClick"
                @DblClick="handleDoubleClick" />
            </div>
          </el-col>

          <!-- 小图信息展示 -->
          <el-col style="
          /* background: #f5f7fa;  */
          flex: 1; 
          margin-top: 15px;">
            <ImagesTable 
            :initialFigure="imageTable[selectedImageIndex][selectedRegin].ocr" 
            :initialName="imageTable[selectedImageIndex][selectedRegin].child_fig"
            :initialWidth="imageTable[selectedImageIndex][selectedRegin].width" 
            :initialHeight="imageTable[selectedImageIndex][selectedRegin].height"
            :initialScale="imageTable[selectedImageIndex][selectedRegin].scale" 
            :savedScales="savedScales" 
            :currentRect="poses[selectedImageIndex][selectedRegin]"
            :initialSelectedScale="selectedScale" @update:selectedScale="selectedScale = $event"
              @updateData="SaveRegininfo" ref="ImagesTableRef" />
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
    <el-dialog v-model="dialogVisible" width="90%" class="custom-dialog">
      <div class="dialog-content">
        <div class="dialog-container">
          <!-- 左半部分 - 大图和测量工具 -->
          <div class="left-section">
            <div class="image-title">大图
              <el-button @click="toggleMagnifier" :type="isMagnifierActive ? 'success' : 'danger'" size="small"
                style="margin-left: 10px;">
                {{ isMagnifierActive ? '放大镜(开)' : '放大镜(关)' }}
              </el-button>
            </div>
            <div class="large-image" @click="handleImageClickForMeasurement" @mousemove="handleMouseMove"
              @mouseover="changeCursor" @mouseleave="resetMouseMove" ref="imageContainer">
              <img :src="selectedImage" alt="大图" ref="largeImageRef"
                style="max-width: none; width: auto; height: auto;" />
              <canvas ref="canvasRef" class="measure-canvas"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"></canvas>
              <!-- 放大镜效果 -->
              <div v-if="isMagnifierActive && isHoverZoomed" class="magnifier" :style="{
                left: `${magnifierPosition.x}px`,
                top: `${magnifierPosition.y}px`,
                width: `${zoomWindowSize}px`,
                height: `${zoomWindowSize}px`
              }">
                <canvas ref="zoomCanvasRef"></canvas>
              </div>
            </div>
            <div class="input-container">
              <div class="input-group">
                <label>像素长度：</label>
                <el-input v-model="pixelLength" placeholder="请输入像素长度" style="margin-left: 10px;" disabled></el-input>
                <span style="margin-left: 10px;">pixel</span>
              </div>
              <div class="input-group">
                <label>实际长度：</label>
                <el-input v-model="actualLength" placeholder="请输入实际长度" style="margin-left: 10px;"></el-input>
                <el-select v-model="lengthUnit" placeholder="选择单位" style="margin-left: 10px; width: 100px;">
                  <el-option label="cm" value="cm" />
                  <el-option label="mm" value="mm" />
                  <el-option label="m" value="m" />
                  <el-option label="inch" value="inch" />
                </el-select>
                <el-button type="primary" @click="saveScaleWithPrompt" style="margin-left: 10px;"
                  :disabled="!actualLength || !pixelLength">
                  保存比例尺
                </el-button>
                <el-button type="danger" @click="showDeleteDialog = true" style="margin-left: 10px;"
                  :disabled="savedScales.length === 0">
                  删除比例尺
                </el-button>

              </div>
            </div>
          </div>

          <!-- 右半部分 - 小图和计算结果 -->
          <div class="right-section">
            <div class="right-content-wrapper">
              <div class="right-content">
                <div class="image-title">小图</div>
                <div class="small-image">
                  <img :src="selectedImage1" alt="小图" v-if="selectedImage1" />
                  <div v-else style="color: red; font-size: 14px;">加载失败，请检查图片路径或网络连接</div>
                </div>
                <div class="result-container">
                  <!-- 新增化石名称输入框 -->
                  <div class="input-group">
                    <label>化石名称：</label>
                    <el-input v-model="fossilName" placeholder="化石名称" style="margin-left: 10px; width: 400px"
                      disabled />
                  </div>
                  <div class="input-group">
                    <label>选择比例尺：</label>
                    <el-select v-model="selectedScale" placeholder="选择标尺" style="margin-left: 10px; width: 120px;"
                      @change="loadScale">
                      <el-option v-for="(scale, index) in savedScales" :key="index" :label="scale.name"
                        :value="index" />
                    </el-select>
                  </div>
                  <div class="input-group">
                    <label>化石长度：</label>
                    <el-input v-model="fossilLength" placeholder="请输入化石长度" style="margin-left: 10px;"
                      disabled></el-input>
                    <el-select v-model="fossilLengthUnit" placeholder="选择单位" style="margin-left: 10px; width: 100px;">
                      <el-option label="cm" value="cm" />
                      <el-option label="mm" value="mm" />
                      <el-option label="m" value="m" />
                      <el-option label="inch" value="inch" />
                    </el-select>
                  </div>
                  <div class="input-group">
                    <label>化石宽度：</label>
                    <el-input v-model="fossilWidth" placeholder="请输入化石宽度" style="margin-left: 10px;"
                      disabled></el-input>
                    <el-select v-model="fossilWidthUnit" placeholder="选择单位" style="margin-left: 10px; width: 100px;">
                      <el-option label="cm" value="cm" />
                      <el-option label="mm" value="mm" />
                      <el-option label="m" value="m" />
                      <el-option label="inch" value="inch" />
                    </el-select>
                  </div>
                  <el-button type="primary" @click="openApplyToFossilsDialog" style="margin-left: 10px;"
                    :disabled="!selectedScale && savedScales.length === 0">
                    应用该标尺到部分化石
                  </el-button>

                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button plain type="success" style="margin-right: 20px;" @click="applyChanges">应用</el-button>
          <el-button plain type="danger" @click="dialogVisible = false">退出</el-button>
        </div>
      </template>
    </el-dialog>
    <!-- 删除存档的对话框 -->
    <el-dialog v-model="showDeleteDialog" title="删除存档" width="30%">
      <div>
        <p>请选择要删除的存档：</p>
        <el-select v-model="scaleToDelete" placeholder="选择存档" style="width: 100%;">
          <el-option v-for="(scale, index) in savedScales" :key="index" :label="scale.name" :value="index" />
        </el-select>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteDialog = false">取消</el-button>
          <el-button type="danger" @click="deleteScale" :disabled="scaleToDelete === null">确定</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 添加新的弹窗 -->
    <el-dialog v-model="applyToFossilsDialogVisible" title="应用标尺到部分化石" width="50%">
      <div>
        <div style="display: flex; gap: 20px;">
          <!-- 大图显示 -->
          <div style="flex: 1;">
            <div class="image-title">大图</div>
            <img :src="largeImageForDialog" alt="大图" style="width: 100%; height: auto;" v-if="largeImageForDialog" />
          </div>

          <!-- 小图选择 -->
          <div style="flex: 1;">
            <p>请选择要应用当前标尺的小图：</p>
            <el-checkbox-group v-model="selectedFossils">
              <el-checkbox v-for="option in allFossilOptions" :key="option.value" :label="option.value"
                style="display: block; margin: 5px 0;">
                {{ option.label }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="applyToFossilsDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="applyScaleToSelectedFossils" :disabled="selectedFossils.length === 0">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from "vue";
import PdfViewer from "../../components/PdfViewer.vue";
import ImagesViewer from "../../components/ImagesViewer.vue";
import ImagesDisplay from "../../components/ImagesDisplay.vue";
import ImagesTable from "../../components/ImagesTable.vue";

import axios from "axios";

import { countdownEmits, ElMessage, ElMessageBox } from 'element-plus';

import { getImageExtraDataService, updateImageExtraDataService } from '../../api/picture.js';

const pdfUrl = ref("pdfes/DX-2018-JP-Ammonoid.pdf"); // 初始显示 1.pdf

const imagesList = ref(["1.jpg", "2.jpg"]); // 用于存储 tableImg

const pdfList = ref(["1", "DX-2018-JP-Ammonoid", "3", "Test"]);

//小图矩形框
const poses = ref([
  [
    [632, 771, 105, 225],
    [760, 770, 43, 224],
    [476, 509, 122, 539],
    [10, 508, 456, 541],
  ],
  [
    [614, 356, 224, 258],
    [554, 338, 30, 112],
    [506, 338, 28, 122],
  ]
]);

const imageTable = ref([
  [
    {
      ocr: "1",
      child_fig: "化石",
      width: { value: 5, unit: "cm" },
      height: { value: 3, unit: "cm" },
      scale: { value: 1, unit: null }
    },
    {
      ocr: "2",
      child_fig: "小远",
      width: { value: null, unit: null },
      height: { value: null, unit: null },
      scale: { value: null, unit: null }
    }
  ],
  [
    {
      ocr: "1",
      child_fig: "化石",
      width: { value: 5, unit: "cm" },
      height: { value: 3, unit: "cm" },
      scale: { value: 1, unit: null }
    },
    {
      ocr: "2",
      child_fig: "小远",
      width: { value: null, unit: null },
      height: { value: null, unit: null },
      scale: { value: null, unit: null }
    }
  ]
]);




// 定义长度单位
const largeImageRef = ref(null); // 大图的引用
const canvasRef = ref(null); // 画布的引用
const points = ref([]); // 存储用户点击的点的坐标
const pixelLength = ref(""); // 像素长度
const actualLength = ref(""); // 实际长度
const lengthUnit = ref("cm"); // 长度单位
const scale = ref(null); // 比例
const fossilLength = ref(""); // 化石长度
const fossilWidth = ref(""); // 化石宽度
const fossilLengthUnit = ref("cm"); // 化石长度单位
const fossilWidthUnit = ref("cm"); // 化石宽度单位

// 新增变量
const isDrawing = ref(false); // 是否正在绘制线段
const tempPoint = ref(null); // 临时存储鼠标移动时的点

const savedScales = ref([]); // 存储所有存档的比例
const selectedScale = ref(null); // 当前选中的存档索引
const showDeleteDialog = ref(false); // 控制删除对话框显示
const scaleToDelete = ref(null); // 要删除的存档索引
// 新增一个响应式变量来跟踪是否首次加载
const isInitialLoad = ref(true);

const fossilName = ref(""); // 选中小图化石名称

// 放大镜相关变量
const isMagnifierActive = ref(false); // 是否启用放大镜
const magnifierPosition = ref({ x: 0, y: 0 }); // 放大镜位置
const imageContainer = ref(null); // 图片容器引用

const hoverTimer = ref(null); // 悬停计时器
const hoverTimeout = 1000; // 悬停触发时间(毫秒)
const isHoverZoomed = ref(false); // 是否处于悬停放大状态
const zoomLevel = ref(2); // 放大倍数
const zoomWindowSize = ref(200); // 放大窗口大小(像素)
const mousePosition = ref({ x: 0, y: 0 }); // 鼠标位置
const zoomCanvasRef = ref(null); // 放大镜画布引用

// 新状态
const applyToFossilsDialogVisible = ref(false); // 控制应用标尺弹窗的显示
const selectedFossils = ref([]); // 存储用户选择的小图索引
const allFossilOptions = ref([]); // 所有小图的选项

const largeImageForDialog = ref(""); // 用于存储弹窗中右半部分的大图




const pdfViewRef = ref(null); // 使用 Vue 的 ref 来定义 pdfViewRef

const ImagesTableRef = ref(null); // 存储的是选中的小图的信息，具体结构如下
// {
//   ocr: "1",
//   child_fig: "化石",
//   width: { value: 5, unit: "cm" },
//   height: { value: 3, unit: "cm" },
//   scale: { value: 1, unit: null }
// }

// POST请求  获取数据的方法(待调试)
const fetchData = async () => {
  try {
    // 向后端发送 POST 请求
    const response = await getImageExtraDataService(selectedPdf.value);
    const data = response.data;

    console.log("data:", data);

    // 清空旧数据
    poses.value = [];
    savedScales.value = [];
    imagesList.value = [];
    imageTable.value = [];

    // 更新新数据
    imagesList.value = data.image_list || [];

    const figDataList = data.fig_data || [];

    for (let imgIndex = 0; imgIndex < figDataList.length; imgIndex++) {
      const fig = figDataList[imgIndex];
      console.log(fig);

      const child_figs = fig.child_fig || [];
      const ocrs = fig.ocrs || [];
      const widths = fig.width || { value: null, unit: null };
      const heights = fig.height || { value: null, unit: null };
      const scales = fig.scale || { value: null, unit: null };

      poses.value.push(fig.pos || []);
      console.log(poses.value)

      const tablePerImage = [];
      for (let i = 0; i < child_figs.length; i++) {
        const scale = scales[i] || { value: null, unit: null };
        addScaleIfUnique(scale);

        tablePerImage.push({
          ocr: ocrs[i] || "",
          child_fig: child_figs[i] || "",
          width: widths[i] || "",
          height: heights[i] || "",
          scale: scale
        });
      }
      console.log("tablePerImage:",tablePerImage)

      imageTable.value.push(tablePerImage);
    }

    console.log("savedScales:", savedScales.value);
    console.log("imagesList:", imagesList.value);
    console.log("imageTable:", imageTable.value);

  } catch (error) {
    console.error('Error fetching data:', error);
  }

};

// 将获取到的数据中的比例尺存在前端
const addScaleIfUnique = (scale) => {
  if (!scale || scale.value == null || scale.unit == null) return; // 排除无效比例尺

  const isDuplicate = savedScales.value.some(savedScale =>
    savedScale.value === scale.value && savedScale.unit === scale.unit
  );

  if (!isDuplicate) {
    savedScales.value.push(scale);
  }
}


// 选择的 PDF 文件名
const selectedPdf = ref("");
const selectedRegin = ref(0);

const isPdfVisible = ref(true); // 控制 PDF 容器显示状态
const buttonText = ref("-"); // 按钮上的文本

// 切换 PDF 显示状态的方法
const pdfVisible = () => {
  isPdfVisible.value = !isPdfVisible.value; // 切换显示状态
  buttonText.value = isPdfVisible.value ? "-" : "+"; // 动态更新按钮文本
};

//接口调试（1）
// 监听文件选择变化
const handlePdfChange = (selectedFileName) => {
  const pdfPath = `pdfes/${selectedFileName}.pdf`; // 假设 PDF 文件存储在 /pdfes 文件夹中
  console.log("11111pdfPath:", pdfPath); // 输出 PDF 文件的路径
  pdfUrl.value = pdfPath; // 更新 pdfUrl
  // pdfViewRef.value.changePdf(pdfUrl.value); // 调用子组件的方法更新 PDF 阅读器
  pdfViewRef.value.changePdf("/src/assets/DX-2018-JP-Ammonoid.pdf");
  console.log(pdfUrl.value)
  // 这里生成对应的 PDF URL
  //const pdfPath = `/pdfes/${selectedFileName}.pdf`; // 这里的路径应与你的文件存放路径一致
  //发送POST请求
  fetchData()
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
const dialogVisible = ref(false);
// 定义 selectedImage 和 selectedImage1 为响应式引用
const selectedImage = ref("/images/Test.png");  //选中大图的url
const selectedImageIndex = ref(0)  //选中大图的索引
const selectedImage1 = ref("");





// 选中大图后，更改selectedImage的值和selectedImageIndex的值
const handleImageClick = (imageName) => {
  selectedImage.value = imageName; //url
  console.log(selectedImage.value);


  // 遍历 imagesList
  for (let i = 0; i < imagesList.value.length; i++) {
    // 如果找到了匹配的图像名称
    if (imagesList.value[i] === imageName) {
      console.log("你点击了图片列表中的图片:", i);
      selectedImageIndex.value = i; //index
      break; // 跳出循环
    }
  }
  console.log(selectedImageIndex.value);


};

// 选中小图，单击事件处理函数
const handleSingleClick = (chosenID) => {
  console.log("单击选中的框索引:", chosenID);
  // 更新操作面板的内容
  selectedRegin.value = chosenID; // 更新选中的区域索引
  const rect = poses.value[selectedImageIndex.value][chosenID];
  const fullImagePath = selectedImage.value; // 使用完整的 URL
  cropImageToDataUrl(fullImagePath, rect); // 裁剪并更新小图
  if (ImagesTableRef.value) {
    const selectedItem = imageTable.value[selectedImageIndex][chosenID];

    ImagesTableRef.value.setTableData(
      selectedItem.ocr,
      selectedItem.child_fig,
      selectedItem.width?.value,
      selectedItem.height?.value,
      selectedItem.width?.unit || "cm",
      selectedItem.height?.unit || "cm"
    );

  }
};


// 选中小图，双击事件处理函数
const handleDoubleClick = (chosenID) => {
  console.log("双击选中的框索引:", chosenID);
  // 弹出弹窗
  dialogVisible.value = true; // 显示弹窗
  selectedRegin.value = chosenID; // 更新选中的区域索引
  const rect = poses.value[selectedImageIndex.value][chosenID];
  const fullImagePath = selectedImage.value; // 使用完整的 URL
  cropImageToDataUrl(fullImagePath, rect); // 裁剪并更新小图

  const selectedItem = imageTable.value[selectedImageIndex.value][chosenID];

  if (selectedItem) {
    fossilName.value = selectedItem.child_fig;

    ImagesTableRef.value.setTableData(
      selectedItem.ocr,          // OCR 结果
      selectedItem.child_fig,    // 化石名称
      selectedItem.width?.value, // 宽度（值）
      selectedItem.height?.value, // 高度（值）
      selectedItem.width?.unit || "cm",  // 宽度单位，默认 "cm"
      selectedItem.height?.unit || "cm", // 高度单位，默认 "cm"

    );
  }
};

// 从大图中根据pos切割小图
const cropImageToDataUrl = (imageUrl, rect) => {
  const img = new Image();
  img.crossOrigin = 'Anonymous'; // 设置跨域属性
  img.onload = () => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = rect[2];
    canvas.height = rect[3];
    //ctx.drawImage(img, -rect[0], -rect[1], rect[2], rect[3]);
    ctx.drawImage(
      img,
      rect[0],        // 源X坐标
      rect[1],        // 源Y坐标
      rect[2],        // 源宽度
      rect[3],        // 源高度
      0,              // 目标X坐标
      0,              // 目标Y坐标
      rect[2],        // 目标宽度
      rect[3]         // 目标高度
    );
    selectedImage1.value = canvas.toDataURL('image/png'); // 将截取的小图设置为弹窗中的小图
    console.log('Cropped image data URL:', selectedImage1.value);
  };
  img.onerror = () => {
    console.error('Failed to load image:', imageUrl);
    selectedImage1.value = ''; // 清空无效的图片路径
  };
  img.src = imageUrl;
};


// 接收子组件保存时的数据
const SaveRegininfo = async (data) => {
  console.log("更新前 imageTable:", imageTable.value);

  const outerIndex = selectedImageIndex.value;
  const innerIndex = selectedRegin.value;


  // 获取当前大图的子图列表
  const currentImageTables = [...imageTable.value[outerIndex]];

  // 更新当前子图信息
  currentImageTables[innerIndex] = {
    ...currentImageTables[innerIndex],  // 保留原有数据
    ocr: data.figure,      // 更新 ocr
    child_fig: data.name,  // 更新 name
    width: { value: data.width.value, unit: data.width.unit }, // 更新宽度（值 + 单位）
    height: { value: data.height.value, unit: data.height.unit }, // 更新高度（值 + 单位）
    scale: { value: data.scale?.value || null, unit: data.scale?.unit || null } // 更新缩放（值 + 单位）
  };

  imageTable.value[outerIndex] = currentImageTables;

  console.log("更新后 imageTable:", imageTable.value);

  // 更新全局数据后 更新后端数据
  try {
    const update_fig_data = imageTable.value.map((tableRow, rowIndex) => {
      const child_fig = []
      const ocrs = []
      const width = []
      const height = []
      const scale = []
      const pos = []

      tableRow.forEach((item, colIndex) => {
        child_fig.push(item.child_fig)
        ocrs.push(item.ocr)
        width.push({
          value: item.width?.value ?? null,
          unit: item.width?.unit ?? null
        })
        height.push({
          value: item.height?.value ?? null,
          unit: item.height?.unit ?? null
        })
        scale.push({
          value: item.scale?.value ?? null,
          unit: item.scale?.unit ?? null
        })
        pos.push(poses.value?.[rowIndex]?.[colIndex] ?? [0, 0, 0, 0])
      })

      return {
        child_fig,
        ocrs,
        pos,
        width,
        height,
        scale
      }
    })


    console.log("update_fig_data:", update_fig_data);

    const response = await updateImageExtraDataService(
      {
        pdf_id: "123",
        pdf_url: pdfUrl.value,
        image_list: imagesList.value,
        fig_data: update_fig_data
      }
    );

    if (response.status === 200) {
      console.log('后端数据更新成功:', response.data);
      // 在这里可以处理后端返回的数据，例如更新前端视图等
    }
  } catch (error) {
    console.error('更新后端数据失败:', error);
    // 可以显示错误提示，或其他操作
  }

};


// 新方法 - 打开应用标尺弹窗
const openApplyToFossilsDialog = () => {
  if (!selectedScale.value && savedScales.value.length === 0) {
    ElMessage.warning('请先选择或创建标尺');
    return;
  }

  // 设置弹窗中右半部分的大图路径
  largeImageForDialog.value = selectedImage.value; // 假设 selectedImage 是当前选中的大图路径

  // 生成选项并按照序号排序
  allFossilOptions.value = imageTable.value
    .map((item, index) => ({
      value: index,
      label: `小图 (${item.ocr} - ${item.child_fig})`,
      // 提取序号用于排序
      number: parseInt(item.ocr) || 0 // 假设item[0]是序号字符串
    }))
    .sort((a, b) => a.number - b.number); // 按序号升序排序

  applyToFossilsDialogVisible.value = true;
};


// 新方法 - 应用标尺到选中的小图
const applyScaleToSelectedFossils = () => {
  if (selectedScale.value === null || selectedFossils.value.length === 0) return;

  const currentScale = savedScales.value[selectedScale.value];
  const outerIndex = selectedImageIndex.value;
  const posesList = poses.value[outerIndex];
  const imageTables = [...imageTable.value[outerIndex]];

  // 计算每个选中小图的尺寸
  selectedFossils.value.forEach(index => {
    const rect = posesList[index];
    const item = imageTables[index];
    if (!rect || !item) return;

    const widthPixels = rect[2];
    const heightPixels = rect[3];

    // 转换为厘米
    let actualLengthInCm = parseFloat(currentScale.actualLength);
    if (currentScale.unit === 'mm') {
      actualLengthInCm = actualLengthInCm / 10;
    } else if (currentScale.unit === 'm') {
      actualLengthInCm = actualLengthInCm * 100;
    } else if (currentScale.unit === 'inch') {
      actualLengthInCm = actualLengthInCm * 2.54;
    }

    // 计算比例
    const scaleValue = parseFloat(currentScale.pixelLength) / actualLengthInCm;

    // 计算化石尺寸（厘米）
    const fossilLengthCm = heightPixels / scaleValue;
    const fossilWidthCm = widthPixels / scaleValue;

    // 转换为当前选择的单位
    let lengthConversion = 1;
    let widthConversion = 1;

    switch (fossilLengthUnit.value) {
      case 'mm': lengthConversion = 10; break;
      case 'm': lengthConversion = 0.01; break;
      case 'inch': lengthConversion = 0.393701; break;
    }

    switch (fossilWidthUnit.value) {
      case 'mm': widthConversion = 10; break;
      case 'm': widthConversion = 0.01; break;
      case 'inch': widthConversion = 0.393701; break;
    }

    // 更新表格数据
    item.width = { value: (fossilWidthCm * widthConversion).toFixed(2), unit: fossilWidthUnit.value };
    item.height = { value: (fossilLengthCm * lengthConversion).toFixed(2), unit: fossilLengthUnit.value };


    // 如果当前选中的区域是被修改的区域，更新操作面板
    if (selectedRegin.value === index && ImagesTableRef.value) {
      ImagesTableRef.value.setTableData(
        item.ocr,
        item.child_fig,
        item.width.value,
        item.height.value,
        item.width.unit,
        item.height.unit
      );
    }
  });

  ElMessage.success(`已成功应用标尺到 ${selectedFossils.value.length} 个小图`);
  applyToFossilsDialogVisible.value = false;
  selectedFossils.value = []; // 清空选择
};

const applyChanges = () => {
  // 关闭弹窗
  dialogVisible.value = false;

  // 如果 ImagesTableRef 存在且有化石长度和宽度数据
  if (ImagesTableRef.value && fossilLength.value && fossilWidth.value && imageTable.value[selectedImageIndex.value]) {
    const outerIndex = selectedImageIndex.value;
    const innerIndex = selectedRegin.value;

    const selectedItem = imageTable.value[outerIndex][innerIndex];

    // 调用子组件的 setTableData 方法更新数据
    ImagesTableRef.value.setTableData(
      selectedItem.ocr, // 保持原有序号
      fossilName.value || selectedItem.child_fig, // 使用弹窗中的名称或原有名称
      fossilWidth.value, // 设置化石宽度
      fossilLength.value, // 设置化石长度
      fossilWidthUnit.value, // 设置化石宽度单位
      fossilLengthUnit.value // 设置化石长度单位
    );

    // 同时更新本地存储的数据
    selectedItem.child_fig = fossilName.value || selectedItem.child_fig;
    selectedItem.width = { value: fossilWidth.value, unit: fossilWidthUnit.value };
    selectedItem.height = { value: fossilLength.value, unit: fossilLengthUnit.value };
  }
};


// 保存新的比例尺
const saveScaleWithPrompt = () => {
  if (!pixelLength.value || !actualLength.value) return;

  // 弹出输入框，让用户输入存档名称
  ElMessageBox.prompt('请输入存档名称', '存档', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputPattern: /^[\s\S]*.*[^\s][\s\S]*$/, // 确保用户输入非空内容
    inputErrorMessage: '存档名称不能为空'
  }).then(({ value }) => {
    // 用户点击确定并输入了名称
    const scaleValue = parseFloat(pixelLength.value) / parseFloat(actualLength.value);
    const newScale = {
      scale: scaleValue,
      pixelLength: pixelLength.value,
      actualLength: actualLength.value,
      unit: lengthUnit.value,
      name: value, // 使用用户输入的名称
      timestamp: Date.now()
    };

    savedScales.value.push(newScale);
    selectedScale.value = savedScales.value.length - 1;

    // 强制更新当前选中的存档
    loadScale(selectedScale.value, true);

    ElMessage.success(`存档成功，存档名称为：${value}`);
  }).catch(() => {
    // 用户点击了取消
    ElMessage.info('存档操作已取消');
  });
};

// 加载比例尺
const loadScale = async (index, forceReload = false) => {
  // 重置相关数据
  resetScaleData();

  if (index === null || index === undefined || !savedScales.value[index]) return;

  const saved = savedScales.value[index];

  // 更新基础数据
  scale.value = saved.scale;
  pixelLength.value = saved.pixelLength;
  actualLength.value = saved.actualLength;
  lengthUnit.value = saved.unit;
  fossilLengthUnit.value = saved.unit;
  fossilWidthUnit.value = saved.unit;

  // 确保DOM更新后计算化石尺寸
  await nextTick();
  calculateFossilDimensions();

  // 更新选中索引
  selectedScale.value = index;
};

// 删除比例尺
const deleteScale = () => {
  if (scaleToDelete.value === null) return;

  ElMessageBox.confirm(
    `确定要删除存档 "${savedScales.value[scaleToDelete.value].name}" 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    // 如果删除的是当前选中的存档，清空选中状态
    if (selectedScale.value === scaleToDelete.value) {
      selectedScale.value = null;
      resetScaleData();
    }

    // 调整选中索引（如果删除的是前面的存档）
    if (selectedScale.value > scaleToDelete.value) {
      selectedScale.value--;
    }

    savedScales.value.splice(scaleToDelete.value, 1);
    scaleToDelete.value = null;
    showDeleteDialog.value = false;

    ElMessage({
      message: '存档已删除',
      type: 'success',
      duration: 2000
    });
  }).catch(() => {
    // 用户点击了取消
    scaleToDelete.value = null;
  });
};

// 重置比例相关数据
const resetScaleData = () => {
  scale.value = null;
  pixelLength.value = "";
  actualLength.value = "";
  fossilLength.value = "";
  fossilWidth.value = "";
};

// 切换放大镜状态
const toggleMagnifier = () => {
  isMagnifierActive.value = !isMagnifierActive.value;
  if (!isMagnifierActive.value) {
    isHoverZoomed.value = false;
  }
};
// // 鼠标悬停事件处理
// const handleMouseHover = (event) => {
//   if (!largeImageRef.value) return;

//   const rect = largeImageRef.value.getBoundingClientRect();
//   mousePosition.value = {
//     x: event.clientX - rect.left,
//     y: event.clientY - rect.top
//   };

//   // 清除之前的计时器
//   if (hoverTimer.value) {
//     clearTimeout(hoverTimer.value);
//   }

//   // 设置新的计时器
//   hoverTimer.value = setTimeout(() => {
//     isHoverZoomed.value = true;
//     drawZoomedArea();
//   }, hoverTimeout);
// };

// // 鼠标离开事件处理
// const handleMouseLeave = () => {
//   // 清除计时器
//   if (hoverTimer.value) {
//     clearTimeout(hoverTimer.value);
//     hoverTimer.value = null;
//   }

//   // 关闭放大效果
//   isHoverZoomed.value = false;
//   resetCursor();

//   // 清除放大镜画布
//   if (zoomCanvasRef.value) {
//     const ctx = zoomCanvasRef.value.getContext("2d");
//     ctx.clearRect(0, 0, zoomCanvasRef.value.width, zoomCanvasRef.value.height);
//   }
// };

// // 绘制放大区域
// const drawZoomedArea = () => {
//   if (!isHoverZoomed.value || !largeImageRef.value || !zoomCanvasRef.value) return;

//   const img = largeImageRef.value;
//   const zoomCanvas = zoomCanvasRef.value;
//   const ctx = zoomCanvas.getContext("2d");

//   // 设置放大镜画布大小
//   zoomCanvas.width = zoomWindowSize.value;
//   zoomCanvas.height = zoomWindowSize.value;

//   // 计算放大区域
//   const zoomRectSize = zoomWindowSize.value / zoomLevel.value;
//   const sx = mousePosition.value.x - zoomRectSize / 2;
//   const sy = mousePosition.value.y - zoomRectSize / 2;

//   // 确保不超出图像边界
//   const clampedSx = Math.max(0, Math.min(sx, img.width - zoomRectSize));
//   const clampedSy = Math.max(0, Math.min(sy, img.height - zoomRectSize));

//   // 绘制放大区域
//   ctx.clearRect(0, 0, zoomCanvas.width, zoomCanvas.height);
//   ctx.drawImage(
//     img,
//     clampedSx, clampedSy, zoomRectSize, zoomRectSize, // 源矩形
//     0, 0, zoomWindowSize.value, zoomWindowSize.value  // 目标矩形
//   );

//   // 添加放大镜边框和十字准线
//   ctx.strokeStyle = "red";
//   ctx.lineWidth = 1;
//   ctx.strokeRect(0, 0, zoomCanvas.width, zoomCanvas.height);

//   // 十字准线
//   ctx.beginPath();
//   ctx.moveTo(zoomCanvas.width / 2, 0);
//   ctx.lineTo(zoomCanvas.width / 2, zoomCanvas.height);
//   ctx.moveTo(0, zoomCanvas.height / 2);
//   ctx.lineTo(zoomCanvas.width, zoomCanvas.height / 2);
//   ctx.stroke();

//   // 更新放大镜位置
//   positionZoomWindow();
// };

// // 定位放大窗口
// const positionZoomWindow = () => {
//   if (!zoomCanvasRef.value) return;

//   const offset = 20; // 距离鼠标的偏移量
//   let left = mousePosition.value.x + offset;
//   let top = mousePosition.value.y + offset;

//   // 确保放大镜不会超出视口
//   const imgRect = largeImageRef.value.getBoundingClientRect();
//   const maxLeft = imgRect.width - zoomWindowSize.value;
//   const maxTop = imgRect.height - zoomWindowSize.value;

//   left = Math.min(left, maxLeft);
//   top = Math.min(top, maxTop);

//   zoomCanvasRef.value.style.left = `${left}px`;
//   zoomCanvasRef.value.style.top = `${top}px`;
// };

// 鼠标移动事件处理
const handleMouseMove = (event) => {
  if (!largeImageRef.value || points.value.length === 0) return;

  const rect = largeImageRef.value.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.top;

  // 更新临时点
  tempPoint.value = { x, y };

  // 如果已经有一个点，绘制动态线段
  if (points.value.length === 1) {
    drawDynamicLine();
    calculateDynamicAngle();
  }

  // 放大镜功能 - 直接处理，不再等待定时器
  if (isMagnifierActive.value) {
    handleMagnifierHover(event);
  }
};

// 处理放大镜悬停
const handleMagnifierHover = (event) => {
  if (!largeImageRef.value || !imageContainer.value) return;

  // 清除之前的计时器
  if (hoverTimer.value) {
    clearTimeout(hoverTimer.value);
  }

  // 立即处理而不是等待定时器
  const containerRect = imageContainer.value.getBoundingClientRect();
  const img = largeImageRef.value;
  const imgRect = img.getBoundingClientRect();

  // 计算鼠标相对于图片的位置
  const mouseX = event.clientX - imgRect.left;
  const mouseY = event.clientY - imgRect.top;

  // 确保鼠标在图片范围内
  if (mouseX >= 0 && mouseX <= img.width && mouseY >= 0 && mouseY <= img.height) {
    isHoverZoomed.value = true;

    // 更新放大镜位置（考虑边界情况）
    magnifierPosition.value = {
      x: Math.min(
        Math.max(event.clientX - containerRect.left - zoomWindowSize.value / 2, 10),
        containerRect.width - zoomWindowSize.value - 10
      ),
      y: Math.min(
        Math.max(event.clientY - containerRect.top - zoomWindowSize.value / 2, 10),
        containerRect.height - zoomWindowSize.value - 10
      )
    };

    drawZoomedArea(mouseX, mouseY);
  } else {
    isHoverZoomed.value = false;
  }
};

// 绘制放大区域
const drawZoomedArea = (mouseX, mouseY) => {
  if (!isHoverZoomed.value || !largeImageRef.value || !zoomCanvasRef.value) return;

  const img = largeImageRef.value;
  const zoomCanvas = zoomCanvasRef.value;
  const ctx = zoomCanvas.getContext("2d");
  const mainCanvas = canvasRef.value;
  const mainCtx = mainCanvas.getContext("2d");

  // 确保画布大小正确
  zoomCanvas.width = zoomWindowSize.value;
  zoomCanvas.height = zoomWindowSize.value;

  // 计算放大区域 - 使用自然尺寸而不是显示尺寸
  const zoomRectSize = zoomWindowSize.value / zoomLevel.value;
  const sx = (mouseX / img.width) * img.naturalWidth - zoomRectSize / 2;
  const sy = (mouseY / img.height) * img.naturalHeight - zoomRectSize / 2;

  // 确保不超出图像边界
  const clampedSx = Math.max(0, Math.min(sx, img.naturalWidth - zoomRectSize));
  const clampedSy = Math.max(0, Math.min(sy, img.naturalHeight - zoomRectSize));

  // 清除并绘制放大区域
  ctx.clearRect(0, 0, zoomCanvas.width, zoomCanvas.height);
  ctx.drawImage(
    img,
    clampedSx, clampedSy, zoomRectSize, zoomRectSize, // 源矩形
    0, 0, zoomWindowSize.value, zoomWindowSize.value  // 目标矩形
  );

  // 绘制主画布内容到放大镜
  ctx.globalCompositeOperation = 'source-over';
  ctx.drawImage(
    mainCanvas,
    clampedSx, clampedSy, zoomRectSize, zoomRectSize, // 源矩形
    0, 0, zoomWindowSize.value, zoomWindowSize.value  // 目标矩形
  );

  // 添加放大镜边框和十字准线
  ctx.strokeStyle = "red";
  ctx.lineWidth = 2;
  ctx.strokeRect(0, 0, zoomCanvas.width, zoomCanvas.height);

  // 十字准线
  ctx.beginPath();
  ctx.moveTo(zoomCanvas.width / 2, 0);
  ctx.lineTo(zoomCanvas.width / 2, zoomCanvas.height);
  ctx.moveTo(0, zoomCanvas.height / 2);
  ctx.lineTo(zoomCanvas.width, zoomCanvas.height / 2);
  ctx.stroke();


};
// 鼠标离开时重置
const resetMouseMove = () => {
  tempPoint.value = null;
  drawPoints(); // 清除动态线段
  resetCursor(); // 重置光标样式

  // 清除放大镜相关状态
  if (hoverTimer.value) {
    clearTimeout(hoverTimer.value);
    hoverTimer.value = null;
  }
  isHoverZoomed.value = false;
};

// 动态绘制线段
const drawDynamicLine = () => {
  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawPoints();

  if (points.value.length === 1 && tempPoint.value) {
    ctx.beginPath();
    ctx.moveTo(points.value[0].x, points.value[0].y);
    ctx.lineTo(tempPoint.value.x, tempPoint.value.y);
    ctx.strokeStyle = "red";
    ctx.lineWidth = 2 * zoomLevel.value; // 放大动态线的宽度
    ctx.stroke();
  }
};

// 动态计算角度
const calculateDynamicAngle = () => {
  if (!points.value[0] || !tempPoint.value) return;

  const dx = tempPoint.value.x - points.value[0].x;
  const dy = tempPoint.value.y - points.value[0].y;
  const angleRad = Math.atan2(dy, dx); // 计算弧度
  const angleDeg = (angleRad * 180) / Math.PI; // 转换为度数

  // 显示角度
  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.font = "16px Arial";
  ctx.fillStyle = "black";
  ctx.textAlign = "center";
  ctx.fillText(`角度: ${angleDeg.toFixed(2)}°`, (points.value[0].x + tempPoint.value.x) / 2, (points.value[0].y + tempPoint.value.y) / 2);
};


// 新的点击事件处理方法
const handleImageClickForMeasurement = (event) => {
  if (!largeImageRef.value || !imageContainer.value) return;

  // 获取图片和容器元素
  const img = largeImageRef.value;
  const container = imageContainer.value;

  // 1. 计算容器相对于视口的位置
  const containerRect = container.getBoundingClientRect();

  // 2. 计算滚动偏移（如果有滚动条）
  const scrollLeft = container.scrollLeft || 0;
  const scrollTop = container.scrollTop || 0;

  // 3. 计算鼠标相对于图片左上角的精确坐标
  const x = event.clientX - containerRect.left + scrollLeft;
  const y = event.clientY - containerRect.top + scrollTop;

  // 4. 边界检查（确保点击在图片范围内）
  if (
    x < 0 || x > img.naturalWidth ||
    y < 0 || y > img.naturalHeight
  ) {
    return; // 点击在图片外则不处理
  }

  // 5. 存储坐标（最多2个点）
  if (points.value.length >= 2) {
    resetPoints(); // 清除之前的点
  }

  points.value.push({ x, y });

  // 6. 根据点数执行不同操作
  if (points.value.length === 1) {
    isDrawing.value = true;
  } else if (points.value.length === 2) {
    isDrawing.value = false;
    calculatePixelLength(); // 计算两点距离
    calculateAngle();       // 计算角度
  }

  // 7. 绘制点/线
  drawPoints();
  if (points.value.length === 2) {
    drawLine();
  }

  // points.value.push({ x, y });
  // drawPoints(); // 绘制点击的点

  // if (points.value.length === 2) {
  //   drawLine(); // 绘制连线
  //   calculatePixelLength(); // 计算像素长度
  //   calculateAngle(); // 计算角度
  // }
};

const calculateAngle = () => {
  const dx = points.value[1].x - points.value[0].x;
  const dy = points.value[1].y - points.value[0].y;
  const angleRad = Math.atan2(dy, dx);
  const angleDeg = (angleRad * 180) / Math.PI;

  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.font = `${16 * zoomLevel.value}px Arial`; // 放大字体
  ctx.fillStyle = "black";
  ctx.textAlign = "center";
  ctx.fillText(
    `角度: ${angleDeg.toFixed(2)}°`,
    (points.value[0].x + points.value[1].x) / 2,
    (points.value[0].y + points.value[1].y) / 2
  );
};

// 绘制点击的点
const drawPoints = () => {
  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  points.value.forEach(point => {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 3 * zoomLevel.value, 0, 2 * Math.PI); // 放大点的大小
    ctx.fillStyle = "red";
    ctx.fill();
  });
};

// 绘制两点之间的连线
const drawLine = () => {
  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.moveTo(points.value[0].x, points.value[0].y);
  ctx.lineTo(points.value[1].x, points.value[1].y);
  ctx.strokeStyle = "red";
  ctx.lineWidth = 2 * zoomLevel.value; // 放大线的宽度
  ctx.stroke();
};

// 计算像素长度
const calculatePixelLength = () => {
  if (points.value.length < 2) return;

  const dx = points.value[1].x - points.value[0].x;
  const dy = points.value[1].y - points.value[0].y;
  const pixelLen = Math.sqrt(dx * dx + dy * dy);
  pixelLength.value = pixelLen.toFixed(2);
};

// // 计算比例
// watch(actualLength, (newVal) => {
//   if (newVal && pixelLength.value) {
//     const actualLen = parseFloat(newVal);
//     const pixelLen = parseFloat(pixelLength.value);
//     scale.value = pixelLen / actualLen; // 计算比例
//     calculateFossilDimensions(); // 计算化石的长度和宽度
//   }
// });

// // 监听长度单位变化
// watch(lengthUnit, (newVal) => {
//   fossilLengthUnit.value = newVal; // 小图长度单位同步
//   fossilWidthUnit.value = newVal; // 小图宽度单位同步
//   calculateFossilDimensions(); // 重新计算化石的长度和宽度
// });

// // 监听小图长度单位变化
// watch(fossilLengthUnit, (newVal) => {
//   if (scale.value) {
//     calculateFossilDimensions(); // 重新计算化石的长度和宽度
//   }
// });

// // 监听小图宽度单位变化
// watch(fossilWidthUnit, (newVal) => {
//   if (scale.value) {
//     calculateFossilDimensions(); // 重新计算化石的长度和宽度
//   }
// });

// 计算化石的实际长度和宽度
const calculateFossilDimensions = () => {
  if (!scale.value || selectedRegin.value === null || !poses.value[selectedRegin.value]) {
    fossilLength.value = "";
    fossilWidth.value = "";
    return;
  }

  const rect = poses.value[selectedRegin.value];
  const widthPixels = rect[2];
  const heightPixels = rect[3];

  // 首先将实际长度转换为厘米（因为比例是基于厘米计算的）
  let actualLengthInCm = parseFloat(actualLength.value);
  if (lengthUnit.value === 'mm') {
    actualLengthInCm = actualLengthInCm / 10;
  } else if (lengthUnit.value === 'm') {
    actualLengthInCm = actualLengthInCm * 100;
  } else if (lengthUnit.value === 'inch') {
    actualLengthInCm = actualLengthInCm * 2.54;
  }

  // 计算比例（像素/厘米）
  const scaleValue = parseFloat(pixelLength.value) / actualLengthInCm;

  // 计算化石尺寸（以厘米为单位）
  const fossilLengthCm = heightPixels / scaleValue;
  const fossilWidthCm = widthPixels / scaleValue;

  // 转换为用户选择的单位
  let lengthConversion = 1;
  let widthConversion = 1;

  switch (fossilLengthUnit.value) {
    case 'mm': lengthConversion = 10; break;
    case 'm': lengthConversion = 0.01; break;
    case 'inch': lengthConversion = 0.393701; break;
  }

  switch (fossilWidthUnit.value) {
    case 'mm': widthConversion = 10; break;
    case 'm': widthConversion = 0.01; break;
    case 'inch': widthConversion = 0.393701; break;
  }

  fossilLength.value = (fossilLengthCm * lengthConversion).toFixed(2);
  fossilWidth.value = (fossilWidthCm * widthConversion).toFixed(2);
};

// 修改watch监听器，确保单位变化时重新计算
watch(lengthUnit, (newVal) => {
  fossilLengthUnit.value = newVal; // 小图长度单位同步
  fossilWidthUnit.value = newVal;  // 小图宽度单位同步
  if (scale.value) {
    calculateFossilDimensions(); // 重新计算化石的长度和宽度
  }
});

watch([actualLength, lengthUnit], () => {
  if (actualLength.value && pixelLength.value) {
    calculateFossilDimensions();
  }
});

watch([fossilLengthUnit, fossilWidthUnit], () => {
  if (scale.value) {
    calculateFossilDimensions();
  }
});

watch(selectedScale, (newVal) => {
  if (newVal !== null && savedScales.value[newVal]) {
    const selectedScale = savedScales.value[newVal];
    fossilLengthUnit.value = selectedScale.unit;
    fossilWidthUnit.value = selectedScale.unit;
  }
});



// 改变光标颜色
const changeCursor = () => {
  largeImageRef.value.style.cursor = "crosshair";
};

// 重置光标颜色
const resetCursor = () => {
  largeImageRef.value.style.cursor = "default";
};

// 重置点和画布
const resetPoints = () => {
  points.value = [];
  const canvas = canvasRef.value;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
};

// 在组件挂载时自动选择第二个文件
// 需要修改的地方
onMounted(() => {
  if (pdfList.value.length >= 2) {
    selectedPdf.value = pdfList.value[1]; // 选择第二个文件
    handlePdfChange(selectedPdf.value); // 触发文件选择后的处理逻辑
  }
});

// 在弹窗打开时初始化画布大小
watch(dialogVisible, async (newVal) => {
  if (!newVal) {
    // 弹窗关闭时清空输入框中的数据
    pixelLength.value = "";
    actualLength.value = "";
    lengthUnit.value = "cm";
    fossilLength.value = "";
    fossilWidth.value = "";
    fossilLengthUnit.value = "cm";
    fossilWidthUnit.value = "cm";
    fossilName.value = ""; // 清空化石名称
    points.value = []; // 清空点击的点
    resetPoints(); // 清空画布上的点和连线
  } else {
    await nextTick(); // 确保DOM更新完成

    // 初始化画布
    const canvas = canvasRef.value;
    const img = largeImageRef.value;
    if (img && canvas) {
      // 等待图片加载完成
      await new Promise(resolve => {
        if (img.complete) resolve();
        else img.onload = resolve;
      });

      // 设置 canvas 尺寸 = 图片自然尺寸
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;

      // 确保 canvas 的 CSS 尺寸也匹配（避免缩放）
      canvas.style.width = `${img.naturalWidth}px`;
      canvas.style.height = `${img.naturalHeight}px`;
    }
    resetPoints();

    // 如果是首次加载或者有选中的存档，强制重新加载
    if (isInitialLoad.value || selectedScale.value !== null) {
      if (selectedScale.value !== null && savedScales.value[selectedScale.value]) {
        await loadScale(selectedScale.value, true); // 强制重新加载
      }
      isInitialLoad.value = false;
    }
  }
});
</script>

<style scoped>
.dialog-content {
  /* display: flex;
  flex-direction: column;
  align-items: center; */
  background-color: rgb(221, 238, 229);
  padding: 10px;
  max-height: 90vh;
  /* 限制最大高度为视口的70% */
  overflow-y: auto;
  /* 添加滚动条以防内容过多 */
}

.dialog-container {
  display: flex;
  gap: 15px;
  width: 100%;
  min-height: 400px;
  /* 设置最小高度 */
}

.left-section {
  flex: 2;
  /* 占据2/3的空间 */
  display: flex;
  flex-direction: column;
  min-width: 0;
  /* 防止内容溢出 */
}

.right-section {
  flex: 1;
  /* 占据1/3的空间 */
  display: flex;
  flex-direction: column;
  height: 100%;
  /* 确保高度充满父容器 */
  min-width: 0;
  /* 防止内容溢出 */
}

.right-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: center;
  gap: 15px;
}

.right-content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  /* 垂直居中 */
  height: 100%;
  /* 确保高度充满父容器 */
  padding: 20px 0;
  /* 添加一些上下内边距 */
}

.large-image {
  width: 100%;
  max-height: 600px;
  /* 限制最大高度，避免弹窗过大 */
  overflow: auto;
  /* 添加滚动条 */
  position: relative;
  display: flex;
  justify-content: flex-start;
  /* 图片左对齐 */
  align-items: flex-start;
  /* 图片顶部对齐 */
  padding: 0;
  /* 移除内边距 */
  border: none;
  /* 移除边框（或计入坐标计算） */
  margin: 0;
  /* 移除外边距 */
  box-sizing: border-box;
  /* 确保边框不影响尺寸 */
}

.image-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
  /* 减少间距 */
}

.large-image img {
  max-width: none;
  /* 禁用最大宽度限制 */
  width: auto;
  /* 使用图片原始宽度 */
  height: auto;
  /* 使用图片原始高度 */
  display: block;
  /* 避免图片下方出现空白 */
}

.result-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  /* 控制输入框之间的间距 */
}

.input-container {
  margin: 10px 0;
  width: 100%;
}

.input-container label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group {
  display: flex;
  align-items: center;
  /* 垂直居中对齐 */
  margin-bottom: 15px;
  /* 输入框组之间的间距 */
}

.input-group label {
  width: auto;
  /* 自动宽度，根据内容调整 */
  min-width: 80px;
  /* 最小宽度，确保标签不会太窄 */
  text-align: right;
  margin-right: 10px;
  font-weight: bold;
  white-space: nowrap;
  /* 防止文字换行 */
  overflow: hidden;
  /* 隐藏溢出的部分 */
  text-overflow: ellipsis;
  /* 使用省略号表示溢出的文本 */
}

.input-group .el-input {
  flex: 1;
  /* 输入框占据剩余空间 */
  max-width: 200px;
}

.input-group .el-select {
  margin-left: 10px;
  /* 单位选择框与输入框的间距 */
  width: 100px;
}

.small-image-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0;
}

.small-image {
  display: flex;
  justify-content: center;
  align-items: center;
  /* 垂直居中 */
  min-height: 200px;
  /* 设置最小高度 */
}

.small-image img {
  max-width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: contain;
}

.elements {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.measure-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
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

/* 添加放大镜样式 */
.magnifier {
  position: absolute;
  border: 2px solid #409EFF;
  border-radius: 50%;
  overflow: hidden;
  pointer-events: none;
  z-index: 10;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.magnifier canvas {
  width: 100%;
  height: 100%;
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
  width: 32px;
  /* 图标的宽度 */
  height: 32px;
  /* 图标的高度 */
  fill: currentColor;
  /* 图标颜色 */
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

.pdf-select:deep(.el-select__wrapper) {
  width: 500px;
  /* 设置选择器的宽度 */
  border-radius: 8px;
  background: #e8fafe;
  /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
  height: 20px;
  /* 设置选择框的高度 */
  line-height: 20px;
  /* 保持文字垂直居中 */
  padding: 0 10px;
  /* 调整左右内边距 */
}

.pdf-select .el-select__prefix {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 10px;
  /* 根据需要调整间距 */
}

/* 调整内部输入框的样式 */
.pdf-select .el-input__inner {
  height: 20px;
  /* 确保内部输入框高度一致 */
  line-height: 20px;
  border-radius: 4px;
  /* 可选：调整圆角 */
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

  .dialog-container {
    flex-direction: column;
  }

  .left-section,
  .right-section {
    flex: none;
    width: 100%;
  }

  .right-content {
    margin-top: 15px;
  }
}
</style>