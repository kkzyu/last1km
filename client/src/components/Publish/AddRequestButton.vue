<template>
  <div class="action-header-container">
    <a-button type="default" @click="goToHome" class="return-btn">
      <template #icon><ArrowLeftOutlined /></template>
      返回
    </a-button>
    <a-button type="primary" @click="handleAddRequest" class="add-btn">
      <template #icon><PlusOutlined /></template>
      添加委托
    </a-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { ArrowLeftOutlined, PlusOutlined } from '@ant-design/icons-vue';

const router = useRouter();
const emit = defineEmits(['add-request-clicked']);

const handleAddRequest = () => {
  emit('add-request-clicked');
};

const goToHome = () => {
  router.push('/home'); // Assuming '/home' is your home route
};
</script>

<style scoped>
.action-header-container {
  padding: 0px; /* Consistent padding */
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  /* border-bottom: 1px solid #f0f0f0; */ /* Ant Design's PageHeader might handle this if used in parent */
  width:100%;
  box-sizing: border-box;
}

.return-btn {
  /* Ant Design buttons have their own styling, we might adjust margin if needed */
}

.add-btn {
  /* Ant Design buttons have their own styling */
}

/* Optional: If you need to enforce a specific gap that antd's default doesn't provide */
.action-header-container > .ant-btn + .ant-btn {
  margin-left: 12px; /* Example gap */
}
</style>