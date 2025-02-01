<script setup>
import { ref, onMounted } from 'vue'
import {
  NCard,
  NButton,
  NSpace,
  NForm,
  NFormItem,
  NInput,
  NInputNumber,
  NDataTable,
} from 'naive-ui'
import { formatDate } from '@/utils'
import api from '@/api'

const props = defineProps({
  billId: {
    type: Number,
    required: true,
  },
})

const emit = defineEmits(['success', 'close'])

const billDetail = ref(null)
const selectedItems = ref([])
const showAddItem = ref(false)

const itemForm = ref({
  name: '',
  price: 0,
  quantity: 1,
})

const columns = [
  { title: '商品名称', key: 'name' },
  { title: '单价', key: 'price' },
  { title: '数量', key: 'quantity' },
  { title: '总价', key: 'total_price' },
  { title: '状态', key: 'status' },
  {
    title: '操作',
    key: 'actions',
    render(row) {
      if (row.status === 'unpaid') {
        return h(
          NButton,
          {
            size: 'small',
            onClick: () => handleSettleItem(row.id),
          },
          { default: () => '结算' }
        )
      }
      return '已结算'
    },
  },
]

async function loadBillDetail() {
  try {
    billDetail.value = await api.getBillDetail(props.billId)
  } catch (error) {
    console.error('加载账单详情失败:', error)
  }
}

async function handleAddItem() {
  try {
    await api.addBillItem(props.billId, itemForm.value)
    showAddItem.value = false
    itemForm.value = { name: '', price: 0, quantity: 1 }
    await loadBillDetail()
    emit('success')
  } catch (error) {
    console.error('添加商品失败:', error)
  }
}

async function handleSettleItems() {
  if (selectedItems.value.length === 0) return
  try {
    await api.settleBillItems(props.billId, selectedItems.value)
    await loadBillDetail()
    selectedItems.value = []
    emit('success')
  } catch (error) {
    console.error('结算商品失败:', error)
  }
}

async function handleSettleItem(itemId) {
  try {
    await api.settleBillItems(props.billId, [itemId])
    await loadBillDetail()
    emit('success')
  } catch (error) {
    console.error('结算商品失败:', error)
  }
}

onMounted(() => {
  loadBillDetail()
})

onMounted(() => {
  loadBillDetail()
})
</script>

<template>
  <div class="p-4">
    <NCard v-if="billDetail" title="账单信息">
      <NSpace vertical>
        <div>用户名称：{{ billDetail.owner_name }}</div>
        <div>账单状态：{{ billDetail.status }}</div>
        <div>总金额：{{ billDetail.total_amount }}</div>
        <div>已结金额：{{ billDetail.paid_amount }}</div>
        <div>备注：{{ billDetail.remark }}</div>
      </NSpace>
    </NCard>

    <NCard class="mt-4" title="商品列表">
      <template #header-extra>
        <NSpace>
          <NButton
            v-if="selectedItems.length > 0"
            type="primary"
            @click="handleSettleItems"
          >
            批量结算
          </NButton>
          <NButton @click="showAddItem = true">添加商品</NButton>
        </NSpace>
      </template>

      <NDataTable
        :columns="columns"
        :data="billDetail?.items || []"
        :row-key="(row) => row.id"
        v-model:checked-row-keys="selectedItems"
      />
    </NCard>

    <NCard v-if="showAddItem" class="mt-4" title="添加商品">
      <NForm>
        <NFormItem label="商品名称">
          <NInput v-model:value="itemForm.name" placeholder="请输入商品名称" />
        </NFormItem>
        <NFormItem label="单价">
          <NInputNumber v-model:value="itemForm.price" placeholder="请输入单价" />
        </NFormItem>
        <NFormItem label="数量">
          <NInputNumber v-model:value="itemForm.quantity" placeholder="请输入数量" :min="1" />
        </NFormItem>
        <NSpace justify="end">
          <NButton @click="showAddItem = false">取消</NButton>
          <NButton type="primary" @click="handleAddItem">确定</NButton>
        </NSpace>
      </NForm>
    </NCard>
  </div>
</template>
