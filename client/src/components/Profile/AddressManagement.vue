<template>
  <div class="address-management">
    <div class="page-container">
      <span class="back-icon" @click="$router.push('/profile/personal')">
        <i class="fas fa-angle-left"></i>
      </span>
      <h2 class="title">常用地址管理</h2>
    </div>

    <a-spin :spinning="loading">
      <!-- 地址列表 -->
      <div class="address-list" v-if="addresses.length">
        <div v-for="address in addresses" :key="address.id" class="address-item">
          <div class="address-content">
            <div class="address-info">
              <div class="address-type">{{ getAddressTypeText(address.address_type) }}</div>
              <div class="address-name">{{ address.name }}</div>
              <div class="address-text">{{ address.address_detail }}</div>
              <div class="address-notes" v-if="address.notes">{{ address.notes }}</div>
              <div class="address-contact" v-if="address.contact_person">
                联系人: {{ address.contact_person }}
                <span v-if="address.contact_phone"> - {{ address.contact_phone }}</span>
              </div>
              <div class="address-default" v-if="address.is_default">
                <a-tag color="blue">默认地址</a-tag>
              </div>
            </div>
            <div class="address-actions">
              <a-button type="text" @click="editAddress(address)">
                <template #icon><i class="fas fa-edit"></i></template>
              </a-button>
              <a-button type="text" danger @click="confirmDelete(address)">
                <template #icon><i class="fas fa-trash-alt"></i></template>
              </a-button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态 -->
      <div class="empty-state" v-else-if="!loading">
        <a-empty description="暂无常用地址" />
      </div>
    </a-spin>

    <!-- 添加按钮 -->
    <div class="add-address">
      <a-button type="primary" shape="circle" size="large" @click="showAddressModal(null)">
        <template #icon><i class="fas fa-plus"></i></template>
      </a-button>
    </div>
    
    <!-- 地址表单弹窗 - 修复 Modal 警告 -->
    <a-modal
      :open="addressModalVisible"
      :title="currentAddress ? '编辑地址' : '新增地址'"
      @ok="saveAddress"
      @cancel="addressModalVisible = false"
      :confirmLoading="saveLoading"
      :width="350"
    >
      <a-form :model="addressForm" layout="vertical">
        <a-form-item label="地址类型" required>
          <a-select v-model:value="addressForm.address_type">
            <a-select-option value="pickup">取餐地址</a-select-option>
            <a-select-option value="delivery">送达地址</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="地址名称" required>
          <a-input 
            v-model:value="addressForm.name" 
            placeholder="如：宿舍、食堂、教学楼等"
          />
        </a-form-item>
        
        <a-form-item label="具体地址" required>
          <a-textarea 
            v-model:value="addressForm.address_detail" 
            :rows="3" 
            placeholder="请输入详细地址，如XX区XX楼XX层"
          />
        </a-form-item>
        
        <a-form-item label="联系人">
          <a-input 
            v-model:value="addressForm.contact_person" 
            placeholder="可选"
          />
        </a-form-item>
        
        <a-form-item label="联系电话">
          <a-input 
            v-model:value="addressForm.contact_phone" 
            placeholder="可选"
          />
        </a-form-item>
        
        <a-form-item label="备注">
          <a-input 
            v-model:value="addressForm.notes" 
            placeholder="可选，如配送注意事项"
          />
        </a-form-item>
        
        <a-form-item label="设为默认地址">
          <a-switch v-model:checked="addressForm.is_default" />
        </a-form-item>
      </a-form>
    </a-modal>
    
    <!-- 删除确认 - 修复 Modal 警告 -->
    <a-modal
      :open="deleteModalVisible"
      title="确认删除"
      @ok="deleteAddress"
      @cancel="deleteModalVisible = false"
      :okText="'删除'"
      :okButtonProps="{ danger: true }"
      :confirmLoading="deleteLoading"
      :width="300"
    >
      <p>确定要删除此地址吗？此操作无法撤销。</p>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { getAddresses, addAddress, updateAddress, deleteAddress as deleteAddressAPI } from '@/api/address.js';

const router = useRouter();
const route = useRoute();
const addresses = ref([]);
const loading = ref(false);
const addressModalVisible = ref(false);
const saveLoading = ref(false);
const deleteModalVisible = ref(false);
const deleteLoading = ref(false);
const addressToDelete = ref(null);
const currentAddress = ref(null);

const addressForm = ref({
  address_type: 'pickup',
  name: '',
  address_detail: '',
  contact_person: '',
  contact_phone: '',
  notes: '',
  is_default: false
});

onMounted(() => {
  // 根据路由参数设置默认地址类型
  const addressType = route.query.type;
  if (addressType && ['pickup', 'delivery'].includes(addressType)) {
    addressForm.value.address_type = addressType;
  }
  
  fetchAddresses();
});

// 获取地址列表
async function fetchAddresses() {
  loading.value = true;
  try {
    const response = await getAddresses();
    if (response.code === 200) {
      addresses.value = response.data;
    } else {
      throw new Error(response.message || '获取地址失败');
    }
  } catch (error) {
    console.error('获取地址失败', error);
    message.error(error.message || '获取地址列表失败');
  } finally {
    loading.value = false;
  }
}

// 显示地址编辑弹窗
function showAddressModal(address) {
  currentAddress.value = address;
  if (address) {
    // 编辑模式
    addressForm.value = {
      address_type: address.address_type,
      name: address.name || '',
      address_detail: address.address_detail,
      contact_person: address.contact_person || '',
      contact_phone: address.contact_phone || '',
      notes: address.notes || '',
      is_default: address.is_default
    };
  } else {
    // 新增模式
    const defaultType = route.query.type || 'pickup';
    addressForm.value = {
      address_type: defaultType,
      name: '',
      address_detail: '',
      contact_person: '',
      contact_phone: '',
      notes: '',
      is_default: false
    };
  }
  addressModalVisible.value = true;
}

// 编辑地址
function editAddress(address) {
  showAddressModal(address);
}

// 显示删除确认弹窗
function confirmDelete(address) {
  addressToDelete.value = address;
  deleteModalVisible.value = true;
}

// 保存地址
async function saveAddress() {
  // 验证必填字段
  if (!addressForm.value.name.trim()) {
    message.error('请输入地址名称');
    return;
  }
  
  if (!addressForm.value.address_detail.trim()) {
    message.error('请输入具体地址');
    return;
  }
  
  saveLoading.value = true;
  try {
    let response;
    if (currentAddress.value) {
      // 更新地址
      response = await updateAddress(currentAddress.value.id, addressForm.value);
      message.success('地址更新成功');
    } else {
      // 新增地址
      response = await addAddress(addressForm.value);
      message.success('地址添加成功');
    }
    
    addressModalVisible.value = false;
    await fetchAddresses(); // 刷新列表
  } catch (error) {
    console.error('保存地址失败', error);
    message.error(error.message || '操作失败，请稍后重试');
  } finally {
    saveLoading.value = false;
  }
}

// 删除地址
async function deleteAddress() {
  if (!addressToDelete.value) return;
  
  deleteLoading.value = true;
  try {
    await deleteAddressAPI(addressToDelete.value.id);
    message.success('地址已删除');
    deleteModalVisible.value = false;
    await fetchAddresses(); // 刷新列表
  } catch (error) {
    console.error('删除地址失败', error);
    message.error(error.message || '删除失败，请稍后重试');
  } finally {
    deleteLoading.value = false;
  }
}

// 获取地址类型显示文本
function getAddressTypeText(type) {
  const typeMap = {
    pickup: '取餐地址',
    delivery: '送达地址'
  };
  return typeMap[type] || '其他';
}
</script>

<style scoped>
.address-management {
  max-width: 390px;
  margin: 0 auto;
  padding-bottom: 70px;
  background-color: #f5f5f7;
  min-height: 900px;
}

.page-container {
  display: flex;
  padding: 20px;
  align-items: center;
  background-color: #fff;
  position: relative;
  margin-bottom: 16px;
  max-width: 390px;
}

.back-icon {
  font-size: 18px;
  margin-right: 15px;
  cursor: pointer;
  color: #333;
}

.title {
  font-size: 18px;
  margin: 0;
  flex: 1;
  text-align: center;
  font-weight: 600;
  color: #333;
}

.address-list {
  padding: 0 16px;
  max-width: 390px;
}

.address-item {
  background-color: #fff;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.address-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.address-info {
  flex: 1;
  margin-right: 10px;
}

.address-type {
  font-weight: 500;
  margin-bottom: 5px;
  color: #1890ff;
  font-size: 12px;
}

.address-name {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
  font-size: 14px;
}

.address-text {
  margin-bottom: 5px;
  color: #666;
  font-size: 13px;
  line-height: 1.4;
}

.address-contact {
  font-size: 12px;
  color: #888;
  margin-bottom: 5px;
}

.address-notes {
  font-size: 12px;
  color: #888;
  margin-bottom: 5px;
}

.address-default {
  margin-top: 5px;
}

.address-actions {
  display: flex;
  align-items: flex-start;
  gap: 5px;
}

.empty-state {
  background-color: #fff;
  padding: 40px 16px;
  border-radius: 8px;
  margin: 16px;
  max-width: 390px;
}

.add-address {
  position: fixed;
  right: calc(50% - 195px + 20px);
  bottom: 80px;
  z-index: 100;
}

/* 响应式设计 */
@media (max-width: 420px) {
  .address-management {
    max-width: 100%;
  }
  
  .page-container,
  .address-list,
  .empty-state {
    max-width: 100%;
  }
  
  .add-address {
    right: 20px;
  }
}

/* 确保 Modal 内容也符合宽度限制 */
:deep(.ant-modal-content) {
  max-width: 350px;
}

:deep(.ant-form-item-label) {
  font-weight: 500;
}

:deep(.ant-input),
:deep(.ant-select),
:deep(.ant-input-affix-wrapper) {
  border-radius: 6px;
}

:deep(.ant-btn) {
  border-radius: 6px;
}
</style>