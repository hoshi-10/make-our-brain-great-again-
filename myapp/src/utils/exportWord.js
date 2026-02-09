// src/utils/exportWord.js
import { Document, Packer, Paragraph, Table, TableRow, TableCell } from 'docx'
import { saveAs } from 'file-saver'
import { ElMessage } from 'element-plus'

export async function exportWord(list, totalPrice) {
  if (!list || list.length === 0) {
    ElMessage.warning('暂无数据可导出')
    return
  }

  // 表头
  const headerRow = new TableRow({
    children: [
      '日期',
      '内容 / 备注',
      '尺寸',
      '材料',
      '数量',
      '单价',
      '小计'
    ].map(text =>
      new TableCell({
        children: [new Paragraph(text)]
      })
    )
  })

  // 数据行
  const dataRows = list.map(item =>
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph(item.date || '')] }),
        new TableCell({ children: [new Paragraph(item.content || '')] }),
        new TableCell({ children: [new Paragraph(item.size || '')] }),
        new TableCell({ children: [new Paragraph(item.material || '')] }),
        new TableCell({ children: [new Paragraph(String(item.quantity))] }),
        new TableCell({ children: [new Paragraph(String(item.price))] }),
        new TableCell({ children: [new Paragraph(String(item.subtotal))] })
      ]
    })
  )

  // 总价行
  const totalRow = new TableRow({
    children: [
      new TableCell({ children: [new Paragraph('')] }),
      new TableCell({ children: [new Paragraph('')] }),
      new TableCell({ children: [new Paragraph('')] }),
      new TableCell({ children: [new Paragraph('')] }),
      new TableCell({ children: [new Paragraph('')] }),
      new TableCell({ children: [new Paragraph('总价')] }),
      new TableCell({ children: [new Paragraph(String(totalPrice))] })
    ]
  })

  const table = new Table({
    rows: [headerRow, ...dataRows, totalRow]
  })

  const doc = new Document({
    sections: [
      {
        children: [
          new Paragraph({
            text: '报价清单',
            heading: 'Heading1'
          }),
          table
        ]
      }
    ]
  })

  const blob = await Packer.toBlob(doc)
  saveAs(blob, '报价清单.docx')
}
