<template>
  <div class="document-library">
    <div class="header">
      <span class="title">文档库</span>
      <svg t="1740122874019" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
        p-id="1844" width="28" height="28">
        <path
          d="M190.57142832 254.85714248h642.85714336c19.28571416 0 32.14285752 12.85714248 32.14285664 32.14285752v482.14285752H158.42857168V287c0-19.28571416 12.85714248-32.14285752 32.14285664-32.14285752z"
          fill="#91D5FF" p-id="1845"></path>
        <path
          d="M225.92857168 126.28571416h540c19.28571416 0 35.35714248 16.07142832 35.35714248 32.14285752s-16.07142832 32.14285752-35.35714248 32.14285664H225.92857168C206.64285752 190.57142832 190.57142832 174.5 190.57142832 158.42857168s16.07142832-32.14285752 35.35714336-32.14285752z"
          fill="#BAE7FF" p-id="1846"></path>
        <path
          d="M110.21428584 479.85714248h202.5l61.07142832 141.42857168h273.21428584l73.92857168-141.42857168h192.85714248c25.71428584 0 48.21428584 22.5 48.21428584 48.21428584v385.71428584c0 25.71428584-22.5 48.21428584-48.21428584 48.21428584h-803.57142832C84.5 962 62 939.5 62 913.78571416v-385.71428584c3.21428584-25.71428584 22.5-48.21428584 48.21428584-48.21428584z"
          fill="#40A9FF" p-id="1847"></path>
        <path
          d="M287 769.14285752h450c19.28571416 0 32.14285752 12.85714248 32.14285752 32.14285664s-12.85714248 32.14285752-32.14285752 32.14285752H287c-19.28571416 0-32.14285752-12.85714248-32.14285752-32.14285752s12.85714248-32.14285752 32.14285752-32.14285664z"
          fill="#BAE7FF" p-id="1848"></path>
      </svg>
      <div class="search-container">
        <!-- SVG 图标 -->
        <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="2296" width="32" height="32">
          <path
            d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z"
            fill="#1296db" p-id="2297"></path>
        </svg>
        <!-- 搜索框 -->
        <el-input v-model="searchQuery" placeholder="输入文件名搜索" class="search-input" @input="handleSearch"
          clearable></el-input>
      </div>
    </div>
    <div class="button-group">
      <div class="group">
        <!-- 使用原生 input 元素选择文件 -->
        <el-button type="success" plain @click="triggerUpload">上传文件</el-button>
        <input type="file" ref="fileInput" @change="handleFileSelect" style="display: none;">
        <el-button type="danger" plain @click="deleteFiles">删除文件（仅限自己的文件）</el-button>
      </div>
      <div class="group-gap"></div>
      <div class="group">
        <el-button type="success" plain @click="submitDatabase">提交数据库（审批用户）</el-button>
        <el-button type="primary" plain @click="exportData">数据导出（审批用户）</el-button>
        <el-button type="primary" plain @click="goBack">返回项目库</el-button>
      </div>
    </div>

    <!-- <div v-if="logVisible" class="log-popover" :style="popoverPosition">
        <div v-for="msg in logsMap[currentFile]?.[currentService] || []">
          {{ msg }}
        </div>
      </div> -->

    <div v-if="logVisible" class="log-popover" :style="Object.assign({}, popoverPosition)">
      <div v-for="msg in logsMap[currentPdf]?.[currentService] || []">
        {{ msg }}
      </div>
    </div>



    <el-table :data="paginatedData" style="width: 100%;" @filter-change="handleFilterChange"
      @selection-change="handleSelectionChange">

      <!-- 第一列多选框 选中之后出发selection-change功能 -->
      <el-table-column type="selection" width="55"></el-table-column>

      <!-- 每一行文件详细信息 -->
      <el-table-column prop="name" label="文件名称" :filters="[{ text: 'Document1.pdf', value: 'Document1.pdf' }]"
        :filter-method="filterName">
        <template #default="scope">
          <div class="file-name-container">
            <!-- 文件图标 -->
            <svg class="file-icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="28"
              height="28">
              <path
                d="M902.101333 314.517333V853.333333a97.514667 97.514667 0 0 1-97.536 97.514667H219.434667A97.514667 97.514667 1 0 1 121.898667 853.333333V170.666667a97.514667 97.514667 0 0 1 97.536-97.514667H660.693333l241.386667 241.365333z"
                fill="#ED5050"></path>
              <path
                d="M660.714667 265.749333V73.173333l241.386666 241.365334h-192.618666a48.768 48.768 0 0 1-48.768-48.768z"
                fill="#D43030"></path>
              <path
                d="M633.898667 577.834667c-19.989333 0.341333-39.914667 2.624-59.477334 6.826666a288.661333 288.661333 0 0 1-59.008-76.074666c16.341333-52.906667 17.066667-88.981333 4.885334-106.048a31.445333 31.445333 0 0 0-24.384-12.437334 30.72 30.72 0 0 0-29.504 15.36c-17.066667 28.266667 7.552 84.352 19.008 107.029334A673.642667 673.642667 0 0 1 435.2 629.973333C344.021333 669.013333 341.333333 692.693333 341.333333 701.226667c0.32 10.517333 6.549333 19.946667 16.085334 24.362666 4.245333 2.645333 9.173333 3.925333 14.144 3.669334 24.384 0 51.2-26.581333 80.704-78.506667a658.282667 658.282667 0 0 1 112.64-36.096 121.898667 121.898667 0 0 0 70.208 28.544c16.106667 0 48.768 0 48.768-32.426667 0.256-10.986667-6.336-31.957333-49.984-32.917333z m-260.629334 124.330666h-2.922666a73.152 73.152 0 0 1 34.133333-27.541333 62.656 62.656 0 0 1-31.210667 27.541333zM489.813333 419.626667c1.28-0.448 2.645333-0.448 3.904 0h2.922667a80.938667 80.938667 0 0 1 0 48.746666 76.8 76.8 0 0 1-6.826667-48.746666z m48.768 183.829333a588.074667 588.074667 0 0 0-64.618666 19.008v-1.941333h-1.941334c10.474667-20.736 19.989333-42.666667 28.522667-64.362667v-1.962667c10.986667 16.704 23.637333 32.213333 37.781333 46.336h-2.666666l2.922666 2.922667z m97.514667 12.437333a82.645333 82.645333 0 0 1-28.757333-6.357333c8.021333-1.578667 16.213333-2.218667 24.362666-1.941333 18.773333 0 22.677333 4.629333 22.677334 7.552a40.96 40.96 0 0 1-18.517334 0.746666h0.234667z"
                fill="#FFFFFF"></path>
            </svg>
            <!-- 文件名 -->
            <span class="file-name">{{ scope.row.name }}</span>
          </div>
        </template>
      </el-table-column>


      <el-table-column prop="updateTime" label="更新时间" sortable>
        <template #header>
          <el-button type="text" @click="showDateFilter = !showDateFilter">筛选日期</el-button>
        </template>
        <template #default="scope">
          {{ scope.row.updateTime }}
        </template>
      </el-table-column>

      <!-- 连接三个不同的后端程序，开始处理pdf抽取功能 -->
      <el-table-column prop="imageStatus" label="图片抽取状态">
        <template #default="scope">
          <el-button v-if="scope.row.imageStatus === 'Completed'" type="text" @click="jumpToDetailImage(scope.row)">
            跳转
          </el-button>
          <div v-else-if="scope.row.imageStatus === 'Processing'" @mouseover="showLog($event, scope.row, 'image')"
            @mouseleave="hideLog" class="loading-text" style="position: relative;">
            正在处理...
          </div>
          <el-button v-else-if="scope.row.imageStatus === 'Unready'" type="text" @click="handleImageProcess(scope.row)">
            处理
          </el-button>
          <el-button v-else-if="scope.row.imageStatus === 'Error'" type="text" @click="handleImageProcess(scope.row)">
            重试
          </el-button>
        </template>
      </el-table-column>

      <!-- 连接三个不同的后端程序，开始处理pdf抽取功能 -->
      <el-table-column prop="tableStatus" label="表格抽取状态">
        <template #default="scope">
          <el-button v-if="scope.row.tableStatus === 'Completed'" type="text" @click="jumpToDetailTable(scope.row)">
            跳转
          </el-button>
          <div v-else-if="scope.row.tableStatus === 'Processing'" @mouseover="showLog($event, scope.row, 'table')"
            @mouseleave="hideLog" class="loading-text" style="position: relative;">
            正在处理...
          </div>
          <el-button v-else-if="scope.row.tableStatus === 'Unready'" type="text" @click="handleTableProcess(scope.row)">
            处理
          </el-button>
          <el-button v-else-if="scope.row.tableStatus === 'Error'" type="text" @click="handleTableProcess(scope.row)">
            重试
          </el-button>
        </template>
      </el-table-column>

      <!-- 连接三个不同的后端程序，开始处理pdf抽取功能 -->
      <el-table-column prop="entityStatus" label="实体抽取状态">
        <template #default="scope">
          <el-button v-if="scope.row.entityStatus === 'Completed'" type="text" @click="jumpToDetailEntity(scope.row)">
            跳转
          </el-button>
          <div v-else-if="scope.row.entityStatus === 'Processing'" @mouseover="showLog($event, scope.row, 'entity')"
            @mouseleave="hideLog" class="loading-text" style="position: relative;">
            正在处理...
          </div>
          <el-button v-else-if="scope.row.entityStatus === 'Unready'" type="text"
            @click="handleEntityProcess(scope.row)">
            处理
          </el-button>
          <el-button v-else-if="scope.row.entityStatus === 'Error'" type="text" @click="handleEntityProcess(scope.row)">
            重试
          </el-button>
        </template>
      </el-table-column>


      <el-table-column prop="correction" label="是否被修正"
        :filters="[{ text: '未修正', value: '未修正' }, { text: '已完成修正', value: '已完成修正' }]" :filter-method="filterCorrection">
        <template #default="scope">
          <div class="status-icon">
            <!-- 已修正 -->
            <svg v-if="scope.row.correction === '已完成修正'" class="icon" viewBox="0 0 1024 1024" version="1.1"
              xmlns="http://www.w3.org/2000/svg" width="24" height="24">
              <path
                d="M927.288889 244.622222l-142.222222-147.911111c-51.2-51.2-142.222222-51.2-193.422223 0l-506.311111 506.311111c-17.066667 17.066667-28.444444 39.822222-28.444444 62.577778v233.244444c0 45.511111 22.755556 68.266667 68.266667 68.266667h233.244444c22.755556 0 45.511111-11.377778 62.577778-28.444444l500.622222-506.311111c56.888889-51.2 56.888889-136.533333 5.688889-187.733334zM352.711111 893.155556h-227.555555v-221.866667-11.377778c0 5.688889 5.688889 11.377778 5.688888 11.377778L341.333333 881.777778c5.688889 5.688889 11.377778 5.688889 11.377778 5.688889 5.688889 5.688889 5.688889 5.688889 0 5.688889z m51.2-34.133334c0-5.688889-5.688889-17.066667-11.377778-22.755555L182.044444 625.777778c-5.688889-5.688889-11.377778-11.377778-22.755555-11.377778l341.333333-341.333333 244.622222 244.622222-341.333333 341.333333z m472.177778-472.177778L796.444444 466.488889 551.822222 221.866667l79.644445-79.644445c28.444444-28.444444 68.266667-28.444444 96.711111 0l142.222222 147.911111c34.133333 28.444444 34.133333 68.266667 5.688889 96.711111z"
                fill="#1296db" p-id="6125"></path>
            </svg>
            <!-- 未修正 -->
            <svg v-else class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="24"
              height="24">
              <path
                d="M927.288889 244.622222l-142.222222-147.911111c-51.2-51.2-142.222222-51.2-193.422223 0l-506.311111 506.311111c-17.066667 17.066667-28.444444 39.822222-28.444444 62.577778v233.244444c0 45.511111 22.755556 68.266667 68.266667 68.266667h233.244444c22.755556 0 45.511111-11.377778 62.577778-28.444444l500.622222-506.311111c56.888889-51.2 56.888889-136.533333 5.688889-187.733334zM352.711111 893.155556h-227.555555v-221.866667-11.377778c0 5.688889 5.688889 11.377778 5.688888 11.377778L341.333333 881.777778c5.688889 5.688889 11.377778 5.688889 11.377778 5.688889 5.688889 5.688889 5.688889 5.688889 0 5.688889z m51.2-34.133334c0-5.688889-5.688889-17.066667-11.377778-22.755555L182.044444 625.777778c-5.688889-5.688889-11.377778-11.377778-22.755555-11.377778l341.333333-341.333333 244.622222 244.622222-341.333333 341.333333z m472.177778-472.177778L796.444444 466.488889 551.822222 221.866667l79.644445-79.644445c28.444444-28.444444 68.266667-28.444444 96.711111 0l142.222222 147.911111c34.133333 28.444444 34.133333 68.266667 5.688889 96.711111z"
                fill="#d81e06" p-id="6125"></path>
            </svg>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="approval" label="是否被审批"
        :filters="[{ text: '未审批', value: '未审批' }, { text: '已完成审批', value: '已完成审批' }]" :filter-method="filterApproval">
        <template #default="scope">
          <div class="status-icon">
            <!-- 已审核 -->
            <svg v-if="scope.row.approval === '已完成审批'" class="icon" viewBox="0 0 1024 1024" version="1.1"
              xmlns="http://www.w3.org/2000/svg" width="24" height="24">
              <path
                d="M0 0m180.705882 0l662.588236 0q180.705882 0 180.705882 180.705882l0 662.588236q0 180.705882-180.705882 180.705882l-662.588236 0q-180.705882 0-180.705882-180.705882l0-662.588236q0-180.705882 180.705882-180.705882Z"
                fill="#1676FF" p-id="9145"></path>
              <path
                d="M785.377882 562.055529h-102.279529c-22.678588 0-43.158588-13.251765-52.013177-33.671529l-35.026823-80.685176a29.184 29.184 0 0 1 7.860706-33.641412 131.915294 131.915294 0 0 0 42.345412-128.512c-10.902588-50.477176-52.675765-91.256471-104.32753-101.797647-88.545882-18.100706-166.550588 47.495529-166.550588 130.891294 0 40.176941 18.221176 75.986824 46.893176 100.47247a29.304471 29.304471 0 0 1 8.342589 34.032942l-34.394353 79.239529a56.560941 56.560941 0 0 1-52.013177 33.671529H238.622118a27.467294 27.467294 0 0 0-27.798589 27.166118v106.435765c0 14.998588 12.438588 27.166118 27.798589 27.166117h546.755764c15.36 0 27.798588-12.167529 27.798589-27.166117v-106.405647a27.467294 27.467294 0 0 0-27.798589-27.196236zM769.355294 783.058824H254.644706c-7.559529 0-13.703529 6.806588-13.70353 15.209411v29.816471c0 8.402824 6.144 15.209412 13.70353 15.209412h514.710588c7.559529 0 13.703529-6.806588 13.70353-15.209412v-29.816471c0-8.402824-6.144-15.209412-13.70353-15.209411z"
                fill="#FFFFFF" p-id="9146"></path>
            </svg>
            <!-- 未审核 -->
            <svg v-else class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="24"
              height="24">
              <path
                d="M106.9056 804.522667a33.450667 33.450667 0 0 1-33.723733-33.314134v-99.669333c0-55.159467 45.329067-99.805867 101.239466-99.805867h176.674134a33.655467 33.655467 0 0 0 33.041066-26.624c5.256533-25.258667 2.8672-41.437867-7.168-48.3328a231.492267 231.492267 0 0 1-101.1712-182.954666l-0.136533-7.9872c0-128.546133 105.813333-232.789333 236.3392-232.789334l8.123733 0.136534c124.040533 4.164267 223.914667 102.4 228.010667 224.597333l0.2048 8.055467-0.136533 7.918933a231.560533 231.560533 0 0 1-101.1712 183.022933c-9.966933 6.894933-12.424533 23.074133-7.168 48.3328a33.450667 33.450667 0 0 0 29.0816 26.4192l4.027733 0.2048h176.605867c53.930667 0 98.030933 41.5744 101.102933 93.866667l0.2048 5.870933v99.805867a33.450667 33.450667 0 0 1-29.832533 32.9728l-3.959467 0.273067H106.9056zM109.704533 877.568h804.590934c24.3712 0 36.590933 12.219733 36.590933 36.590933 0 24.3712-12.219733 36.590933-36.590933 36.590934H109.704533c-24.3712 0-36.522667-12.219733-36.522666-36.590934 0-24.3712 12.151467-36.590933 36.522666-36.590933z"
                fill="#EB0000" p-id="10214"></path>
            </svg>
          </div>
        </template>
      </el-table-column>
    </el-table>


    <el-dialog v-model="showDateFilter" title="筛选日期">
      <el-date-picker v-model="selectedDate" type="daterange" start-placeholder="开始日期" end-placeholder="结束日期"
        @change="handleDateChange" :picker-options="pickerOptions"></el-date-picker>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showDateFilter = false">取消</el-button>
          <el-button type="primary" @click="confirmDateFilter">确定</el-button>
        </div>
      </template>
    </el-dialog>
    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
      :page-sizes="[5, 10, 15, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
      :total="tableData.length">
    </el-pagination>
  </div>
</template>

<script setup>
import { ref, computed, inject, watch, onMounted, nextTick } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import axios from 'axios';
import COS from 'cos-js-sdk-v5';

const router = useRouter(); // 使用useRouter
const globalState = inject('globalState'); // 注入全局状态
const tableData = ref([
  { id: 1, name: 'DX-2018-JP-Ammonoid ', pdf_id: 1, uploader: 'User1', updateTime: '2024-01-01', imageStatus: 'Unready', tableStatus: 'Unready', entityStatus: 'Unready', correction: '未修正', approval: '未审批' },
  { id: 2, name: 'The dentition', pdf_id: 2, uploader: 'User2', updateTime: '2024-09-06', imageStatus: 'Completed', tableStatus: 'Completed', entityStatus: 'Completed', correction: '已完成修正', approval: '已完成审批' },
  { id: 3, name: 'Waterbird foraging traces from the early Eocene Green River Formation, Utah', pdf_id: 3, uploader: 'User3', updateTime: '2024-12-24', imageStatus: 'Completed', tableStatus: 'Completed', entityStatus: 'Completed', correction: '已完成修正', approval: '已完成审批' },
  { id: 4, name: 'A remarkable spiny arachnid from the Pennsylvanian Mazon Creek Lagerstätte, Illinois', pdf_id: 4, uploader: 'User4', updateTime: '2024-11-01', imageStatus: 'Completed', tableStatus: 'Completed', entityStatus: 'Completed', correction: '已完成修正', approval: '已完成审批' },

  // // 更多数据...
]);

const currentPage = ref(1);
const pageSize = ref(10); // 每页显示的条目数

const selectedRows = ref([]); // 选中的行

const fileList = ref([]); // 上传文件列表
const fileInput = ref(null); // 文件输入元素的引用

const correctionFilter = ref([]); // 用于存储是否被修正的筛选值
const approvalFilter = ref([]); // 用于存储是否被审批的筛选值

const showDateFilter = ref(false);
const selectedDate = ref(null);
const pickerOptions = ref({
  shortcuts: [
    {
      text: '最近一周',
      onClick(picker) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 1000 * 60 * 60 * 24 * 7);
        picker.$emit('pick', [start, end]);
      }
    },
    {
      text: '最近一个月',
      onClick(picker) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 1000 * 60 * 60 * 24 * 30);
        picker.$emit('pick', [start, end]);
      }
    },
    {
      text: '最近三个月',
      onClick(picker) {
        const end = new Date();
        const start = new Date();
        start.setTime(start.getTime() - 1000 * 60 * 60 * 24 * 90);
        picker.$emit('pick', [start, end]);
      }
    }
  ],
  firstDayOfWeek: 1 // 例如，设置每周的第一天为星期一
});

const searchQuery = ref()


const handleModleProcess = async (row, url, serviceType) => {
  const post = { "pdf_id": row.pdf_id, "pdf_url": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/01xybTest/01xybTest.pdf' }
  console.log(post)

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(post),
    });

    if (serviceType === "entity") {
      row.entityStatus = "Processing"
    }
    else if (serviceType === "image") {
      row.imageStatus = "Processing"
    }
    else if (serviceType === "table") {
      row.tableStatus = "Processing"
    }

    if (!response.ok) {
      throw new Error(`请求失败，状态码: ${response.status}`);
    }

    // SSE 原生 EventSource 不支持 POST，这里用流处理
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    logsMap[row.pdf_id][serviceType] = []

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const dataStr = line.slice(6).trim();

          if (!(dataStr.startsWith("{") || dataStr.startsWith("["))) {
            console.error("收到非 JSON 格式数据:", dataStr);
            reader.cancel();
            ElMessage.error("服务内部错误：" + dataStr); // 可以替换为你项目里的错误提示方式
            return;
          }


          try {
            const data = JSON.parse(dataStr);

            if (data.event === "status") {
              console.log(data)
              const timestamp = new Date().toLocaleTimeString();
              const logMsg = `[${timestamp}] ${data.message}`;

              // 确保 logsMap 里有对应数组，防止报错
              if (!logsMap[row.pdf_id]) logsMap[row.pdf_id] = {};
              if (!logsMap[row.pdf_id][serviceType]) logsMap[row.pdf_id][serviceType] = [];

              // 推入日志
              logsMap[row.pdf_id][serviceType].push(logMsg);

              if (data.status === "success") {
                reader.cancel();
                // if (serviceType === "entity") {
                //   row.entityStatus = "Completed"
                // }
                // else if (serviceType === "image") {
                //   row.imageStatus = "Completed"
                // }
                // else if (serviceType === "table") {
                //   row.tableStatus = "Completed"
                // }
                break;
              }
              else if (data.status === "error") {
                console.error("错误:", data.error);
                reader.cancel();
                console.error("抱歉，发生了一些错误，请稍后重试。");
                return;
              }
            }

            if (data.error) {
              console.error("错误:", data.error);
              reader.cancel();
              return;

            }
          } catch (e) {
            console.error("JSON 解析失败:", e, "收到数据:", dataStr);
          }
        }
      }
    }


  } catch (error) {
    console.error('处理失败:', error);
  }

}

const handleImageProcess = async (row) => {
  const post = { "pdf_id": row.pdf_id, "pdf_url": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/01xybTest/01xybTest.pdf' }
  console.log(post)
  const url = 'http://localhost:8000/api/imageProcess' //待改
  handleModleProcess(row, url, "image")
}

const handleTableProcess = async (row) => {
  const post = { "pdf_id": row.pdf_id, "pdf_url": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/01xybTest/01xybTest.pdf' }
  console.log(post)
  const url = 'http://localhost:8000/api/tableProcess'  //待改
  handleModleProcess(row, url, "table")
}

const handleEntityProcess = async (row) => {
  const post = { "pdf_id": row.pdf_id, "pdf_url": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/01xybTest/01xybTest.pdf' }
  console.log(post)
  const url = 'http://localhost:8000/api/entityProcess'
  handleModleProcess(row, url, "entity")

}


const logsMap = {
  "1": {
    entity: [
    ],
    table: [
      "表格识别开始",
      "找到 3 个表格",
      "表格数据解析成功"
    ],
    image: [
      "图像识别模型加载中...",
      "图像区域处理完成"
    ]
  },
  "2": {
    entity: [
      "实体抽取中...",
      "共找到 7 个实体"
    ],
    table: [
      "无表格区域"
    ]
  }
}

const popoverPosition = ref({
  top: '100px',
  left: '150px',
  position: 'absolute'
})

const currentPdf = ref(null)
const currentService = ref(null)
const logVisible = ref(false)

const showLog = (Event, row, serviceType) => {

  popoverPosition.value = {
    top: Event.clientY + 10 + 'px',
    left: Event.clientX + 10 + 'px',
    position: 'absolute'
  }
  currentPdf.value = row.pdf_id
  currentService.value = serviceType
  logVisible.value = true

}

const hideLog = () => {
  logVisible.value = false
}



const filteredData = computed(() => {
  let filteredData = tableData.value;
  if (searchQuery.value) {
    filteredData = filteredData.filter(item => item.name.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }
  if (selectedDate.value) {
    const [startDate, endDate] = selectedDate.value;
    filteredData = filteredData.filter(item => {
      const itemDate = new Date(item.updateTime);
      return itemDate >= startDate && itemDate <= endDate;
    });
  }
  if (correctionFilter.value.length > 0) {
    filteredData = filteredData.filter(item => correctionFilter.value.includes(item.correction));
  }
  if (approvalFilter.value.length > 0) {
    filteredData = filteredData.filter(item => approvalFilter.value.includes(item.approval));
  }
  return filteredData;
});

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredData.value.slice(start, end);
});

// 监听filteredData的变化，更新全局的pdf_ids_list
watch(filteredData, (newVal) => {
  globalState.pdf_ids_list = newVal.map(item => item.pdf_id);
  console.log('Updated pdf_ids_list:', globalState.pdf_ids_list); // 检查更新后的列表
});

const handleFilterChange = (filters) => {
  console.log("筛选Filters:", filters);
  // 重置筛选条件
  correctionFilter.value = [];
  approvalFilter.value = [];
  let filteredData = tableData.value;
  Object.keys(filters).forEach(key => {
    if (filters[key].length > 0) {
      const filterValues = filters[key].map(item => item.value);
      if (key === 'correction') {
        // 更新是否被修正的筛选条件
        correctionFilter.value = filterValues;
      } else if (key === 'approval') {
        // 更新是否被审批的筛选条件
        approvalFilter.value = filterValues;
      } else if (key === 'updateTime') {
        // 处理时间筛选
        const [startDate, endDate] = filters[key][0].value;
        filteredData = filteredData.filter(item => {
          const itemDate = new Date(item.updateTime);
          return itemDate >= startDate && itemDate <= endDate;
        });
      } else {
        filteredData = filteredData.filter(item => filterValues.includes(item[key]));
      }
    }
  });
  // 更新 paginatedData 以重新渲染表格
  currentPage.value = 1; // 重置当前页为第一页
  paginatedData.value = filteredData.slice(0, pageSize.value); // 修改这里
};

const handleDateChange = (value) => {
  selectedDate.value = value;
  if (value) {
    const [startDate, endDate] = value;
    const filters = { updateTime: [{ value: [startDate, endDate] }] };
    handleFilterChange(filters);
  }
};
const confirmDateFilter = () => {
  if (selectedDate.value) {
    const [startDate, endDate] = selectedDate.value;
    const filters = { updateTime: [{ value: [startDate, endDate] }] };
    handleFilterChange(filters);
  }
  showDateFilter.value = false;
};

const filterName = (value, row) => row.name.toLowerCase().includes(value.toLowerCase());
const filterCorrection = (value, row) => {
  console.log("筛选值 - 是否被修正:", value);
  return row.correction === value;
};
const filterApproval = (value, row) => {
  console.log("筛选值 - 是否被审批:", value);
  return row.approval === value;
}
const handleSelectionChange = (val) => {
  selectedRows.value = val;
};

const deleteFiles = () => {
  if (selectedRows.value.length === 0) {
    ElMessageBox.alert('请先选择要删除的文件', '提示');
    return;
  }

  ElMessageBox.confirm('确定要删除选中的文件吗？', '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 删除选中的行
    selectedRows.value.forEach(row => {
      const index = tableData.value.indexOf(row);
      if (index !== -1) {
        tableData.value.splice(index, 1);
      }
    });
    // 重置选中的行
    selectedRows.value = [];
    ElMessageBox.alert('文件删除成功', '提示');
  }).catch(() => {
    // 取消删除
    ElMessageBox.alert('已取消删除', '提示');
  });
};

const uploadFile = () => {
  ElMessageBox.alert('上传文件功能尚未实现', '提示');
};

const submitDatabase = () => {
  ElMessageBox.alert('提交数据库功能尚未实现', '提示');
};

const exportData = () => {
  ElMessageBox.alert('数据导出功能尚未实现', '提示');
};

const goBack = () => {
  // 使用router.push进行页面跳转到项目库
  router.push({ name: 'ProjcetVue' });
};

const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  // 重置当前页为第一页，以便重新计算分页数据
  currentPage.value = 1;
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
};

const jumpToDetailImage = (row) => {
  // 设置全局变量pdf_id
  //const globalState = inject('globalState');
  globalState.pdf_id = row.pdf_id; // 直接访问属性，不需要 .value
  console.log("global变量pdfid：", globalState.pdf_id);
  // 使用router.push进行页面跳转
  // router.push({ name: 'PictureVue' });
  const route = router.resolve({ name: 'PictureVue' });
  window.open(route.href, '_blank');

  //为全局变量赋值
  //const globalState = inject('globalState');
  // 修改 pdf_id
  //globalState.pdf_id = id;
  //globalState.pdfList=pdfList;

  // 使用router.push进行页面跳转
  //router.push({ name: 'PictureVue' });
  //ElMessageBox.alert(`跳转到 ${row.name} 的详情`, '提示');
};

const jumpToDetailTable = (row) => {
  //为全局变量赋值
  // 设置全局变量pdf_id
  //const globalState = inject('globalState');
  globalState.pdf_id = row.pdf_id; // 直接访问属性，不需要 .value
  console.log("global变量pdfid：", globalState.pdf_id);
  // 使用router.push进行页面跳转
  // router.push({ name: 'TableVue' });

  const route = router.resolve({ name: 'TableVue' });
  window.open(route.href, '_blank');
  //const globalState = inject('globalState');
  // 修改 pdf_id
  //globalState.pdf_id = id;
  //globalState.pdfList=pdfList;

  // 使用router.push进行页面跳转
  //router.push({ name: 'TableVue' });
  //ElMessageBox.alert(`跳转到 ${row.name} 的详情`, '提示');
};

const jumpToDetailEntity = (row) => {
  //为全局变量赋值
  // 设置全局变量pdf_id
  //const globalState = inject('globalState');
  globalState.pdf_id = row.pdf_id; // 直接访问属性，不需要 .value
  console.log("global变量pdfid：", globalState.pdf_id);
  // 使用router.push进行页面跳转
  const route = router.resolve({ name: 'EntityVue' });
  window.open(route.href, '_blank');

  //const globalState = inject('globalState');
  // 修改 pdf_id
  //globalState.pdf_id = id;
  //globalState.pdfList=pdfList;

  // 使用router.push进行页面跳转
  //router.push({ name: 'EntityVue' });
  //ElMessageBox.alert(`跳转到 ${row.name} 的详情`, '提示');
};

const handleSearch = () => {
  // 重置当前页为第一页，以便重新计算分页数据
  currentPage.value = 1;
};

const triggerUpload = () => {
  // 触发文件选择对话框
  fileInput.value.click();

  startStatusUpdate();
};

const handleFileSelect = (event) => {

  // 处理文件选择事件
  const file = event.target.files[0];
  if (!file) {
    alert('未选择上传文件');
    return;
  }

  // 获取后端随机生成的 pdf_id
  const pdf_id = "00011";

  const initData = {
    "proId": 5
  }
  let headers = {
    'Content-Type': 'application/json', // 告诉服务器我们发送的是JSON格式的数据
    'Accept': 'application/json', // 告诉服务器我们期望接收JSON格式的响应
  }

  axios.post("http://localhost:18000/api/document/init", initData, { headers: headers })
    .then(function (response) {
      // 请求成功时执行的代码
      console.log('Success:', response.data);

    })
    .catch(function (error) {
      // 请求失败时执行的代码
      if (error.response) {
        // 服务器返回了错误状态码
        console.log('Error Status:', error.response.status);
        console.log('Error Data:', error.response.data);
      } else if (error.request) {
        // 请求已经发出，但没有收到回应
        console.log('Error Request:', error.request);
      } else {
        // 发送请求时出了点问题
        console.log('Error Message:', error.message);
      }
    });

  const formData = new FormData();
  formData.append('file', file);
  formData.append('proId', 5);
  formData.append('pdfUploader', "Li");
  formData.append('imageStatus', "Pending");
  formData.append('tableStatus', "Pending");
  formData.append('entityStatus', "Pending");
  formData.append('correctionStatus', "未修正");
  formData.append('approvalStatus', "未审批");
  console.log(typeof file.size)

  const fileData = {
    pdfId: pdf_id,
    name: file.name,
    size: file.size,
    // type: file.type,
    uploadTime: file.lastModified,
    uploader: '当前用户',
    updateTime: new Date().toISOString().slice(0, 10),
    imageStatus: 'Pending',
    tableStatus: 'Pending',
    entityStatus: 'Pending',
    correction: '未修正',
    approval: '未审批',
    pdfUrl: "https://example.com/path/to/pdf.pdf"
  };
  tableData.value.unshift(fileData);


  // Tencent COS 使用
  // const cos = new COS({
  //   SecretId: "AKIDtnX5RaWGn8GHEzYu6DAvUs79zscBy64s", // 推荐使用环境变量获取；用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参考https://cloud.tencent.com/document/product/598/37140
  //   SecretKey: "hDd1PfCqQxZ3MTcfZO2bx63pOkz1rYfb", // 推荐使用环境变量获取；用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参考https://cloud.tencent.com/document/product/598/37140
  // });
  //const cos = new COS({

  //})
  // cos.uploadFile({
  //   Bucket: 'paleodb-1306565154', /* 填写自己的 bucket，必须字段 */
  //   Region: 'ap-shanghai',     /* 存储桶所在地域，必须字段 */
  //   Key: pdf_id,              /* 存储在桶里的对象键（例如:1.jpg，a/b/test.txt，图片.jpg）支持中文，必须字段 */
  //   Body: file, // 上传文件对象
  //   SliceSize: 1024 * 1024 * 5,     /* 触发分块上传的阈值，超过5MB使用分块上传，小于5MB使用简单上传。可自行设置，非必须 */
  //   onProgress: function (progressData) {
  //     console.log(JSON.stringify(progressData));
  //   }
  // }, function (err, data) {
  //   if (err) {
  //     console.log('上传失败', err);
  //   } else {
  //     console.log('上传成功');
  //   }
  // });



  // 2 号机 miniIO 对象存储使用
  headers = {
    'Content-Type': 'multipart/form-data'
  }
  axios.post("http://localhost:18000/api/document/upload", formData, { headers: headers })
    .then(function (response) {
      // 请求成功时执行的代码
      console.log('Success:', response.data);
    })
    .catch(function (error) {
      // 请求失败时执行的代码
      if (error.response) {
        // 服务器返回了错误状态码
        console.log('Error Status:', error.response.status);
        console.log('Error Data:', error.response.data);
      } else if (error.request) {
        // 请求已经发出，但没有收到回应
        console.log('Error Request:', error.request);
      } else {
        // 发送请求时出了点问题
        console.log('Error Message:', error.message);
      }
    });
  ElMessage.success(`成功选择了 ${files.length} 个文件`);

  // 重置文件输入元素，以便可以再次选择相同的文件
  fileInput.value.value = null;
};


</script>

<style scoped>
.log-popover {
  position: absolute;
  z-index: 9999;
  background-color: #e6f4ea;
  /* 浅蓝色背景 */
  color: #555f7a;
  /* 柔和圆滑的字体颜色 */
  padding: 10px 15px;
  /* 增加一点内边距 */
  border-radius: 12px;
  /* 更圆润的边角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1),
    /* 轻微阴影，产生突起感 */
    0 1px 3px rgba(0, 0, 0, 0.06);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  /* 更现代圆润的字体 */
  font-size: 14px;
  line-height: 1.4;
}


.title {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title .icon {
  width: 32px;
  height: 32px;
  margin-right: 8px;
}

/* 搜索框优化 */
.search-container {
  flex: 1;
  max-width: 400px;
  margin-left: auto;
  position: relative;
}

.search-input :deep(.el-input__wrapper) {
  padding-left: 40px;
  border-radius: 8px;
  background: #e8fafe;
  /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
}

.search-container .icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

.document-library {
  padding: 20px;
}

/* 头部优化 */
.header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 按钮组优化 */
.button-group {
  display: flex;
  justify-content: space-between;
  /* 按钮平均分布 */
  margin-bottom: 20px
}

.button-group .el-button {
  border-radius: 8px;
  padding: 12px 24px;
  transition: all 0.2s ease;
}

.group {
  display: flex;
  gap: 10px;
  /* Adjust the gap between buttons within the same group */
}

.group-gap {
  flex-grow: 1;
}

.return-button {
  position: absolute;
  top: 20px;
  right: 20px;
}

.el-table {
  width: 100%;
  margin-top: 20px;
  overflow: auto;
  /* 确保表格内容不会溢出 */
}


/* 使用深度选择器确保样式能够穿透到子组件 */
/* :deep(.el-table__row) {
  transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
} */

/* :deep(.el-table__row:hover) {
  background-color: #f0f9ff !important; */
/* 悬浮时的背景颜色 */
/* transform: scale(1.02); */
/* 放大 2% */
/* box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); */
/* 添加阴影效果 */
/* z-index: 10; */
/* 确保放大后的行不会被其他元素遮挡 */
/* } */

/* 修复放大后可能引起的布局问题 */
/* :deep(.el-table__row:hover .el-table__cell) { */
/* overflow: visible; */
/* 允许内容超出单元格 */
/* } */


.el-table th,
.el-table td {
  white-space: nowrap;
  /* 防止内容换行 */
  overflow: hidden;
  text-overflow: ellipsis;
  /* 显示省略号 */
}

.dialog-footer {
  text-align: right;
}

/* 确保对话框能够正常显示 */
.el-dialog {
  z-index: 10000;
  /* 确保对话框在最上层 */
}

.file-name-container {
  display: flex;
  align-items: center;
  gap: 8px;
  /* 图标和文件名之间的间距 */
}

.file-icon {
  width: 28px;
  height: 28px;
}

.file-name {
  flex: 1;
  white-space: nowrap;
  /* 防止文件名换行 */
  overflow: hidden;
  text-overflow: ellipsis;
  /* 显示省略号 */
}

.status-icon {
  display: flex;
  align-items: center;
}

.icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  /* 与文字的间距 */
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

  .file-name-container {
    flex-direction: column;
    /* 在小屏幕上将图标和文件名垂直排列 */
    align-items: start;
    /* 对齐方式 */
  }

  .file-icon {
    margin-bottom: 4px;
    /* 图标和文件名之间的间距 */
  }

  .button-group {
    flex-direction: column;
  }

  .button-group .el-button {
    width: 100%;
  }




}
</style>