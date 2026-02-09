<template>
  <el-card class="box" shadow="always">
    <h1 class="print-title">报价清单</h1>

    <!-- 表单 -->
    <QuoteForm @add="addItem" />

    <!-- 表格 -->
    <QuoteTable
      :list="list"
      @remove="removeItem"
    />

    <!-- 总价 -->
    <div class="total">
      <el-text size="large" type="danger">
        总价：￥{{ totalPrice }}
      </el-text>
    </div>

    <!-- 操作按钮 -->
    <QuoteActions
      :list="list"
      :total="totalPrice"
    />
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessageBox } from 'element-plus'

import QuoteForm from '@/components/QuoteForm.vue'
import QuoteTable from '@/components/QuoteTable.vue'
import QuoteActions from '@/components/QuoteActions.vue'

// ① 核心数据
const list = ref([])

// ② 派生数据
const totalPrice = computed(() => {
  return list.value.reduce((sum, item) => sum + item.subtotal, 0)
})

// ③ 业务调度（只改数据）
const addItem = (item) => {
  list.value.push(item)
}

const removeItem = (index) => {
  ElMessageBox.confirm(
    '确定删除这一行吗？',
    '提示',
    { type: 'warning' }
  ).then(() => {
    list.value.splice(index, 1)
  })
}
</script>

<style scoped>
.box {
  max-width: 900px;
  margin: 30px auto;
}

.total {
  margin-top: 20px;
  text-align: right;
  font-weight: bold;
}

@media print {
  .print-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
  }
}
</style>
