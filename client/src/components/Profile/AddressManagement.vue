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
              <div class="address-text">{{ address.address_detail }}</div>
              <div class="address-notes" v-if="address.notes">{{ address.notes }}</div>
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
    
    <!-- 地址表单弹窗 -->
    <a-modal
      v-model:visible="addressModalVisible"
      :title="currentAddress ? '编辑地址' : '新增地址'"
      @ok="saveAddress"
      :confirmLoading="saveLoading"
    >
      <a-form :model="addressForm" layout="vertical">
        <a-form-item label="地址类型" required>
          <a-select v-model:value="addressForm.address_type">
            <a-select-option value="home">宿舍/家</a-select-option>
            <!-- <a-select-option value="school">学校</a-select-option> -->
            <a-select-option value="work">工作地点</a-select-option>
            <a-select-option value="other">其他</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="具体地址" required>
          <a-textarea 
            v-model:value="addressForm.address_detail" 
            :rows="3" 
            placeholder="请输入详细地址，如XX区XX楼XX层"
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
    
    <!-- 删除确认 -->
    <a-modal
      v-model:visible="deleteModalVisible"
      title="确认删除"
      @ok="deleteAddress"
      :okText="'删除'"
      :okButtonProps="{ danger: true }"
      :confirmLoading="deleteLoading"
    >
      <p>确定要删除此地址吗？此操作无法撤销。</p>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message } from 'ant-design-vue';
import axios from 'axios';

const router = useRouter();
const addresses = ref([]);
const loading = ref(false);
const addressModalVisible = ref(false);
const saveLoading = ref(false);
const deleteModalVisible = ref(false);
const deleteLoading = ref(false);
const addressToDelete = ref(null);
const currentAddress = ref(null);

const addressForm = ref({
  address_type: 'home',
  address_detail: '',
  notes: '',
  is_default: false
});

onMounted(() => {
  fetchAddresses();
});

// 获取地址列表
async function fetchAddresses() {
  loading.value = true;
  try {
    const response = await axios.get('/api/users/addresses');
    addresses.value = response.data.data;
  } catch (error) {
    console.error('获取地址失败', error);
    message.error('获取地址列表失败');
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
      address_detail: address.address_detail,
      notes: address.notes || '',
      is_default: address.is_default
    };
  } else {
    // 新增模式
    addressForm.value = {
      address_type: 'home',
      address_detail: '',
      notes: '',
      is_default: false
    };
  }
  addressModalVisible.value = true;
}

// 显示删除确认弹窗
function confirmDelete(address) {
  addressToDelete.value = address;
  deleteModalVisible.value = true;
}

// 保存地址
async function saveAddress() {
  if (!addressForm.value.address_detail.trim()) {
    message.error('请输入具体地址');
    return;
  }
  
  saveLoading.value = true;
  try {
    if (currentAddress.value) {
      // 更新地址
      await axios.put(`/api/users/addresses/${currentAddress.value.id}`, addressForm.value);
      message.success('地址更新成功');
    } else {
      // 新增地址
      await axios.post('/api/users/addresses', addressForm.value);
      message.success('地址添加成功');
    }
    addressModalVisible.value = false;
    fetchAddresses(); // 刷新列表
  } catch (error) {
    console.error('保存地址失败', error);
    message.error('操作失败，请稍后重试');
  } finally {
    saveLoading.value = false;
  }
}

// 删除地址
async function deleteAddress() {
  if (!addressToDelete.value) return;
  
  deleteLoading.value = true;
  try {
    await axios.delete(`/api/users/addresses/${addressToDelete.value.id}`);
    message.success('地址已删除');
    deleteModalVisible.value = false;
    fetchAddresses(); // 刷新列表
  } catch (error) {
    console.error('删除地址失败', error);
    message.error('删除失败，请稍后重试');
  } finally {
    deleteLoading.value = false;
  }
}

// 获取地址类型显示文本
function getAddressTypeText(type) {
  const typeMap = {
    home: '宿舍/家',
    work: '工作地点',
    other: '其他'
  };
  return typeMap[type] || '其他';
}
</script>

<style scoped>
.address-management {
  padding-bottom: 70px;
  max-width:390px;
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
}

.back-icon {
  font-size: 18px;
  margin-right: 15px;
  cursor: pointer;
}

.title {
  font-size: 18px;
  margin: 0;
  flex: 1;
  text-align: center;
}

.address-list {
  padding: 0 16px;
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
}

.address-info {
  flex: 1;
}

.address-type {
  font-weight: 500;
  margin-bottom: 5px;
  color: #1890ff;
}

.address-text {
  margin-bottom: 5px;
}

.address-notes {
  font-size: 13px;
  color: #888;
}

.address-actions {
  display: flex;
  align-items: flex-start;
}

.empty-state {
  background-color: #fff;
  padding: 40px 16px;
  border-radius: 8px;
  margin: 16px;
}

.add-address {
  position: absolute;
  right: 20px;
  bottom: 80px;
}
</style>