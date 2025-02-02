<script setup>
import { ref, onMounted, withDirectives, h, resolveDirective } from 'vue'
import CommonPage from '@/components/page/CommonPage.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import { NButton, NInput, NSelect } from 'naive-ui'
import AddBill from './add.vue'
import DetailBill from './detail.vue'

import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { formatDate } from '@/utils'

const showAddModal = ref(false)
const showDetailModal = ref(false)
const currentBillId = ref(null)

const $table = ref(null)
const queryItems = ref({})
const vPermission = resolveDirective('permission')

function handleDetail(row) {
  currentBillId.value = row.id
  showDetailModal.value = true
}

function handleAdd() {
  showAddModal.value = true
}

const columns = [
  {
    title: '用户',
    key: 'owner_name',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '账单状态',
    key: 'status',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      // paid 是已付款，unpaid是未付款，refunded是已退款
      if (row.status === "paid") {
        return "已付款";
      } else if (row.status === "unpaid") {
        return "未付款";
      } else if (row.status === "refunded") {
        return "已退款";
      }
    }
  },
  {
    title: '总金额',
    key: 'total_amount',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '已结金额',
    key: 'paid_amount',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '创建时间',
    key: 'created_at',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return formatDate(row.updated_at)
    },
  },
  {
    title: '更新时间',
    key: 'updated_at',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return formatDate(row.updated_at)
    },
  },
  {
    title: '备注',
    key: 'remark',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
  },
  {
    title: '操作',
    key: 'action',
    width: 'auto',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return [
        withDirectives(
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              style: 'margin-right: 8px;',
              onClick: () => handleDetail(row),
            },
            {
              default: () =>
                h('div', { style: 'display: flex; align-items: center;' }, [
                  h(TheIcon, {
                    icon: 'material-symbols:info-outline',
                    size: 16,
                    style: 'margin-right: 4px;',
                  }),
                  '详情',
                ]),
            }
          ),
          [[vPermission, 'post/api/v1/bill/detail']]
        ),
      ]
    },
  },
]
const billStatusOptions = [
  {
    label: '已结账',
    value: 'paid',
  },
  {
    label: '未结账',
    value: 'unpaid',
  },
]
onMounted(() => {
  $table.value?.handleSearch()
})
</script>
<template>
  <!--  业务页面-->
  <CommonPage show-footer title="账单列表">
    <template #action>
      <div>
        <NButton
          v-permission="'post/api/v1/bill/create'"
          class="float-right mr-15"
          type="primary"
          @click="handleAdd"
        >
          <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />新建账单
        </NButton>
      </div>
    </template>
    <!--    表格-->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :get-data="api.getBillList"
      :columns="columns"
    >
      <template #queryBar>
        <QueryBarItem label="用户" :label-width="40">
          <NInput
            v-model:value="queryItems.owner_name"
            clearable
            type="text"
            placeholder="请输入用户名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="状态" :label-width="40">
          <NSelect
            v-model:value="queryItems.status"
            clearable
            :options="billStatusOptions"
            type="text"
            placeholder="请输入账单状态"
            style="width: 180px"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <!-- 新建账单抽屉 -->
    <NDrawer v-model:show="showAddModal" placement="right" :width="1200">
      <NDrawerContent title="新建账单" closable>
        <AddBill @success="$table?.handleSearch()" @close="showAddModal = false" />
      </NDrawerContent>
    </NDrawer>

    <!-- 账单详情抽屉 -->
    <NDrawer v-model:show="showDetailModal" placement="right" :width="1200">
      <NDrawerContent title="账单详情" closable>
        <DetailBill
          :bill-id="currentBillId"
          @success="$table?.handleSearch()"
          @close="showDetailModal = false"
        />
      </NDrawerContent>
    </NDrawer>
  </CommonPage>
</template>
