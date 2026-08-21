<script setup>
import avatar from "@/assets/default.png";
</script>

<template>
  <!-- element-plus中的容器 -->
  <el-container class="layout-container">
    <!-- 左侧菜单 -->
    <el-aside width="15%">
      <div class="el-aside__logo"></div>
      <!-- element-plus里的菜单标签 -->
      <el-menu active-text-color="#000000" background-color="rgba(195, 195, 192, 0.001)"  text-color="rgba(0, 0, 0, 1)"  style="font-weight: 450;" router>
        <el-menu-item class="project-menu" index="/project" style="margin-bottom: 8px;">
          <el-icon>
            <Management />
          </el-icon>
          <span>项目库</span>
        </el-menu-item>
        <el-sub-menu index="2">
          <template #title>
            <el-icon>
              <UserFilled />
            </el-icon>
            <span>工具库</span>
          </template>
          
          <el-menu-item index="/conversation">
            <el-icon>
              <User />
            </el-icon>
            <span>地学领域对话问答</span>
          </el-menu-item>
          
          <!-- <el-menu-item index="">
            <el-icon>
              <Crop />
            </el-icon>
            <span>分歧时间树构建</span>
          </el-menu-item> -->

          <el-menu-item index="/tool/table">
            <el-icon>
              <EditPen />
            </el-icon>
            <span>表格抽取修正</span>
          </el-menu-item>
          <el-menu-item index="/tool/picture">
            <el-icon>
              <EditPen />
            </el-icon>
            <span>图片抽取修正</span>
          </el-menu-item>
          <el-menu-item index="/tool/entity">
            <el-icon>
              <EditPen />
            </el-icon>
            <span>实体抽取修正</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <!-- 右侧主区域 -->
    <el-container>
      <!-- 头部区域 -->
      <el-header>
        <!-- <div>PaleoGPT:<strong>XX</strong></div> -->
        <div class="header-left">
        <img src="@/assets/paleo-gpt-logo2.png" alt="Paleo GPT Logo" class="logo-image">
        <span class="logo-text">PaleoGpt Chat</span>
      </div>
        <!-- 下拉菜单 -->
        <el-dropdown placement="bottom-end">
          <span class="el-dropdown__box">
            <!-- 头像avatar -->
            <el-avatar :src="avatar" />
            <el-icon>
              <CaretBottom />
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile" :icon="User"
                >基本资料</el-dropdown-item
              >
              <el-dropdown-item command="avatar" :icon="Crop"
                >更换头像</el-dropdown-item
              >
              <el-dropdown-item command="password" :icon="EditPen"
                >重置密码</el-dropdown-item
              >
              <el-dropdown-item command="logout" :icon="SwitchButton"
                >退出登录</el-dropdown-item
              >
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <!-- 中间区域 -->
      <el-main  class="main-background" style="padding-top: 0%;">
        <!-- <div style="width: 1290px; height: 570px;border: 1px solid red;">
                    内容展示区
                </div> -->
        <router-view></router-view>
      </el-main>
      <!-- 底部区域 -->
      <el-footer  class="main-background">PaleoGPT @2024 Created by </el-footer>
    </el-container>
  </el-container>
</template>

<style lang="scss" scoped>
/* 定义字体 */
@font-face {
      font-family: "阿里妈妈灵动体 VF Thin";
      src: url("//at.alicdn.com/wf/webfont/BJzY442fthaR/a2svAS80eBge.woff2") format("woff2"),
           url("//at.alicdn.com/wf/webfont/BJzY442fthaR/Q31HBDiVMMNh.woff") format("woff");
      font-display: swap;
    }

.header-left {
    flex-shrink: 0; // 防止logo被压缩
    .logo-text {
      font-family: "阿里妈妈灵动体 VF Thin", sans-serif; /* 使用自定义字体，同时提供备用字体 */
      font-size: 25px;
      font-weight: 600;
      color: #171717;
      cursor: pointer;
      user-select: none;
      white-space: nowrap; // 防止文字换行
      margin-bottom: 25px;
    }

    .logo-image {
      width: 50px; // logo宽度
      height: 50px; // logo高度
      margin-right: 8px; // logo右侧间距
    }
  }


.project-menu ,
.el-sub-menu{
  border: 3px solid #e2e8f0;
  border-radius: 12px;
  box-shadow: 0 2px 8px 2px rgba(0, 0, 0, 0.05);
}

.el-menu-item {
  border-radius: 12px;
}

.el-menu .el-menu-item.is-active {
  border-radius: 12px;
  background-color: #409EFF !important; /* 设置你想要的背景色 */
}

.layout-container {
  height: 100vh;
  //右侧主题背景
  .main-background{
    background-color: hsl(0, 0%, 100%); 
  }
  .el-aside {
    //rgb(227, 225, 175)
    background-color: #ecf5ffbe;

    &__logo {
      height: 120px;
      background: url("@/assets/logo.png") no-repeat center / 120px auto;
    }

    .el-menu {
      border-right: none;
    }
  }

  .el-header {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .el-dropdown__box {
      display: flex;
      align-items: center;

      .el-icon {
        color: #999;
        margin-left: 10px;
      }

      &:active,
      &:focus {
        outline: none;
      }
    }
  }

  .el-footer {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: #666;
  }
}
</style>
