<template>
  <div class="menu">
    

    <div class="item" @click="$router.push('/home')">
      报价清单
    </div>
  </div>
</template>

<style scoped>
.menu {
  color: #fff;
}

.logo {
  padding: 20px;
  font-size: 18px;
  font-weight: bold;
}

.item {
  padding: 12px 20px;
  cursor: pointer;
}

.item:hover {
  background: rgba(255,255,255,0.1);
}
</style>
