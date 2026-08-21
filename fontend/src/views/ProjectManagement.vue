<template>
  <div class="ProjectManagement">
    <div class="header">
      <span class="title">项目库</span>
    <el-input v-model="searchQuery" placeholder="项目搜索" class="search-input">
    </el-input>
    </div>
    <div class="button-group">
      <el-button type="success" @click="openCreateDialog">新建项目（审批用户）</el-button>
      <el-button type="danger" @click="showDeleteDialog" style="margin-left: 10px;">删除项目（审批用户）</el-button>
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
      <div v-for="project in filteredProjects" :key="project.id" class="project-item">
        <el-checkbox v-model="project.selected" @change="toggleProjectSelection(project)"></el-checkbox>
        <div class="project-title">{{ project.title }}</div>
        <div class="project-description">{{ project.description }}</div>
        <div class="project-actions">
          <el-button type="primary" plain @click="viewDetails(project)">详情（审批用户）</el-button>
          <el-button type="primary" plain @click="enterProject(project)">进入</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
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
    const projects = ref([
       { id: 1, title: '项目一', description: '这是实验室的项目', members: [], selected: false },
       { id: 2, title: '项目二', description: '项目详细描述', members: [], selected: false },
       { id: 3, title: '项目三', description: '项目详细描述', members: [], selected: false },
       { id: 4, title: '项目四', description: '项目详细描述', members: [], selected: false },
       { id: 5, title: '项目五', description: '项目详细描述', members: [], selected: false },
       { id: 6, title: '项目六', description: '项目详细描述', members: [], selected: false },
      // 更多项目...
    ]);

    const selectedProjects = ref([]); // 用于存储选中的项目

    const filteredProjects = computed(() => {
      return projects.value.filter(project =>
        project.title.includes(searchQuery.value) ||
        project.description.includes(searchQuery.value)
      );
    });


    const openCreateDialog = () => {
      dialogVisible.value = true;
    };

    const handleCreateProject = () => {
      const newProjectItem = { ...newProject.value, id: Date.now(), selected: false };
      projects.value.push(newProjectItem);
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
      project.members.push({ id: newMemberId.value, role: role });
      newMemberId.value = ''; // 清空输入框
      }
    };

    const removeMember = (memberId) => {
  // 这里需要添加逻辑来从项目成员列表中移除成员
      selectedProject.value.members = selectedProject.value.members.filter(member => member.id !== memberId);
    };

    const saveDetails = () => {
  // 这里需要添加逻辑来保存项目详情
      detailsDialogVisible.value = false;
    };


    const enterProject = (project) => {
      console.log('进入项目:', project);
      // 使用router.push进行页面跳转
      router.push({ name: 'DocumentLibrary' });
    };

    return {
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
  display: flex;
  flex-direction: column;
}

.header {
  text-align: left;
  align-items: center; /* 垂直居中 */
  margin-bottom: 20px;
}

.title {
  margin-right: 5px; /* 间隔 */
  font-size: 28px; /* 标题字体大小 */
  font-weight: bold;
}

.search-input {
  flex-grow: 1; /* 搜索框占据剩余空间 */
  background-color: #f0f0f0; /* 背景颜色加深 */
  border: 1px solid #ccc; /* 边框颜色 */
  box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
  border-radius: 4px; /* 边框圆角 */
}

.button-group {
  display: flex;
  justify-content: space-between; /* 按钮平均分布 */
  margin-bottom: 20px;
}

.project-container {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 10px; /* 项目之间的间隔 */
  overflow-y: auto; /* 当内容过多时显示滚动条 */
  border: 1px solid #ccc; /* 容器边框 */
  padding: 10px; /* 容器内边距 */
}

.project-item {
  width: calc(33.333% - 10px); /* 每行三个项目，减去间隔 */
  box-sizing: border-box;
  border: 1px solid #ccc; /* 边框颜色 */
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #f0f0f0; /* 浅灰色背景 */
  font-weight: bold; /* 加粗文本 */
  margin-bottom: 10px; /* 项目之间的间隔 */
  border-radius: 4px; /* 边框圆角 */
}

.project-title {
  font-weight: bold;
  margin-bottom: 5px;
}

.project-description {
  width: 100%;
  height: 100px; /* 固定高度，形成正方形或矩形 */
  border: 1px solid #ccc;
  padding: 10px;
  box-sizing: border-box;
  margin-bottom: 10px;
  text-align: center; /* 使文本居中 */
}

.project-actions {
  display: flex;
  justify-content: space-between; /* 按钮平均分布 */
  width: 100%;
}

.project-actions button {
  flex: 1; /* 按钮占据相同空间 */
  margin: 0 5px; /* 按钮之间的间隔 */
}
</style>