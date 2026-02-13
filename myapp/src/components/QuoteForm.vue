<template>
  <!-- 新增按钮 -->
  <el-button
    type="primary"
    @click="toggleForm"
    style="margin-bottom: 20px"
  >
    {{ showForm ? '收起填写' : '新增报价' }}

  </el-button>
<el-card class="box-card" shadow="never" style="margin-bottom:20px;">
  <el-form inline label-width="70px">

  <el-input v-model="props.quoteInfo.handler" placeholder="请填写经办人" />
  <el-input v-model="props.quoteInfo.remark" placeholder="请填写备注" />


  </el-form>
</el-card>

  <!-- 表单 -->
  <el-card v-show="showForm" shadow="never">
    <el-form :model="form" label-width="60px">
      <el-row :gutter="20">

        <el-col :span="12">
          <el-form-item label="日期">
            <el-date-picker v-model="form.date" type="date"
  value-format="YYYY-MM-DD"
  format="YYYY-MM-DD"
  style="width: 100%"/>

          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="内容">
            <el-input v-model="form.content" />
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
            <el-input v-model="form.size" />
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="材料">
            <el-input v-model="form.material" />
          </el-form-item>
        </el-col>

      </el-row>

      <el-form-item>
        <el-button type="success" @click="submit">
          添加到清单
        </el-button>
      </el-form-item>

    </el-form>
  </el-card>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
const props = defineProps({
  quoteInfo: Object  // 接收 Home 的整单信息
})

const emit = defineEmits(['add'])

const showForm = ref(false)

const form = reactive({
  date: '',
  content: '',
  quantity: null,
  price: null,
  size: '',
  material: ''
})

const toggleForm = () => {
  showForm.value = !showForm.value
}

const submit = () => {
  if (!form.quantity || !form.price || !form.material) {
    ElMessage.warning('请填写完整信息')
    return
  }

  emit('add', {
    ...form,
    subtotal: form.quantity * form.price
  })

  // 只清空明细字段
  form.date = ''
  form.content = ''
  form.quantity = null
  form.price = null
  form.size = ''
  form.material = ''

  showForm.value = false
}
</script>

