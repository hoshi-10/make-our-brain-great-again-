<template>
  <el-card class="box" shadow="always">
    <h1 class="print-title">报价清单</h1>
    <el-form inline label-width="60px">
      <el-form-item label="数量">
        <el-input-number
          v-model="form.quantity"
          :min="1"
        />
      </el-form-item>

      <el-form-item label="单价">
        <el-input-number
          v-model="form.price"
          :min="0"
          :precision="2"
        />
      </el-form-item>

      <el-form-item label="尺寸">
        <el-input
          v-model="form.size"
          placeholder="如：A4 / 10×20"
        />
      </el-form-item>

      <el-form-item label="材料">
        <el-input
          v-model="form.material"
          placeholder="如：铜版纸"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="addItem">
          添加到清单
        </el-button>
      </el-form-item>
    </el-form>

    <!-- 清单表格 -->
    <el-table
      :data="list"
      style="width: 100%; margin-top: 20px"
      border
    >
      <el-table-column type="index" label="#" width="50" />
      <el-table-column prop="size" label="尺寸" />
      <el-table-column prop="material" label="材料" />
      <el-table-column prop="quantity" label="数量" />
      <el-table-column prop="price" label="单价" />
      <el-table-column prop="subtotal" label="小计 (￥)" />
    </el-table>

    <!-- 总价 -->
    <div class="total">
      <el-text size="large" type="danger">
        总价：￥{{ totalPrice }}
      </el-text>
    </div>

    <!-- 操作按钮 -->
    <div style="margin-top: 16px">
      <el-button type="success" @click="print">
        打印
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  quantity: null,
  price: null,
  size: '',
  material: ''
})

const list = ref([])

const addItem = () => {
  if (!form.quantity || !form.price) {
    ElMessage.warning('请填写数量和单价')
    return
  }

  list.value.push({
    quantity: form.quantity,
    price: form.price,
    size: form.size,
    material: form.material,
    subtotal: form.quantity * form.price
  })

  // 清空表单
  form.quantity = null
  form.price = null
  form.size = ''
  form.material = ''
}

const totalPrice = computed(() => {
  return list.value.reduce((sum, item) => sum + item.subtotal, 0)
})

const print = () => {
  window.print()
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
@media print {
  /* 隐藏表单和按钮 */
  .el-form,
  .el-button {
    display: none !important;
  }
}

</style>
