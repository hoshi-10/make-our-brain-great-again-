<template>
  <div class="layout">
    <!-- 左侧固定 -->
    <aside class="sidebar">
        <h1 class="title">报价单结算管理系统</h1>
      <Sidebar />
    </aside>

    <!-- 右侧内容 -->
    <div class="main">
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 220px;
  background-color: #1f2d3d;
  color: #fff;
}

.main {
  flex: 1;
  background: #f5f7fa;
overflow:auto;
}

</style>
