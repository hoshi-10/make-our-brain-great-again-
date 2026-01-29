<template>
  <view class="box">
    <input v-model.number="form.quantity" placeholder="数量" />
    <input v-model.number="form.price" placeholder="单价" />
    <input v-model="form.size" placeholder="尺寸" />
    <input v-model="form.material" placeholder="材料" />

    <button @click="addItem">添加到清单</button>

    <view
      v-for="(item, index) in list"
      :key="index"
    >
      {{ index + 1 }} |
      {{ item.size }} |
      {{ item.material }} |
      {{ item.quantity }} × {{ item.price }} =
      ￥{{ item.subtotal }}
    </view>

    <view class="total">
      总价：￥{{ totalPrice }}
    </view>

    <button @click="print">打印</button>
  </view>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'

const form = reactive({
  quantity: 0,
  price: 0,
  size: '',
  material: ''
})

const list = ref([])

const addItem = () => {
  list.value.push({
    quantity: form.quantity,
    price: form.price,
    size: form.size,
    material: form.material,
    subtotal: form.quantity * form.price
  })
}

const totalPrice = computed(() => {
  return list.value.reduce((sum, item) => sum + item.subtotal, 0)
})

const print = () => {
  window.print()
}
</script>

<style>
.box {
  padding: 20rpx;
}
.total {
  margin-top: 20rpx;
  font-weight: bold;
}
</style>
