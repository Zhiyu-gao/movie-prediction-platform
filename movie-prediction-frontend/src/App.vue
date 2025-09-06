<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-header style="background-color: #409EFF; color: white;">
        <div class="logo">电影类型预测平台</div>
        <el-menu mode="horizontal" :default-active="activeMenu" @select="handleMenuSelect" router style="background-color: transparent; border-bottom: none;">
          <el-menu-item index="/" style="color: white;">可视化分析</el-menu-item>
          <el-menu-item index="/movies" style="color: white;">电影管理</el-menu-item>
          <el-menu-item index="/prediction" style="color: white;">类型预测</el-menu-item>
        </el-menu>
      </el-header>
      <el-container>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
      <el-footer style="background-color: #f5f5f5; text-align: center; padding: 20px;">© 2025 电影类型预测平台</el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 根据当前路由计算激活的菜单项
const activeMenu = computed(() => {
  return route.path
})

const handleMenuSelect = (index) => {
  // 路由会自动处理，这里可以添加其他逻辑
  console.log('导航到:', index)
}
</script>

<style scoped>
.logo {
  float: left;
  color: white;
  font-size: 24px;
  line-height: 60px;
  padding: 0 20px;
}

:deep(.el-menu--horizontal .el-menu-item) {
  color: white !important;
}

:deep(.el-menu--horizontal .el-menu-item.is-active) {
  color: #ffd04b !important;
  background-color: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-menu--horizontal .el-menu-item:hover) {
  color: #ffd04b !important;
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>    