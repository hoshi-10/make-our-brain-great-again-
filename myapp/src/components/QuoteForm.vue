<template>
<el-form
  :model="form"
  label-width="60px"
>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-form-item label="日期">
        <el-date-picker v-model="form.date" style="width: 100%" />
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item label="内容">
        <el-input v-model="form.content" placeholder="内容 / 备注" />
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item label="数量">
        <el-input-number v-model="form.quantity" style="width: 100%" />
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item label="单价">
        <el-input-number v-model="form.price" style="width: 100%" />
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item label="尺寸">
        <el-input v-model="form.size" placeholder="如：A4 / 10x20" />
      </el-form-item>
    </el-col>

    <el-col :span="12">
      <el-form-item label="材料">
        <el-input v-model="form.material" placeholder="如：铜版纸" />
      </el-form-item>
    </el-col>
  </el-row>
</el-form>



<el-form-item>
<el-button type="primary" @click="submit">添加到清单</el-button>
</el-form-item>
</template>


<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'


const emit = defineEmits(['add'])


const form = reactive({
date: '',
content: '',
quantity: null,
price: null,
size: '',
material: ''
})


const submit = () => {
if (!form.quantity || !form.price || !form.material) {
ElMessage.warning('请填写完整信息')
return
}


emit('add', {
...form,
subtotal: form.quantity * form.price
})


Object.keys(form).forEach(k => form[k] = '')
}
</script>