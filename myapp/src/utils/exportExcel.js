// src/utils/exportExcel.js
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'
import { ElMessage } from 'element-plus'

export async function exportExcel(list, totalPrice) {
  if (!list || list.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }

  const workbook = new ExcelJS.Workbook()
  const worksheet = workbook.addWorksheet('报价清单')

  // 表头
  worksheet.columns = [
    { header: '日期', key: 'date', width: 15 },
    { header: '内容 / 备注', key: 'content', width: 20 },
    { header: '尺寸', key: 'size', width: 15 },
    { header: '材料', key: 'material', width: 15 },
    { header: '数量', key: 'quantity', width: 10 },
    { header: '单价', key: 'price', width: 10 },
    { header: '小计', key: 'subtotal', width: 12 }
  ]

  // 数据行
  list.forEach(item => {
    worksheet.addRow({
      date: item.date,
      content: item.content,
      size: item.size,
      material: item.material,
      quantity: item.quantity,
      price: item.price,
      subtotal: item.subtotal
    })
  })

  // 空一行
  worksheet.addRow({})

  // 总价行
  worksheet.addRow({
    price: '总价',
    subtotal: totalPrice
  })

  try {
    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    saveAs(blob, `报价清单_${Date.now()}.xlsx`)
    ElMessage.success('Excel 导出成功')
  } catch (err) {
    ElMessage.error('Excel 导出失败')
  }
}
