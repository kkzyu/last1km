<template>
  <div class="action-header-container">
    <button class="btn return-btn" @click="goToHome">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      <span></span>
    </button>
    <button class="btn add-btn" @click="handleAddRequest">
      <span>添加委托</span>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M12 5v14M5 12h14"/></svg>
    </button>
  </div>
</template>

<script setup>
// import { useOrderStore } from '@/stores/orderStore'; // Not used directly here
import { useRouter } from 'vue-router';

// const orderStore = useOrderStore(); // Not used
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
  padding: 12px 15px; /* Standard padding */
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff; /* Give it a background if it's a header bar */
  /* border-bottom: 1px solid #e0e0e0; */ /* Optional separator */
  width:100%;
}

.btn {
  display: flex; /* For aligning icon and text */
  align-items: center;
  justify-content: center;
  gap: 6px; /* Space between icon and text */
  border: none;
  padding: 8px 16px; /* Adjusted padding for better proportions */
  font-size: 15px;   /* Slightly smaller font for mobile */
  font-weight: 500; /* Medium weight */
  border-radius: 20px; /* Consistent rounded corners */
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  /* min-width: 100px; */ /* Optional: ensure a minimum tap target size */
}

.btn .icon {
  margin-bottom: -2px; /* Fine-tune icon vertical alignment */
}

.return-btn {
  background-color: #f0f2f5; /* Lighter gray, less prominent */
  color: #333; /* Darker text for readability */
  /* border: 1px solid #d0d0d0; */ /* Optional subtle border */
  /* margin-right:300px; */
}

.return-btn:hover {
  background-color: #e0e2e5;
  /* transform: translateY(-1px); */
}

.add-btn {
  background-color: #007BFF;
  color: white;
}

.add-btn:hover {
  background-color: #0056b3;
  /* transform: translateY(-1px); */
}
</style>