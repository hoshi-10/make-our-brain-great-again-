<template>
  <div style="margin-top:16px">
    <el-button type="success" @click="handlePrint">打印</el-button>
    <el-button type="primary" @click="handleExportExcel">导出 Excel</el-button>
    <el-button type="primary" @click="handleExportWord">导出 Word</el-button>
  </div>
</template>

<script setup>
import { exportExcel } from '@/utils/exportExcel'
import { exportWord } from '@/utils/exportWord'

const props = defineProps({
  list: Array,
  total: Number
})

const handlePrint = () => window.print()

const handleExportExcel = () => {
  exportExcel(props.list, props.total)
}

const handleExportWord = () => {
  exportWord(props.list, props.total)
}
</script>
