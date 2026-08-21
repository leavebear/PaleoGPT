<template>
  <div class="ProjectManagement">
    <div class="header">
      <span class="title">项目库</span>
      <svg t="1740116777201" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1436" width="28" height="28"><path d="M754.752 587.968h139.904L896 494.208l-101.312-115.84h-39.936v209.6z" fill="#1296db" p-id="1437"></path><path d="M404.48 177.6a17.088 17.088 0 0 0-13.056 6.08L177.6 437.376V832c0 9.408 7.68 17.088 17.088 17.088h544c9.408 0 17.024-7.68 17.024-17.088V194.688a17.088 17.088 0 0 0-17.024-17.088H404.48z m-52.16-26.88c12.928-15.424 32-24.32 52.16-24.32h334.208c37.696 0 68.224 30.592 68.224 68.288V832c0 37.76-30.528 68.288-68.224 68.288h-544c-37.76 0-68.288-30.592-68.288-68.288V418.624l225.92-267.968z" fill="#1296db" p-id="1438"></path><path d="M405.376 493.312a64 64 0 0 0-64 64v170.688a64 64 0 0 0 64 64H832a64 64 0 0 0 64-64V493.312H405.376z m66.432 54.4c-27.136 0-48.64 9.216-64.512 28.16-15.104 17.664-22.528 40.192-22.528 67.584 0 27.136 7.424 49.408 22.528 66.56 16.128 18.432 38.656 27.648 67.84 27.648 16.384 0 30.976-2.048 44.288-6.144a120.32 120.32 0 0 0 11.648-4.48c14.592-6.464 21.632-22.272 21.632-38.208v-12.864a39.168 39.168 0 0 0-39.168-39.168h-26.368a12.8 12.8 0 0 0 0 25.6h11.648c13.248 0 23.936 10.688 23.936 23.872 0 8.512-4.48 16.64-12.352 19.712a83.072 83.072 0 0 1-32 5.568c-22.208 0-38.592-6.144-49.088-18.432-9.728-11.52-14.592-28.16-14.592-49.664 0-22.528 5.376-39.68 16.384-51.968 9.984-11.776 23.552-17.408 40.704-17.408 13.824 0 25.088 2.816 33.536 8.704a39.232 39.232 0 0 1 12.416 14.72c3.2 6.4 9.088 11.648 16.256 11.648 9.344 0 16.64-8.512 13.44-17.344a62.528 62.528 0 0 0-20.096-28.48c-13.568-10.496-32-15.616-55.552-15.616z m131.264 0a19.712 19.712 0 0 0-14.08 5.376 17.92 17.92 0 0 0-5.632 13.824c0 5.632 1.792 10.24 5.632 14.08 3.84 3.584 8.448 5.376 14.08 5.376s10.24-1.792 14.08-5.376a18.752 18.752 0 0 0 5.888-14.08 18.88 18.88 0 0 0-5.632-13.824 20.352 20.352 0 0 0-14.336-5.376z m0 54.016a14.592 14.592 0 0 0-14.592 14.592v103.168a14.592 14.592 0 1 0 29.184 0V616.32a14.592 14.592 0 0 0-14.592-14.592z m75.648-40.704c6.144-6.656 15.36-9.728 27.136-9.728h15.872a12.288 12.288 0 1 1 0 24.576h-11.776c-3.84 0-6.656 1.024-8.704 3.072-2.048 2.048-2.816 5.12-2.816 9.472v6.528c0 3.712 3.008 6.784 6.72 6.784h15.168a11.904 11.904 0 0 1 0 23.808h-15.168a6.784 6.784 0 0 0-6.72 6.72v87.232a14.592 14.592 0 1 1-29.184 0V631.424a5.888 5.888 0 0 0-5.888-5.888h-11.648a11.904 11.904 0 0 1 0-23.808h11.648c3.2 0 5.888-2.688 5.888-5.888v-8.192c0-11.264 3.072-20.224 9.472-26.624z" fill="#1296db" p-id="1439"></path><path d="M404.672 406.72V197.824a32 32 0 0 0-56.192-20.864L167.808 385.728A32 32 0 0 0 192 438.656h180.672a32 32 0 0 0 32-31.936z" fill="#1296db" p-id="1440"></path></svg>
      <div class="search-container">
    <!-- SVG 图标 -->
    <svg t="1740117903957" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2296" width="32" height="32"><path d="M762.794667 702.805333A373.376 373.376 0 0 0 205.312 208 373.333333 373.333333 0 0 0 702.72 763.392l120.106667 120.106667a42.666667 42.666667 0 0 0 60.330666-60.330667l-120.362666-120.362667z m-215.04-409.898666a184.832 184.832 0 0 0-69.12-13.312 25.6 25.6 0 0 1-0.042667-51.2 234.965333 234.965333 0 0 1 166.997333 69.034666 235.434667 235.434667 0 0 1 65.28 208.64 25.6 25.6 0 0 1-50.432-9.088 184.277333 184.277333 0 0 0-51.072-163.328 183.808 183.808 0 0 0-61.568-40.746666z" fill="#1296db" p-id="2297"></path></svg>
    <!-- 搜索框 -->
    <el-input
      v-model="searchQuery"
      placeholder="项目搜索"
      class="search-input"
    ></el-input>
  </div>
    </div>
    <div class="button-group">
      <el-button type="success" plain @click="openCreateDialog">新建项目（审批用户）</el-button>
      <el-button type="danger"  plain @click="showDeleteDialog" style="margin-left: 10px;">删除项目（审批用户）</el-button>
    </div>

    <el-dialog
      title="新建项目"
      v-model="dialogVisible"
      width="30%"
    >
      <el-form :model="newProject">
      <el-form-item label="项目名称" :label-width="formLabelWidth">
        <el-input v-model="newProject.title" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="项目描述" :label-width="formLabelWidth">
        <el-input type="textarea" v-model="newProject.description" autocomplete="off"></el-input>
      </el-form-item>
      <!-- 添加成员部分 -->
      <el-form-item label="添加普通成员">
        <el-input v-model="newMemberId" placeholder="输入成员ID"></el-input>
        <el-button @click="addMember('普通')">添加</el-button>
      </el-form-item>
      <el-form-item label="添加审批成员">
        <el-input v-model="newMemberId" placeholder="输入成员ID"></el-input>
        <el-button @click="addMember('审批')">添加</el-button>
      </el-form-item>
      <!-- 成员列表 -->
      <el-table :data="newProject.members" style="width: 100%">
          <el-table-column prop="id" label="用户ID" width="180"></el-table-column>
          <el-table-column prop="role" label="权限" width="100"></el-table-column>
        </el-table>
    </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleCreateProject">确 定</el-button>
      </template>
    </el-dialog>

    <el-dialog
    title="项目详情"
    v-model="detailsDialogVisible"
    width="50%"
  >
    <el-form>
      <el-form-item label="项目名称">
        <el-input v-model="selectedProject.title" disabled></el-input>
      </el-form-item>
      <el-form-item label="项目描述">
        <el-input type="textarea" v-model="selectedProject.description" disabled></el-input>
      </el-form-item>
    </el-form>
    <!-- 添加成员部分 -->
    <el-form>
      <el-form-item label="添加普通成员">
        <el-input v-model="newMemberId" placeholder="输入成员ID"></el-input>
        <el-button @click="addMember('普通')">添加</el-button>
      </el-form-item>
      <el-form-item label="添加审批成员">
        <el-input v-model="newMemberId" placeholder="输入成员ID"></el-input>
        <el-button @click="addMember('审批')">添加</el-button>
      </el-form-item>
    </el-form>
    <!-- 成员列表 -->
    <el-table :data="selectedProject.members" style="width: 100%">
      <el-table-column prop="id" label="用户ID" width="180"></el-table-column>
      <el-table-column prop="name" label="用户姓名" width="180"></el-table-column>
      <el-table-column prop="role" label="权限" width="100"></el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="scope">
          <el-button @click="removeMember(scope.row.id)" type="text" size="small">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <el-button @click="detailsDialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="saveDetails">保存详情</el-button>
    </template>
  </el-dialog>
    <!-- 删除确认弹窗 -->
    <el-dialog
      title="删除项目"
      v-model="deleteDialogVisible"
      width="30%"
    >
      <span>确认删除选中的项目吗？</span>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmDeleteProjects">确 定</el-button>
      </template>
    </el-dialog>

    <div class="project-container" ref="projectContainer">
      <div v-for="project in paginatedProjects" :key="project.id" class="project-item">
        <el-checkbox v-model="project.selected" @change="toggleProjectSelection(project)"></el-checkbox>
        <el-collapse v-model="project.active" class="project-collapse">
          <el-collapse-item :name="project.id" :title="project.title" class="project-collapse-item">
            <template #title>
              <div class="project-title">
                <span>{{ project.title }}</span>
                <!-- 在这里插入图标 -->
                <svg t="1740383576807" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1326" width="28" height="28"><path d="M287 962h530.35714248c45 0 80.35714248-35.35714248 80.35714336-80.35714248V576.28571416H158.42857168v257.14285752c0 70.71428584 57.85714248 128.57142832 128.57142832 128.57142832z" fill="#BAE7FF" p-id="1327"></path><path d="M647 962H238.78571416C193.78571416 962 158.42857168 926.64285752 158.42857168 881.64285752v-739.28571504C158.42857168 97.35714248 193.78571416 62 238.78571416 62h575.35714336C862.35714248 62 897.71428584 97.35714248 897.71428584 142.35714248v572.14285752L647 962z" fill="#69C0FF" p-id="1328"></path><path d="M650.21428584 962v-186.42857168c0-32.14285752 25.71428584-61.07142832 61.07142832-61.07142832H897.71428584L650.21428584 962z" fill="#1890FF" p-id="1329"></path><path d="M319.14285752 640.57142832h417.85714248c19.28571416 0 32.14285752-12.85714248 32.14285752-32.14285664s-12.85714248-32.14285752-32.14285752-32.14285752H319.14285752c-19.28571416 0-32.14285752 12.85714248-32.14285752 32.14285752s12.85714248 32.14285752 32.14285752 32.14285664zM576.28571416 479.85714248h160.71428584c19.28571416 0 32.14285752-12.85714248 32.14285752-32.14285664s-12.85714248-32.14285752-32.14285752-32.14285752h-160.71428584c-19.28571416 0-32.14285752 12.85714248-32.14285664 32.14285752s12.85714248 32.14285752 32.14285664 32.14285664z" fill="#BAE7FF" p-id="1330"></path><path d="M319.14285752 479.85714248h128.57142832c19.28571416 0 32.14285752-12.85714248 32.14285664-32.14285664V287c0-19.28571416-12.85714248-32.14285752-32.14285664-32.14285752H319.14285752c-19.28571416 0-32.14285752 12.85714248-32.14285752 32.14285752v160.71428584c0 19.28571416 12.85714248 32.14285752 32.14285752 32.14285664z" fill="#BAE7FF" p-id="1331"></path><path d="M576.28571416 319.14285752h160.71428584c19.28571416 0 32.14285752-12.85714248 32.14285752-32.14285752s-12.85714248-32.14285752-32.14285752-32.14285752h-160.71428584c-19.28571416 0-32.14285752 12.85714248-32.14285664 32.14285752s12.85714248 32.14285752 32.14285664 32.14285752z" fill="#BAE7FF" p-id="1332"></path></svg>
              </div>
            </template>
            <div class="project-description">{{ project.description }}</div>
          </el-collapse-item>
        </el-collapse>
        <div class="project-actions">
          <el-button type="primary" plain @click="viewDetails(project)">详情（审批用户）</el-button>
          <el-button type="primary" plain @click="enterProject(project)">进入</el-button>
        </div>
      </div>
    </div>
    <!-- 分页组件 -->
    <el-pagination
      class="pagination"
      background
      layout="prev, pager, next"
      :total="filteredProjects.length"
      :page-size="pageSize"
      v-model:current-page="currentPage"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script>
import { ref, computed ,onMounted} from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { Search } from '@element-plus/icons-vue'; // 引入图标
export default {
  setup() {
    const router = useRouter(); // 使用useRouter
    const searchQuery = ref('');
    const dialogVisible = ref(false);
    const deleteDialogVisible = ref(false);
    const newProject = ref({ title: '', description: '', members: [] }); // 初始化 members 为空数组
    const detailsDialogVisible = ref(false);
    const newMemberId = ref('');
    const selectedProject = ref({});
    const projects = ref([]);

    // 初始化项目数据
    const initProjects = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/project/init");
        if (response.data.status_code === 0) {
          projects.value = response.data.data.map(project => ({
            id: project.projectId,
            title: project.projectName,
            description: project.projectDescription,
            members: [
              ...project.normalMembers.map(member => ({ id: member.id, name: member.name, role: '普通' })),
              ...project.approvalMembers.map(member => ({ id: member.id, name: member.name, role: '审批' }))
            ],
            selected: false
          }));
        } else {
          console.error('项目初始化失败:', response.data.status_msg);
        }
      } catch (error) {
        console.error('项目初始化失败:', error);
      }
    };
    // 页面加载时调用初始化项目数据
    onMounted(initProjects);
//     const projects = ref([
//       { id: 1, title: '古海洋生物多样性生态重建', description: '着重研究古代海洋生态系统中的各种生物，如三叶虫、海百合、古鱼类等。通过化石分析，重建古代海洋生态系统的结构和功能，了解生物之间的相互关系。', members: [], selected: false },
//       { id: 2, title: '古生物微观结构研究', description: '专注于古生物的微观结构，如细胞结构、组织结构等。利用先进的显微技术，如电子显微镜，观察和分析化石的微观特征，为理解古生物的生理功能和演化提供新的视角。', members: [], selected: false },
//       { id: 3, title: '古生物与现代生物关系研究', description: '探讨古生物与现代生物之间的进化联系，通过比较解剖学、分子生物学等方法，研究它们之间的亲缘关系，揭示生物进化的连续性和阶段性。', members: [], selected: false },
//       { id: 4, title: '古生物化石保护与修复工程', description: '旨在保护和修复珍贵的古生物化石，防止化石因自然侵蚀、人为破坏等原因而损坏。项目可以包括化石的采集规范、保存技术、修复工艺等方面的研究和实践。', members: [], selected: false },
//       { id: 5, title: '古生物化石资源普查与保护', description: '对某一地区或全国范围内的古生物化石资源进行全面普查，摸清资源家底。然后根据普查结果，制定科学合理的保护规划，确保化石资源得到有效保护。', members: [], selected: false },
//       { id: 6, title: '古生物科普绘本创作与推广', description: '创作适合儿童和青少年的古生物科普绘本，以生动有趣的方式介绍古生物的知识。然后通过学校、图书馆、书店等渠道进行推广，激发青少年对古生物的兴趣和探索欲望。', members: [], selected: false },
      
//       // 更多项目...
//     ]);

//     const users = ref([
//   { id: '1', name: '张三' },
//   { id: '2', name: '李四' },
//   { id: '3', name: '王五' },
//   // 更多用户...
// ]);

    // TODO: 初始化项目库接口
    // axios.post('http://localhost:17300/api/project/init', loginData, {
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // }).then(response => {
    //     // 处理响应
    //     return response;
    // }).catch(error => {
    //     // 处理错误
    //     console.error('Error during login:', error);
    //     throw error;
    // });


      axios.get("http://localhost:17300/api/project/init")
      .then(function (response) {
          // 请求成功时执行的代码
          console.log('Success:', response.data);
          response.data.data.forEach(item => {
            let newProjectItem = { title: item.proName, id: item.proID, description: item.proDes, members: item.members, selected: false };
            // console.log("test1:"+newProjectItem)
            projects.value.push(newProjectItem);
          });
          
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


    const selectedProjects = ref([]); // 用于存储选中的项目

    const filteredProjects = computed(() =>
      projects.value.filter((project) =>
        project.title.includes(searchQuery.value) ||
        project.description.includes(searchQuery.value)
      )
    );

    const currentPage = ref(1); // 当前页码
    const pageSize = ref(6); // 每页显示的项目数量

    // 计算当前页显示的项目
    const paginatedProjects = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value;
      const end = start + pageSize.value;
      return filteredProjects.value.slice(start, end);
    });

    // 处理页码切换
    const handlePageChange = (newPage) => {
      currentPage.value = newPage;
    };


    const openCreateDialog = () => {
      dialogVisible.value = true;
    };

    const handleCreateProject = () => {
      const newProjectItem = { ...newProject.value, id: Date.now(), selected: false };
      
      console.log("test:" + JSON.stringify(newProjectItem, null, 2))
      // console.log("test:" + newProjectItem.title)

      

      const reqData = {
        "proName": newProjectItem.title,
        "proDes": newProjectItem.description,
        "members": newProjectItem.members
      }

      const headers = {
        'Content-Type': 'application/json', // 告诉服务器我们发送的是JSON格式的数据
        'Accept': 'application/json', // 告诉服务器我们期望接收JSON格式的响应
      }

      axios.post("http://localhost:17300/api/project/create", reqData, { headers: headers })
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

      projects.value.push((newProjectItem));
      newProject.value = { title: '', description: '', members: [] }; // 清空输入，包括成员列表

      

      dialogVisible.value = false; // 关闭对话框
    };

    const toggleProjectSelection = (project) => {
      const index = selectedProjects.value.indexOf(project.id);
      if (index > -1) {
        selectedProjects.value.splice(index, 1); // 如果已经选中，移除 id
      } else {
        selectedProjects.value.push(project.id); // 如果未选中，添加 id
      }
    };

    const confirmDeleteProjects = () => {
      projects.value = projects.value.filter(project => !selectedProjects.value.includes(project.id));
      selectedProjects.value = []; // 清空选中的项目 id
      deleteDialogVisible.value = false; // 关闭对话框
    };

    const showDeleteDialog = () => {
      if (selectedProjects.value.length === 0) {
        this.$message.error('请先选择要删除的项目');
        return;
      }
      deleteDialogVisible.value = true;
    };


    const viewDetails = (project) => {
      detailsDialogVisible.value = true;
      selectedProject.value = project; // 确保这里的 project 对象包含 members 数组
    };

    const addMember = (role) => {
      if (newMemberId.value) {
        const project = dialogVisible.value ? newProject.value : selectedProject.value;
        if (!project.members) {
          project.members = [];
        }

        // 查找用户姓名
    const user = users.value.find((u) => u.id === newMemberId.value);
    if (user) {
      project.members.push({ id: newMemberId.value, name: user.name, role: role });
    } else {
      console.warn('用户ID不存在:', newMemberId.value);
    }
        const reqData = {
          "accountID": newMemberId.value,
        }
        const headers = {
          'Content-Type': 'application/json', // 告诉服务器我们发送的是JSON格式的数据
          'Accept': 'application/json', // 告诉服务器我们期望接收JSON格式的响应
        };
        axios.post("http://localhost:17300/api/project/addMem", reqData, { headers: headers })
        .then(function (response) {
            // 请求成功时执行的代码
            console.log('Success:', response.data);
            project.members.push({ accountID: reqData.accountID, accountName: response.data.data.memName, auth: auth });
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

        // project.members.push({ id: newMemberId.value, role: role });
        newMemberId.value = ''; // 清空输入框
      }
    };


    const removeMember = (memberId) => {
      // 这里需要添加逻辑来从项目成员列表中移除成员
      selectedProject.value.members = selectedProject.value.members.filter(member => member.id !== memberId);
    };

    //保存详情
    const saveDetails = () => {
      // console.log(selectedProject.value)
      const reqData = {
        "proID": selectedProject.value.id,
        "proName": selectedProject.value.title,
        "proDes": selectedProject.value.description,
        "members": selectedProject.value.members
      }

        const headers = {
          'Content-Type': 'application/json', // 告诉服务器我们发送的是JSON格式的数据
          'Accept': 'application/json', // 告诉服务器我们期望接收JSON格式的响应
        };
        axios.post("http://localhost:17300/api/project/saveDetailInfo", reqData, { headers: headers })
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

      // 这里需要添加逻辑来保存项目详情
      detailsDialogVisible.value = false;
    };


    const enterProject = (project) => {
      console.log('进入项目:', project);
      // 使用router.push进行页面跳转
      router.push({ name: 'DocumentLibrary' });
    };

    return {
      paginatedProjects,
      currentPage,
      pageSize,
      handlePageChange,
      searchQuery,
      projects,
      filteredProjects,
      detailsDialogVisible,
      newMemberId,
      addMember,
      removeMember,
      selectedProject,
      saveDetails,
      dialogVisible,
      newProject,
      openCreateDialog,
      handleCreateProject,
      deleteDialogVisible,
      selectedProjects,
      showDeleteDialog,
      toggleProjectSelection,
      confirmDeleteProjects,
      viewDetails,
      enterProject,
    };
  },
};
</script>

<style scoped>
.ProjectManagement {
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
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
  background: #e8fafe; /* 更深的背景颜色 */
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.05);
}

.search-container .icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

/* 按钮组优化 */
.button-group {
  display: flex;
  justify-content: space-between; /* 按钮平均分布 */
  margin-bottom: 20px
}

.button-group .el-button {
  border-radius: 8px;
  padding: 12px 24px;
  transition: all 0.2s ease;
}

/* 项目容器优化 */
.project-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.project-item {
  position: relative;
  padding: 20px;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  transition: all 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
  background-color: #e2f0ff; /* 添加浅蓝色背景 */
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease, background-color 0.3s ease; /* 平滑过渡效果 */
}

/* 复选框优化 */
.project-item .el-checkbox {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1;
  border-color: #d1eaff; /* 边框颜色也稍微加深 */
}


/* 折叠面板优化 */
.project-collapse-item :deep(.el-collapse-item__header) {
  font-weight: 500;
  font-size: 16px;
  padding: 0;
  border: none;
  background: transparent !important;
}

.project-collapse-item :deep(.el-collapse-item__content) {
  padding: 12px 0 0;
  color: #64748b;
  line-height: 1.5;
}

/* 操作按钮优化 */
.project-actions {
  margin-top: auto;
  display: flex;
  gap: 8px;
}

.project-actions .el-button {
  flex: 1;
  border-radius: 8px;
  padding: 8px 12px;
}

.project-title {
  display: flex;
  align-items: center;
  gap: 8px; /* 图标和文字之间的间距 */
}

.project-title span {
  font-weight: 500;
  font-size: 16px;
  color: #333;
}

.project-icon {
  width: 24px; /* 图标的大小 */
  height: 24px;
  fill: currentColor; /* 使用当前颜色，方便统一管理 */
}

/* 分页优化 */
.pagination {
  margin-top: 24px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  justify-content: center;
}

/* 对话框优化 */
:deep(.el-dialog) {
  border-radius: 12px !important;
}

:deep(.el-dialog__header) {
  border-bottom: 1px solid #e2e8f0;
  margin-right: 0;
}

:deep(.el-form-item__label) {
  color: #475569;
  font-weight: 500;
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
  
  .project-container {
    grid-template-columns: 1fr;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .button-group .el-button {
    width: 100%;
  }
}
</style>