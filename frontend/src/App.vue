<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="logo">
          <i class="el-icon-s-data"></i>
          <span>空气质量数据可视化分析平台</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="nav-menu"
          mode="horizontal"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#409EFF"
          router
        >
          <el-menu-item index="/dashboard">
            <i class="el-icon-s-home"></i>
            <span slot="title">数据概览</span>
          </el-menu-item>
          <el-menu-item index="/ranking">
            <i class="el-icon-s-marketing"></i>
            <span slot="title">城市排名</span>
          </el-menu-item>
          <el-menu-item index="/history">
            <i class="el-icon-date"></i>
            <span slot="title">历史查询</span>
          </el-menu-item>
          <el-menu-item index="/compare">
            <i class="el-icon-s-operation"></i>
            <span slot="title">数据对比</span>
          </el-menu-item>
          <el-menu-item index="/warning">
            <i class="el-icon-warning"></i>
            <span slot="title">预警信息</span>
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
      <el-footer class="footer">
        <p>空气质量数据可视化分析平台 © 2026 中国地质大学（北京）</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f0f2f5;
}

#app {
  min-height: 100vh;
}

.header {
  background-color: #001529;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  margin-right: 40px;
  display: flex;
  align-items: center;
}

.logo i {
  font-size: 28px;
  margin-right: 10px;
  color: #409EFF;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
}

.nav-menu .el-menu-item {
  font-size: 14px;
}

.nav-menu .el-menu-item i {
  margin-right: 5px;
}

.main-content {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.footer {
  background-color: #001529;
  color: #fff;
  text-align: center;
  line-height: 60px;
}

.card-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
  border-left: 4px solid #409EFF;
  padding-left: 12px;
}
</style>
