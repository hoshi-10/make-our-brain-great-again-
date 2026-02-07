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
    <el-table-column label="操作" width="100">
    <template #default="scope">
      <el-button
        type="danger"
        size="small"
        @click="removeItem(scope.$index)"
      >
        删除
      </el-button>
    </template>
  </el-table-column>
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
      <el-button type="primary" @click="exportToExcel">
  导出 Excel
</el-button>
<el-button type="primary" @click="exportWord">
  导出 Word
</el-button>
    </div>
  </el-card>
  
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'
import { Document, Packer, Paragraph, Table, TableRow, TableCell } from 'docx'

const exportWord = async () => {
  const rows = list.value.map(item =>
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph(item.size || '')] }),
        new TableCell({ children: [new Paragraph(item.material)] }),
        new TableCell({ children: [new Paragraph(item.quantity.toString())] }),
        new TableCell({ children: [new Paragraph(item.price.toString())] }),
        new TableCell({ children: [new Paragraph(item.subtotal.toString())] })
      ]
    })
  )

  const table = new Table({
    rows: [
      new TableRow({
        children: ['尺寸', '材料', '数量', '单价', '小计'].map(
          text => new TableCell({ children: [new Paragraph(text)] })
        )
      }),
      ...rows
    ]
  })

  const doc = new Document({
    sections: [{
      children: [
        new Paragraph('报价清单'),
        table
      ]
    }]
  })

  const blob = await Packer.toBlob(doc)
  saveAs(blob, '报价清单.docx')
}


const exportToExcel = () => {
  if (list.value.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }
  // 1. 创建工作簿和工作表
  const workbook = new ExcelJS.Workbook()
  const worksheet = workbook.addWorksheet('报价清单')

  // 2. 设置表头
  worksheet.columns = [
    { header: '尺寸', key: 'size', width: 15 },
    { header: '材料', key: 'material', width: 15 },
    { header: '数量', key: 'quantity', width: 10 },
    { header: '单价', key: 'price', width: 10 },
    { header: '小计', key: 'subtotal', width: 10 }
  ]

  // 3. 添加数据行
  list.value.forEach(item => {
    worksheet.addRow({
      size: item.size,
      material: item.material,
      quantity: item.quantity,
      price: item.price,
      subtotal: item.subtotal
    })
  })

  // 4. 添加总价行
  worksheet.addRow({
    size: '',
    material: '',
    quantity: '',
    price: '总价',
    subtotal: totalPrice.value
  })

  // 5. 生成并下载文件
  workbook.xlsx.writeBuffer().then(buffer => {
    const blob = new Blob([buffer], { 
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    })
    saveAs(blob, `报价清单_${new Date().getTime()}.xlsx`)
    ElMessage.success('Excel导出成功')
  }).catch(err => {
    ElMessage.error('Excel导出失败：' + err.message)
  })
}
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
if(!form.material){
  ElMessage.warning('请填写材料')
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

const removeItem=(index)=>{
  ElMessageBox.confirm(
'确定删除这一行吗？',
'提示',{
  type:'warning'
}
  ).then(()=>{
list.value.splice(index,1)
  })
}
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
