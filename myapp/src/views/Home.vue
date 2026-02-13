<template>
  <el-card class="box" shadow="always">
    <h1 class="print-title">报价清单</h1>

    <div class="print-info">
  <p>经办人：{{ quoteInfo.handler }}</p>
  <p>备注：{{ quoteInfo.remark }}</p>
</div>
<QuoteForm 
  :quoteInfo="quoteInfo"
  @add="addItem"
/>

    <!-- 表单 -->
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
import { reactive, ref, computed } from 'vue'
import { ElMessageBox } from 'element-plus'

import QuoteForm from '@/components/QuoteForm.vue'
import QuoteTable from '@/components/QuoteTable.vue'
import QuoteActions from '@/components/QuoteActions.vue'


const quoteInfo= reactive({
  handler: '',
  remark: ''
})

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

/* 打印样式优化 */
@media print {
  @page {
    size: A4;
    margin: 2cm; /* 设置A4纸边距，更像正式单据 */
  }

  body {
    margin: 0;
    font-family: "Microsoft YaHei", "SimSun", sans-serif; /* 打印友好的字体 */
  }

  /* 隐藏所有不需要打印的元素 */
  .el-aside,
  .el-button,
  .no-print,
  .el-card__header,
  .el-card__body > :first-child {
    display: none !important;
  }

  /* 主容器样式 */
  .box {
    margin: 0;
    width: 100%;
    box-shadow: none !important;
    border: none !important;
  }

  /* 打印标题样式 */
  .print-title {
    display: block !important;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 30px;
    color: #000;
  }

  /* 表格样式重写，确保打印清晰 */
  .el-table {
    width: 100% !important;
    border-collapse: collapse !important;
    page-break-inside: avoid; /* 避免表格被分页切断 */
  }

  .el-table th,
  .el-table td {
    border: 1px solid #ccc !important;
    padding: 8px 12px !important;
    text-align: center !important;
    font-size: 12px !important;
    color: #000 !important;
    background: #fff !important;
  }

  .el-table th {
    background-color: #f5f5f5 !important;
    font-weight: bold;
  }

  /* 总价样式 */
  .total {
    margin-top: 20px;
    text-align: right;
    font-size: 16px;
    font-weight: bold;
    color: #000;
  }

  /* 可选：添加打印页脚 */
  .print-footer {
    display: block !important;
    margin-top: 30px;
    text-align: right;
    font-size: 12px;
    color: #666;
  }
}
</style>