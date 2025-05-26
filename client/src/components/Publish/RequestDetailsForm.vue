<template>  <a-form class="request-details-form" layout="vertical">
    <div class="task-header">
      <span class="task-title">委托 {{ index + 1 }}</span>
      <a-checkbox 
        :checked="request.selected"
        @change="(e) => $emit('update:request', { ...request, selected: e.target.checked })"
        class="task-checkbox"
      ></a-checkbox>
    </div>

    <a-row :gutter="16">
      <a-col :span="24">
        <a-form-item>
          <template #label>
            <div class="form-item-label-with-icon">
              <div class="point-icon origin-icon">起</div>
              <span>起点信息</span>
            </div>
          </template>
          <a-textarea
            v-model:value="computedOrigin"
            placeholder="选择添加起点，填写详细信息 (如蓝田北门外卖柜)"
            :rows="3"
            class="form-textarea"
          />
        </a-form-item>
      </a-col>
    </a-row>

    <a-row :gutter="16">
      <a-col :span="24">
        <a-form-item>
          <template #label>
            <div class="form-item-label-with-icon">
              <div class="point-icon destination-icon">终</div>
              <span>终点信息</span>
            </div>
          </template>
          <a-textarea
            v-model:value="computedDestination"
            placeholder="选择添加终点，填写详细信息 (如青溪一舍大厅)"
            :rows="3"
            class="form-textarea"
          />
        </a-form-item>
      </a-col>
    </a-row>

    <a-divider />


    <a-form-item label="订单截图">
      <a-upload
        v-model:file-list="fileList"
        name="image"
        list-type="picture-card"
        class="screenshot-uploader"
        :show-upload-list="true"
        :before-upload="beforeUpload"
        @change="handleUploadChange"
        @preview="handlePreview"
        accept="image/*"
      >
      <div v-if="fileList.length < 1">
        <PlusOutlined />
        <div style="margin-top: 8px">上传订单截图</div>
        <span style="font-size: 12px; color: #999;">*自动识别物品描述及取件信息</span>
      </div>
      </a-upload>
      <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handlePreviewCancel">
        <img alt="example" style="width: 100%" :src="previewImage" />
      </a-modal>
    </a-form-item>

    <a-form-item label="物品描述">
      <a-textarea v-model:value="computedDescription" placeholder="例如：商家名称+商品名称" :rows="2" />
    </a-form-item>
    <a-form-item label="取件信息">
      <a-textarea v-model:value="computedOrderInfo" placeholder="例如：外卖柜号, 取件码, 手机号后四位" :rows="3" />
    </a-form-item>

    <a-divider />

    <a-form-item label="委托金额">
      <a-input-number
        v-model:value="computedTaskAmount"
        :min="0"
        :step="0.01"
        placeholder="0.00"
        style="width: 100%"
      >
        <template #addonAfter>元</template>
      </a-input-number>
    </a-form-item>
  </a-form>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { PlusOutlined, EyeOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';

const props = defineProps({
  index: { type: Number, required: true },
  request: {
    type: Object,
    required: true
  }
});

const emit = defineEmits([
  'update:origin',
  'update:destination',
  'update:description',
  'update:orderInfo',
  'update:taskAmount',
  'update:selected',
  'update:image', // Added for image data
]);

// Computed properties for v-model two-way binding
const computedOrigin = computed({
  get: () => props.request.origin,
  set: (value) => emit('update:request', { ...props.request, origin: value })
});
const computedDestination = computed({
  get: () => props.request.destination,
  set: (value) => emit('update:request', { ...props.request, destination: value })
});
const computedDescription = computed({
  get: () => props.request.description,
  set: (value) => emit('update:request', { ...props.request, description: value })
});
const computedOrderInfo = computed({
  get: () => props.request.orderInfo,
  set: (value) => emit('update:request', { ...props.request, orderInfo: value })
});
const computedTaskAmount = computed({
  get: () => props.request.amount,
  set: (value) => {
    const numValue = parseFloat(value);
    emit('update:request', { ...props.request, amount: isNaN(numValue) ? 0 : numValue });
  }
});

// Image Upload Logic
const fileList = ref([]);
const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');

// Helper function to convert data URL to File object
function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
}

// Watch for prop changes to initialize fileList for existing images
watch(() => props.image, (newImage) => {
  if (newImage && newImage.url && newImage.name && !fileList.value.length) {
    // Convert data URL back to a File-like object for Ant Design Upload
    // Ant Design Upload expects an object with uid, name, status, and url (or thumbUrl)
     if (newImage.url.startsWith('data:')) {
        const file = dataURLtoFile(newImage.url, newImage.name);
        fileList.value = [{
            uid: '-1', // Static uid for existing image
            name: file.name,
            status: 'done',
            url: newImage.url, // Use the original data URL for preview
            originFileObj: file // Store the File object if needed for re-upload or processing
        }];
    } else { // If it's a direct URL (e.g., from a server)
         fileList.value = [{
            uid: '-1',
            name: newImage.name,
            status: 'done',
            url: newImage.url,
        }];
    }
  } else if (!newImage && fileList.value.length > 0){
      fileList.value = [];
  }
}, { immediate: true });


const getBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

const beforeUpload = (file) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('你只能上传 JPG/PNG 格式的图片!');
  }
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('图片大小必须小于 2MB!');
  }
  // If validation passes, we manually manage fileList, so return false to prevent auto-upload
  return false; // Prevent auto-upload, handle in handleChange
};

const handleUploadChange = async (info) => {
  // Remove file
  if (info.file.status === 'removed') {
    fileList.value = [];
    emit('update:image', null);
    return;
  }

  // Add or update file
  const file = info.file;
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isJpgOrPng || !isLt2M) {
    // Error messages are handled in beforeUpload, but if a file slips through or if we want to remove invalid from list:
    fileList.value = fileList.value.filter(f => f.uid !== file.uid);
    if (fileList.value.length === 0) emit('update:image', null); // Ensure image prop is cleared
    return;
  }
  
  if (file) {
      try {
        const dataUrl = await getBase64(file.originFileObj || file);
        fileList.value = [{ // Replace, only one image allowed
            uid: file.uid || '-1', // Use file.uid if available, else generate one
            name: file.name,
            status: 'done', // Mark as done for display purposes
            url: dataUrl, // For local preview
            originFileObj: file.originFileObj || file
        }];
        emit('update:image', { name: file.name, url: dataUrl, file: file.originFileObj || file });
      } catch (error) {
        message.error('图片处理失败');
        fileList.value = []; // Clear on error
        emit('update:image', null);
      }
  }
};

const handlePreviewCancel = () => {
  previewVisible.value = false;
};

const handlePreview = async (file) => {
  if (!file.url && !file.preview) {
    file.preview = await getBase64(file.originFileObj);
  }
  previewImage.value = file.url || file.preview;
  previewVisible.value = true;
  previewTitle.value = file.name || file.url.substring(file.url.lastIndexOf('/') + 1);
};

const validateForm = () => {
  const errors = [];
  if (!computedOrigin.value.trim()) {
    errors.push('请填写起点信息');
  }
  if (!computedDestination.value.trim()) {
    errors.push('请填写终点信息');
  }
  if (computedTaskAmount.value <= 0) {
    errors.push('委托金额必须大于0');
  }
  return errors;
};

const handleFormChange = () => {
  const errors = validateForm();
  if (errors.length === 0) {
    emit('update:request', { ...props.request });
  }
};

watch([computedOrigin, computedDestination, computedTaskAmount], () => {
  handleFormChange();
});

</script>

<style scoped>
.request-details-form {
  background-color: #ffffff;
  border-radius: 8px; /* Consistent with Ant Design cards */
  padding: 20px;
  /* box-shadow: 0 2px 8px rgba(0, 0, 0, 0.09); */ /* Subtle shadow */
  margin-bottom: 16px; /* Spacing between forms */
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0; /* Ant Design divider color */
}

.task-title {
  font-size: 18px; /* Slightly larger for clarity */
  font-weight: 600;
  color: #262626; /* Darker Ant Design text color */
}

.task-checkbox {
  /* Ant Design checkbox is already well-styled */
}

.form-item-label-with-icon {
  display: flex;
  align-items: center;
  gap: 8px; /* Space between icon and text */
}

.point-icon {
  width: 24px; /* Slightly smaller icons */
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px; /* Smaller font in icon */
  font-weight: bold;
  color: white;
  flex-shrink: 0; /* Prevent icon from shrinking */
}
.origin-icon {
  background-color: #52c41a; /* Ant Design success color */
}
.destination-icon {
  background-color: #ff4d4f; /* Ant Design error color */
}

/* Ensure textareas take full width within form items */
.request-details-form .ant-form-item-control-input-content .ant-input,
.request-details-form .ant-form-item-control-input-content .ant-input-number {
  width: 100%;
}
.form-textarea {
   /* Ant Textarea is styled well by default */
}

/* Style for the Upload component */
.screenshot-uploader > .ant-upload {
  width: 100%; /* Make the upload button area wider */
  min-height: 120px; /* Adjust height as needed */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.screenshot-uploader .ant-upload-list-picture-card-container {
  width: 100px; /* Adjust if needed */
  height: 100px; /* Adjust if needed */
}
.screenshot-uploader.ant-upload-picture-card-wrapper {
    display: flex;
    justify-content: center; /* Center the upload item if only one */
}


/* Custom divider styling if needed, though <a-divider /> is usually sufficient */
/* .ant-divider {
  margin-top: 16px;
  margin-bottom: 24px;
} */

/* General Form Item Styling */
.request-details-form .ant-form-item {
  margin-bottom: 18px; /* Consistent spacing */
}

.request-details-form .ant-form-item-label > label {
  font-weight: 500; /* Medium weight labels */
  color: #595959; /* Slightly lighter text for labels */
}

/* Input Number Styling */
.ant-input-number-group-addon {
  background-color: #fafafa; /* Lighter addon background */
}
</style>