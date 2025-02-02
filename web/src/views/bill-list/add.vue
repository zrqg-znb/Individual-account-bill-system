<script setup>
import { ref } from "vue";
import { NForm, NFormItem, NInput, NButton, NSelect } from "naive-ui";
import api from "@/api";

const emit = defineEmits(["success", "close"]);

const formRef = ref(null);
const formValue = ref({
  owner_id: "",
  remark: "",
  items: [
    {
      product_name: "",
      price: 0,
      quantity: 0,
      unit: "",
      purchase_time: null,
      buyer_name: "",
      remark: ""
    }
  ]
});
const userOptions = ref([]);
const rules = {
  owner_id: {
    required: true,
    validator: (rule, value) => {
      if (value === null || value === undefined || value === "") {
        return new Error("请选择用户");
      }
      return true;
    },
    trigger: "blur"
  },
  items: {
    required: true,
    validator: (rule, value) => {
      if (!Array.isArray(value) || value.length === 0) {
        return new Error("至少需要一个商品信息");
      }
      return true;
    },
    trigger: "change"
  }
};

async function handleSearchUser(value) {
  const { data } = await api.searchUser({
    username: value
  });

  userOptions.value = data.map((item) => ({
    label: item.username + "--" + item.dept_name,
    value: Number(item.id)
  }));
}

async function handleSubmit() {
  try {
    await formRef.value?.validate();
    await api.createBill(formValue.value);
    emit("success");
    emit("close");
    $message.success("创建账单成功");
  } catch (error) {
    console.error("表单验证失败:", error);
  }
}

function handleCancel() {
  emit("close");
}
</script>

<template>
  <div class="p-4">
    <NForm
      ref="formRef"
      :model="formValue"
      :rules="rules"
      label-placement="left"
      label-width="100"
      require-mark-placement="right-hanging"
    >
      <NGrid :cols="24" :x-gap="24">
        <NFormItemGi :span="6" label="用户" path="owner_id">
          <n-select
            v-model:value="formValue.owner_id"
            filterable
            placeholder="搜索用户"
            :options="userOptions"
            clearable
            remote
            @search="handleSearchUser"
          />
        </NFormItemGi>
      </NGrid>

      <NFormItem label="商品信息" path="items">
        <NDynamicInput
          v-model:value="formValue.items"
          :min="1"
          :on-create="() => ({
            product_name: '',
            price: 0,
            quantity: 0,
            unit: '',
            purchase_time: null,
            buyer_name: '',
            remark: '',
          })"
        >
          <template #default="{ value }">
            <NGrid :cols="24" :x-gap="24">
              <NFormItemGi :span="6" label="名称">
                <NInput v-model:value="value.product_name" placeholder="商品名称" />
              </NFormItemGi>
              <NFormItemGi :span="6" label="单价">
                <NInputNumber v-model:value="value.price" placeholder="请输入单价" />
              </NFormItemGi>
              <NFormItemGi :span="6" label="数量">
                <NInputNumber v-model:value="value.quantity" placeholder="请输入数量" />
              </NFormItemGi>
              <NFormItemGi :span="6" label="单位">
                <NInput v-model:value="value.unit" placeholder="请填写个/斤/米..." />
              </NFormItemGi>
              <NFormItemGi :span="8" label="购买时间">
                <NDatePicker
                  v-model:value="value.purchase_time"
                  type="datetime"
                  placeholder="请选择购买时间"
                />
              </NFormItemGi>
              <NFormItemGi :span="6" label="购买人">
                <NInput v-model:value="value.buyer_name" placeholder="请输入购买人" />
              </NFormItemGi>
              <NFormItemGi :span="8" label="备注">
                <NInput v-model:value="value.remark" placeholder="请输入备注信息" />
              </NFormItemGi>
            </NGrid>
          </template>
        </NDynamicInput>
      </NFormItem>
      <NFormItem label="备注" path="remark">
        <NInput v-model:value="formValue.remark" type="textarea" placeholder="请输入备注信息" />
      </NFormItem>
    </NForm>
    <div class="flex justify-center gap-30 mt-4">
      <NButton @click="handleCancel" type="warning">取消</NButton>
      <NButton type="primary" @click="handleSubmit">确定</NButton>
    </div>
  </div>
</template>
