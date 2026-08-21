<template>
  <div class="pdf-container">
    <div id="pdf-viewer" ref="pdfViewerRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps,watch } from 'vue'
import PDFObject from 'pdfobject'

const props = defineProps({
  pdfUrl: {
    type: String,
    required: true
  }
})
const pdfViewerRef = ref(null)

// 加载 PDF 的函数
// const loadPdf = (url) => {
//   const viewer = document.getElementById('pdf-viewer');
//   viewer.innerHTML = '';  // 清除现有的内容
//   PDFObject.embed(url, "#pdf-viewer", {
//     height: "800px",
//     pdfOpenParams: {
//       view: "FitH"
//     }
//   });
// };

const loadPdf = (url) => {
  const viewer = pdfViewerRef.value
  if (!viewer) return
  viewer.innerHTML = ''
  PDFObject.embed(url, viewer, {
    height: "800px",
    pdfOpenParams: {
      view: "FitH"
    }
  });
}

// 更改 PDF 文件的函数
// const changePdf = (pdfNewUrl) => {
//   // 获取 PDF 显示容器，并清空当前内容
//   const pdfContainer = document.getElementById('pdf-viewer')
//   pdfContainer.innerHTML = ''  // 清空容器
//   // 重新嵌入新的 PDF 文件
//   PDFObject.embed(pdfNewUrl, '#pdf-viewer')
// }

const changePdf = (pdfNewUrl) => {
  const viewer = pdfViewerRef.value
  if (!viewer) return
  viewer.innerHTML = ''
  PDFObject.embed(pdfNewUrl, viewer)
}


// 初始化加载 PDF 文件
onMounted(() => {
  loadPdf(props.pdfUrl);
});

// 监听 pdfUrl 的变化，重新加载 PDF
//watch(() => props.pdfUrl, (newPdfUrl) => {
//  loadPdf(newPdfUrl);
//});

// 使用 defineExpose 暴露 changePdf 函数
defineExpose({
  changePdf,
})

</script>

<style scoped>
.pdf-container {
  width:700px;  /* 可以根据需要调整宽度 */
  margin: 0 auto;
  border: 1px solid #ccc;
  border-radius: 4px;
}

#pdf-viewer {
  height: 850px;  /* 可以根据需要调整高度 */
  overflow-y: auto;
}

/* 自定义滚动条样式 */
#pdf-viewer::-webkit-scrollbar {
  width: 8px;
}

#pdf-viewer::-webkit-scrollbar-track {
  background: #f1f1f1;
}

#pdf-viewer::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

#pdf-viewer::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>