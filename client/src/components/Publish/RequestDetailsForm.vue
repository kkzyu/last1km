<template>
  <div class="request-details-form">
    <div class="task-header">
      <span class="task-title">委托 {{ index + 1 }}</span>
      <!-- Checkbox for selecting this specific task -->
      <div class="checkbox-container">
        <input
          type="checkbox"
          :id="'task-selected-checkbox-' + index"
          v-model="isSelected"
          class="custom-checkbox"
        >
        <label :for="'task-selected-checkbox-' + index" class="checkbox-label"></label>
      </div>
    </div>

    <div class="form-section route-section">
      <div class="route-point origin">
        <div class="point-icon-wrapper">
          <div class="point-icon origin-icon">起</div>
          <div class="route-connector">
            <!-- Optional: SVG for dashed line if needed, or just spacing -->
          </div>
        </div>
        <div class="point-details">
          <textarea
            v-model="computedOrigin"
            placeholder="选择添加起点，填写详细信息 (如蓝田北门外卖柜)"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>
      </div>

      <div class="route-point destination">
        <div class="point-icon-wrapper">
          <div class="point-icon destination-icon">终</div>
        </div>
        <div class="point-details">
          <textarea
            v-model="computedDestination"
            placeholder="选择添加终点，填写详细信息 (如青溪一舍大厅)"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>
      </div>
    </div>

    <div class="form-section item-info-section">
      <div class="info-field">
        <label :for="'item-description-' + index">物品描述:</label>
        <textarea :id="'item-description-' + index" v-model="computedDescription" placeholder="例如：商家名称+商品名称" class="form-textarea" rows="2"></textarea>
      </div>

      <div class="info-field">
        <label>订单截图:</label>
        <div class="screenshot-upload-area" @click="triggerFileUpload">
          <input type="file" :ref="el => fileInputRef = el" @change="handleFileUpload" style="display: none;" accept="image/*">
          <div v-if="!uploadedImagePreview" class="upload-prompt">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
            <span>点击上传图片</span>
          </div>
          <img v-if="uploadedImagePreview" :src="uploadedImagePreview" alt="截图预览" class="image-preview"/>
          <span v-if="uploadedImageName && !uploadedImagePreview" class="file-name-display">{{ uploadedImageName }}</span>
        </div>
      </div>

      <div class="info-field">
        <label :for="'order-info-' + index">取件信息:</label>
        <textarea :id="'order-info-' + index" v-model="computedOrderInfo" placeholder="例如：外卖柜号, 取件码, 手机号后四位" class="form-textarea" rows="3"></textarea>
      </div>
    </div>

    <div class="form-section task-amount-section">
      <label :for="'task-amount-input-' + index">委托金额:</label>
      <div class="amount-input-group">
        <input type="number" :id="'task-amount-input-' + index" v-model="computedTaskAmount" placeholder="0.00" step="0.01" min="0">
        <span>元</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
// import { useOrderStore } from '@/stores/orderStore'; // Not directly needed for store modification here

const props = defineProps({
  index: { type: Number, required: true },
  origin: String,
  destination: String,
  description: String, // For item description
  orderInfo: String,   // For pickup details
  taskAmount: Number,
  selected: Boolean    // For the task selection checkbox
});

const emit = defineEmits([
  'update:origin',
  'update:destination',
  'update:description',
  'update:orderInfo',
  'update:taskAmount',
  'update:selected' // Emit for selection change
]);

// const orderStore = useOrderStore(); // Not used for store modification

// Computed properties for v-model two-way binding
const computedOrigin = computed({
  get: () => props.origin,
  set: (value) => emit('update:origin', value)
});
const computedDestination = computed({
  get: () => props.destination,
  set: (value) => emit('update:destination', value)
});
const computedDescription = computed({ // For item description
  get: () => props.description,
  set: (value) => emit('update:description', value)
});
const computedOrderInfo = computed({ // For pickup details
  get: () => props.orderInfo,
  set: (value) => emit('update:orderInfo', value)
});
const computedTaskAmount = computed({
  get: () => props.taskAmount,
  set: (value) => {
    const numValue = parseFloat(value);
    emit('update:taskAmount', isNaN(numValue) ? null : numValue);
  }
});
const isSelected = computed({ // For the task selection checkbox
  get: () => props.selected,
  set: (value) => emit('update:selected', value)
});


// File upload internal state
const fileInputRef = ref(null);
const uploadedImageName = ref('');
const uploadedImagePreview = ref('');

const triggerFileUpload = () => {
  fileInputRef.value?.click();
};

const handleFileUpload = (event) => {
  const file = event.target.files?.[0];
  if (file) {
    uploadedImageName.value = file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedImagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    // TODO: Emit the file or handle actual upload to server
    // emit('file-uploaded', file);
    console.log('Selected file:', file);
  } else {
    uploadedImageName.value = '';
    uploadedImagePreview.value = '';
  }
};

// onMounted: Removed store modification. Parent component is responsible for data.
</script>

<style scoped>
.request-details-form {
  background-color: #fff; /* White background for the form card */
  border-radius: 10px;
  padding: 15px;
  /* margin-bottom: 15px; /* Spacing handled by parent's .request-item-container */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08); /* Softer shadow */
  /* REMOVED: height and overflow-y. Parent handles scrolling. */
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.task-title {
  font-size: 17px;
  font-weight: 600; /* Semibold */
  color: #333;
}

/* Custom Checkbox Styling */
.checkbox-container {
  position: relative;
  display: inline-block;
  width: 20px;
  height: 20px;
}
.custom-checkbox {
  opacity: 0; /* Hide original checkbox */
  width: 0;
  height: 0;
  position: absolute;
}
.checkbox-label {
  position: absolute;
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  background-color: #fff;
  border: 1.5px solid #adb5bd;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s;
}
.custom-checkbox:checked + .checkbox-label {
  background-color: #007bff;
  border-color: #007bff;
}
.custom-checkbox:checked + .checkbox-label::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}


.form-section {
  margin-bottom: 20px;
}
.form-section:last-child {
  margin-bottom: 0;
}

.route-point {
  display: flex;
  align-items: flex-start; /* Align icon with top of textarea */
  width: 100%;
  margin-bottom: 15px;
}
.route-point:last-child {
  margin-bottom: 0;
}

.point-icon-wrapper {
  margin-right: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 4px; /* Align icon better with textarea */
}

.point-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: bold;
  color: white;
}
.origin-icon {
  background-color: #5cb85c; /* Green for origin */
}
.destination-icon {
  background-color: #d9534f; /* Red for destination */
}

.route-connector {
  height: 20px; /* Space between icons if needed */
  width: 2px;
  /* background-image: linear-gradient(to bottom, #bbb 50%, transparent 50%);
  background-size: 2px 8px; */ /* Simple dashed line */
  margin-top: 5px;
  margin-bottom: 5px;
}

.point-details {
  flex-grow: 1;
}

.form-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.5;
  resize: vertical;
  min-height: 60px; /* Minimum height for textareas */
  box-sizing: border-box;
}
.form-textarea:focus {
  outline: none;
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.item-info-section, .task-amount-section {
  padding-top: 15px;
  border-top: 1px solid #e9ecef; /* Lighter separator */
}

.info-field {
  margin-bottom: 15px;
}
.info-field:last-child {
  margin-bottom: 0;
}

.info-field label {
  display: block;
  font-size: 14px;
  color: #495057;
  margin-bottom: 6px;
  font-weight: 500;
}

.screenshot-upload-area {
  width: 100%;
  min-height: 100px; /* Flexible height */
  border: 2px dashed #ced4da;
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background-color: #f8f9fa;
  color: #6c757d;
  font-size: 14px;
  text-align: center;
  padding: 15px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.screenshot-upload-area:hover {
  border-color: #007bff;
}
.upload-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
.upload-prompt svg {
  color: #6c757d;
}
.image-preview {
  max-width: 100%;
  max-height: 150px; /* Limit preview height */
  object-fit: contain;
  border-radius: 4px;
  margin-top: 10px;
}
.file-name-display {
  font-size: 12px;
  color: #333;
  margin-top: 8px;
  word-break: break-all;
}

.task-amount-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.task-amount-section label {
  font-size: 15px;
  color: #333;
  font-weight: 600;
}

.amount-input-group {
  display: flex;
  align-items: center;
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding-left: 10px;
}
.amount-input-group input {
  width: 80px;
  padding: 8px 0;
  border: none;
  text-align: right;
  font-size: 16px;
  font-weight: 600;
  color: #e63946; /* Distinct amount color */
}
.amount-input-group input:focus {
  outline: none;
}
.amount-input-group input::placeholder {
  color: #adb5bd;
  font-weight: normal;
}
.amount-input-group span {
  font-size: 15px;
  color: #495057;
  padding: 8px 10px 8px 5px;
  background-color: #e9ecef;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
}
</style>