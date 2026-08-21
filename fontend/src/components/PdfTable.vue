<template>
  <div>
    <!-- 操作按钮 -->
    <div style="margin-bottom: 20px">
      <el-button 
      type="primary" 
      plain
      size="small" 
      style="height: 40px;  width: 10%;"
      @click="insertRow"> 插入行 </el-button>
      <el-button
        type="danger"
        style="height: 40px;  width: 10%;"
        @click="deleteSelectedRows"
        :disabled="!selectedRows.length"
      >
        删除选中行
      </el-button>
      <el-button 
      type="success"  
      plain
      style="height: 40px;  width: 10%;"
      @click="saveTable"> 保存表格 </el-button>
      <el-button 
        type="warning"  
        plain
        style="height: 40px;  width: 10%;"
        @click="exportTable"> 导出表格 </el-button>
    </div>

    <!-- 动态表格 -->
    <el-table
      :data="currentPageData"
      border
      style="width: 100%"
      ref="tableRef"
      @selection-change="handleSelectionChange"
    >
      <!-- 多选框 -->
      <el-table-column type="selection" width="50"></el-table-column>

      <!-- 动态生成列 -->
      <el-table-column
        v-for="(column, colIndex) in columns"
        :key="colIndex"
        :label="column.label"
      >
        <!-- 可编辑的列头 -->
        <template #header>
          <div class="custom-header">
          <el-input
            v-model="column.label"
            size="small"
            @change="updateColumnLabel(colIndex)"
          />
        </div>
        </template>
        <template #default="{ row }">
          <!-- 单元格可编辑 -->
          <el-input v-model="row[colIndex]" size="small" />
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页组件 -->
    <el-pagination
      v-if="paginationEnabled"
      style="margin-top: 20px; text-align: center"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="tableData.length"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose, defineProps, defineEmits } from "vue";
import * as XLSX from "xlsx";

// 接收父组件传递的初始数据和 PDF 名称
const props = defineProps({
  initialData: {
    type: Array,
    required: true,
  },
  pdfName: {
    type: String,
    required: true,
  },
  tableIndex: {
    type: Number,
    required: true,
  },
});

// 向父组件传递保存后的数据
const emit = defineEmits(["save-table"]);

// 表格完整数据
const tableData = ref([]);
// 当前页显示的数据
const currentPageData = ref([]);
// 表格列头
const columns = ref([]);

// 分页设置
const currentPage = ref(1); // 当前页码
const pageSize = ref(10); // 每页显示的行数
const paginationEnabled = ref(true); // 是否启用分页

// 多选行的功能
const selectedRows = ref([]); // 记录选中的行

// 生成表格数据
const generateTable = (data) => {
  const keys = data[0] || [];
  // 使用第一行数据作为列头
  columns.value = keys.map((key, index) => ({
    label: key, // 列标题
    prop: `column_${index}`, // 动态生成字段属性
  }));

  // 将 data 的第一行去掉，剩余部分存入 tableData
  tableData.value = data.slice(1);

  // 更新分页数据
  updateCurrentPageData();
};

// 更新当前页的数据
const updateCurrentPageData = () => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  currentPageData.value = tableData.value.slice(startIndex, endIndex);

  console.log("currentPageData当前表格内容:", currentPageData.value); // 输出表格的所有内容
};

// 分页组件的页码变化
const handlePageChange = (page) => {
  currentPage.value = page;
  updateCurrentPageData();
};

// 选中行变化时触发
const handleSelectionChange = (selected) => {
  selectedRows.value = selected;
};

// 插入一行
const insertRow = () => {
  const newRow = {};
  columns.value.forEach((col) => {
    newRow[col.prop] = ""; // 空白行
  });

  if (selectedRows.value.length > 0) {
    // 如果有选中行，找到选中行的最大索引
    const maxRowIndex = Math.max(
      ...selectedRows.value.map((row) => tableData.value.indexOf(row))
    );
    tableData.value.splice(maxRowIndex + 1, 0, newRow); // 在最大行索引的下一行插入
  } else {
    // 如果没有选中行，则在最顶部插入
    tableData.value.unshift(newRow);
  }

  // 更新分页显示
  updateCurrentPageData();
};

// 删除选中行
const deleteSelectedRows = () => {
  tableData.value = tableData.value.filter(
    (row) => !selectedRows.value.includes(row)
  );
  selectedRows.value = []; // 清空选中行
  updateCurrentPageData(); // 更新分页数据
};

// 保存表格数据
const saveTable = () => {
  console.log("当前表格内容:", tableData.value); // 输出表格的所有内容
  emit("save-table", tableData.value); // 将表格数据传递给父组件
};

// 主页面通过调用此方法，更新表格内容
const updateTableData = (newData) => {
  generateTable(newData); // 调用 generateTable 更新表格内容
};

// 初始化表格数据
onMounted(() => {
  console.log("initialData: ", props.initialData);
  generateTable(props.initialData); // 使用初始数据生成表格
});

// 导出表格数据为 Excel 文件
const exportTable = () => {
  // 构造文件名
  const fileName = `${props.pdfName}_第${props.tableIndex + 1}个表格.xlsx`;

  // 准备数据：第一行是列标题，后面是数据行
  const exportData = [
    columns.value.map(col => col.label), // 列标题
    ...tableData.value.map(row => {
      // 对于每一行数据，按照列的顺序提取单元格值
      return columns.value.map((_, colIndex) => row[colIndex] || '');
    })
  ];

  // 创建工作表
  const ws = XLSX.utils.aoa_to_sheet(exportData);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

  // 导出文件
  XLSX.writeFile(wb, fileName);
};

defineExpose({
  updateTableData, // 暴露给主页面的方法
});
</script>

<style scoped>
/* 样式可根据需求调整 */
.custom-header {
  background-color: #7fb5f2; /* 表头背景颜色 */
  color: #333; /* 表头文字颜色 */
  font-weight: bold; /* 加粗表头文字 */
  padding: 4px; /* 添加内边距 */
}


</style>
