<template>
<el-table :data="list" border style="margin-top:20px">
<el-table-column type="index" width="50" />
<el-table-column prop="date" label="日期" />
<el-table-column prop="content" label="内容" />
<el-table-column prop="size" label="尺寸" />
<el-table-column prop="material" label="材料" />
<el-table-column prop="quantity" label="数量" />
<el-table-column prop="price" label="单价" />
<el-table-column prop="subtotal" label="小计" />
<el-table-column label="操作">
<template #default="scope">
<el-button size="small" type="danger" class="no-print" @click="$emit('remove', scope.$index)">删除</el-button>
</template>
</el-table-column>
</el-table>
</template>


<script setup>
defineProps({ list: Array })
</script>