<script setup>
import { ref, onMounted, h } from "vue";
import api from "@/api";
import { NButton, useMessage } from "naive-ui";

const message = useMessage();
const props = defineProps({
  billId: {
    type: Number,
    required: true
  }
});

let total_amount = ref(0);
let paid_amount = ref(0);
let remark = ref("");
let created_at = ref("");
let status = ref("");
const items = ref([]);
let settleShow = ref(false);
let settleShowBatch = ref(false);
let payment_method = ref("cash");
let settler_name = ref("");
let settle_remark = ref("");
let rowToSettle = ref(null);
const paymentMethodOptions = [
  {
    label: "现金",
    value: "cash"
  },
  {
    label: "微信",
    value: "wechat"
  },
  {
    label: "支付宝",
    value: "alipay"
  }
];
const selectItems = ref([]);

// 获取账单详情
async function fetchBillDetail() {
  try {
    const response = await api.getBillDetail({ bill_id: props.billId });
    items.value = response.data.items;
    total_amount.value = response.data.total_amount;
    paid_amount.value = response.data.paid_amount;
    remark.value = response.data.remark;
    created_at.value = response.data.created_at.split("T")[0];
    status.value = getBillStatus(response.data.status);
  } catch (error) {
    console.error("获取账单详情失败", error);
  }
}

// 获取账单状态
function getBillStatus(status) {
  if (status === "paid") {
    return "已付款";
  } else if (status === "unpaid") {
    return "未付款";
  } else if (status === "refunded") {
    return "已退款";
  }
}

// 关闭单个结算模态框
function closeSettleModal() {
  settleShow.value = false;
  rowToSettle.value = null;
}

// 关闭批量结算模态框
function closeSettleBatchModal() {
  settleShowBatch.value = false;
}

// 监听表格 选项卡改动
function handleSelectionChange(rows) {
  selectItems.value = [];
  rows.forEach((item) => {
    selectItems.value.push(item);
  });
}

// 处理单个结算
async function handleSettle(row) {
  if (row.status === "refunded") {
    message.warning("该商品已退款，请勿重复操作");
    return;
  } else if (row.status === "paid") {
    message.warning("该商品已付款，请勿重复操作");
    return;
  }
  settleShow.value = true;
  rowToSettle.value = row;
}

// 处理批量结算
async function handleSettleBatch() {
  if (selectItems.value.length === 0) {
    message.warning("请选择要结算的商品");
    return;
  }
  settleShowBatch.value = true;
}

// 批量结算确认按钮
async function confirmSettleBatch() {
  try {
    const response = await api.settleBillBatch(
      {
        payment_method: payment_method.value,
        settler_name: settler_name.value,
        remark: settle_remark.value,
        bill_id: props.billId,
        item_ids: selectItems.value.map((item) => item)
      }
    );
    if (response.code === 200) {
      message.success("批量结算成功");
      await fetchBillDetail();
    } else {
      message.error("批量结算失败" + response.msg);
    }
  } catch (error) {
    console.error("批量结算失败", error);
    message.error("结算失败,稍后重试");
  }
}

// 单个确认结算按钮点击事件
async function confirmSettle() {
  if (!rowToSettle.value) {
    message.error("请选择要结算的商品");
    return;
  }
  try {
    const response = await api.settleBillItem(
      {
        payment_method: payment_method.value,
        settler_name: settler_name.value,
        remark: settle_remark.value
      },
      {
        bill_id: props.billId,
        item_id: rowToSettle.value.id
      }
    );
    if (response.code === 200) {
      message.success("结算成功");
      settleShow.value = false;
      await fetchBillDetail();
    } else {
      message.error("结算失败" + response.msg);
    }
  } catch (error) {
    message.error("结算过程中发生错误，请稍后重试");
  }
}

// 定义表格列
const columns = [
  {
    type: "selection",
    fixed: "left",
    disabled(row) {
      return row.status === "refunded" || row.status === "paid";
    }
  },
  {
    title: "商品名称",
    key: "product_name",
    fixed: "left"
  },
  {
    title: "总价",
    key: "amount"
  },
  {
    title: "商品单价",
    key: "price"
  },
  {
    title: "商品数量",
    key: "quantity"
  },
  {
    title: "单位",
    key: "unit"
  },
  {
    title: "购买时间",
    key: "purchase_time",
    render(row) {
      return row.purchase_time.split("T")[0];
    }
  },
  {
    title: "购买人",
    key: "buyer_name"
  },
  {
    title: "已/未付款",
    key: "status",
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
    title: "结账人",
    key: "settler_name"
  },
  {
    title: "结账方式",
    key: "payment_method",
    // credit是挂帐 cash是现金 WeChat是微信 Alipay是支付宝
    render(row) {
      if (row.payment_method === "credit") {
        return "挂帐";
      } else if (row.payment_method === "cash") {
        return "现金";
      } else if (row.payment_method === "wechat") {
        return "微信";
      } else if (row.payment_method === "alipay") {
        return "支付宝";
      }
    }
  },
  {
    title: "备注",
    key: "remark"
  },
  {
    title: "操作",
    key: "action",
    fixed: "right",
    render(row) {
      return h(
        NButton,
        {
          size: "small",
          type: "primary",
          onClick: () => handleSettle(row)
        },
        { default: () => "结算" }
      );
    }
  }
];

onMounted(() => {
  fetchBillDetail();
});
</script>

<template>
  <n-grid x-gap="24" :cols="4">
    <n-grid-item>
      <n-card title="账单总额">
        {{ total_amount }}
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="已支付金额">
        {{ paid_amount }}
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="创建时间">
        {{ created_at }}
      </n-card>
    </n-grid-item>
    <n-grid-item>
      <n-card title="账单状态">
        {{ status }}
      </n-card>
    </n-grid-item>
  </n-grid>
  <n-divider></n-divider>
  <div class="flex justify-end">
    <n-button type="primary" @click="handleSettleBatch" class="mr-10">批量结算</n-button>
    <n-button type="warning" @click="handleRefundBatch">批量退款</n-button>
  </div>
  <n-data-table
    :columns="columns"
    :data="items"
    :max-height="400"
    :scroll-x="1800"
    virtual-scroll
    :row-key="(row) => row.id"
    class="mt-10"
    :on-update:checked-row-keys="handleSelectionChange"
  />
  <n-modal v-model:show="settleShow">
    <n-card title="商品结算" size="huge" role="dialog" style="width: 600px" aria-modal="true" :bordered="false">
      <NSelect v-model:value="payment_method" :options="paymentMethodOptions" placeholder="请选择结算方式"
               type="text" />
      <n-input class="mt-10" v-model:value="settler_name" placeholder="输入结算人姓名" />
      <n-input class="mt-10" v-model:value="settle_remark" placeholder="输入备注" />
      <div style="text-align: right; margin-top: 10px;">
        <n-button type="default" class="mr-10" @click="closeSettleModal">取消结算</n-button>
        <n-button type="primary" @click="confirmSettle">确认结算</n-button>
      </div>
    </n-card>
  </n-modal>
  <n-modal v-model:show="settleShowBatch">
    <n-card title="商品结算" size="huge" role="dialog" style="width: 600px" aria-modal="true" :bordered="false">
      <NSelect v-model:value="payment_method" :options="paymentMethodOptions" placeholder="请选择结算方式"
               type="text" />
      <n-input class="mt-10" v-model:value="settler_name" placeholder="输入结算人姓名" />
      <n-input class="mt-10" v-model:value="settle_remark" placeholder="输入备注" />
      <div style="text-align: right; margin-top: 10px;">
        <n-button type="default" class="mr-10" @click="closeSettleBatchModal">取消结算</n-button>
        <n-button type="primary" @click="confirmSettleBatch">确认结算</n-button>
      </div>
    </n-card>
  </n-modal>
</template>
