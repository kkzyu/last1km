<template>
  <a-form class="request-details-form" layout="vertical">
    <div class="task-header">
      <span class="task-title">委托 {{ index + 1 }}</span>
      <a-checkbox 
        :checked="request.selected"
        @change="(e) => emitUpdateRequest({ ...request, selected: e.target.checked })"
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
        <span style="font-size: 12px; color: #999;">*可自动识别部分信息</span>
      </div>
      </a-upload>
      <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handlePreviewCancel">
        <img alt="预览图片" style="width: 100%" :src="previewImage" />
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
import { PlusOutlined } from '@ant-design/icons-vue'; // EyeOutlined 未使用，已移除
import { message } from 'ant-design-vue';
import { orderAPI } from '@/api/api'; // **新增：导入 orderAPI**

const props = defineProps({
  index: { type: Number, required: true },
  request: {
    type: Object,
    required: true,
    default: () => ({ // **为request prop添加default，确保其始终是对象**
        origin: '',
        destination: '',
        description: '',
        orderInfo: '',
        amount: 0,
        selected: true,
        image: null // 图片字段，用于存储后端返回的文件名
    })
  }
});

// **统一 emit 事件**
const emit = defineEmits(['update:request']);

// **封装 emit 调用**
const emitUpdateRequest = (updatedFields) => {
  emit('update:request', { ...props.request, ...updatedFields });
};

// Computed properties for v-model two-way binding
const computedOrigin = computed({
  get: () => props.request.origin,
  set: (value) => emitUpdateRequest({ origin: value })
});
const computedDestination = computed({
  get: () => props.request.destination,
  set: (value) => emitUpdateRequest({ destination: value })
});
const computedDescription = computed({
  get: () => props.request.description,
  set: (value) => emitUpdateRequest({ description: value })
});
const computedOrderInfo = computed({
  get: () => props.request.orderInfo,
  set: (value) => emitUpdateRequest({ orderInfo: value })
});
const computedTaskAmount = computed({
  get: () => props.request.amount,
  set: (value) => {
    const numValue = parseFloat(value);
    emitUpdateRequest({ amount: isNaN(numValue) ? 0 : numValue });
  }
});

// Image Upload Logic
const fileList = ref([]); // 用于a-upload组件显示
const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');

const API_BASE_URL = 'http://localhost:5000'; // **定义API基础URL，用于拼接图片路径**

// **监听 props.request.image (存储的是后端返回的文件名)**
watch(() => props.request.image, (newImageFilename) => {
  if (newImageFilename && typeof newImageFilename === 'string') {
    // 如果文件名存在，构建用于预览的完整URL，并更新fileList
    fileList.value = [{
      uid: '-1', // 对于已存在的图片使用静态uid
      name: newImageFilename, // 可以显示文件名
      status: 'done',
      url: `${API_BASE_URL}/static/uploads/${newImageFilename}` // 构建预览URL
    }];
  } else if (!newImageFilename && fileList.value.length > 0) {
    // 如果 props.request.image 被清空 (例如，父组件重置)，也清空fileList
    fileList.value = [];
  }
}, { immediate: true });


const getBase64 = (file) => { // 预览时可能还需要
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
  // 返回 false 以阻止 antd 的默认上传行为，我们将在 handleChange 中手动上传
  return false; 
};

const handleUploadChange = async (info) => {
  // fileList.value = [...info.fileList]; // 同步 antd 的 fileList (可选，但有助于显示)

  const currentFile = info.file;

  // 处理文件移除
  if (currentFile.status === 'removed') {
    fileList.value = []; // 清空显示的列表
    emitUpdateRequest({ image: null }); // 更新父组件，将图片设为null
    return;
  }

  // 如果文件状态不是 'uploading' (antd可能会在beforeUpload返回false后设置它), 
  // 或者不是我们手动添加的，就先把它加入列表（如果需要预览本地选择的文件）
  // 但主要逻辑是处理新文件并上传
  // 我们只处理最新的文件，因为只允许上传一张图片

  // 确保我们只处理用户新选择的文件 (通常是 info.fileList 的最后一个)
  // 并且这个文件有 originFileObj (原始 File 对象)
  const fileToUpload = currentFile.originFileObj || currentFile;

  if (!fileToUpload || !(fileToUpload instanceof File)) {
    // console.warn("No valid file to upload or already uploaded.");
    // 如果 fileList 已经被 watch 更新，或者没有真实文件对象，则不重复上传
    // 但我们需要确保 fileList 和 props.request.image 同步
    // 如果 props.request.image 已经有值，并且 fileList 也正确显示，这里可以不处理
    return;
  }
  
  // 再次校验（虽然beforeUpload已做，但作为保险）
  const isJpgOrPng = fileToUpload.type === 'image/jpeg' || fileToUpload.type === 'image/png';
  const isLt2M = fileToUpload.size / 1024 / 1024 < 2;

  if (!isJpgOrPng || !isLt2M) {
    message.error('图片格式或大小不符合要求，已取消上传。');
    // 从 fileList (如果 antd 自动添加了) 中移除无效文件
    fileList.value = fileList.value.filter(f => f.uid !== currentFile.uid); 
    if (fileList.value.length === 0) {
        emitUpdateRequest({ image: null });
    }
    return;
  }

  // --- 开始上传 ---
  const formData = new FormData();
  formData.append('image', fileToUpload);

  // 更新fileList以显示加载状态 (Ant Design Upload 会自动处理一部分)
  // 我们可以手动标记为 'uploading'
   const tempFileEntry = {
        uid: currentFile.uid || Date.now().toString(), // 确保有uid
        name: fileToUpload.name,
        status: 'uploading',
        percent: 50, // 模拟上传进度
   };
   fileList.value = [tempFileEntry];


  try {
    const response = await orderAPI.uploadOrderImage(formData);
    if (response.data && response.data.success) {
      const serverFilename = response.data.data.filename; // 从后端获取文件名
      emitUpdateRequest({ image: serverFilename }); // **更新父组件，传递文件名**
      
      // 更新 fileList 以正确显示已上传的图片，并用于预览
      fileList.value = [{
        uid: tempFileEntry.uid, //保持uid
        name: fileToUpload.name,
        status: 'done',
        url: `${API_BASE_URL}/static/uploads/${serverFilename}`, // **用于预览的完整URL**
        originFileObj: fileToUpload // 保留原始文件对象，预览时可能需要
      }];
      message.success('图片上传成功!');
    } else {
      throw new Error(response.data.message || '图片上传失败');
    }
  } catch (error) {
    message.error(error.message || '图片上传失败');
    fileList.value = fileList.value.filter(f => f.status !== 'uploading'); // 移除上传中的占位
    if(fileList.value.length === 0) { // 如果之前没有成功上传的图片，则清空
        emitUpdateRequest({ image: null });
    }
  }
};

const handlePreviewCancel = () => {
  previewVisible.value = false;
};

const handlePreview = async (file) => {
  if (!file.url && !file.preview && file.originFileObj) { // 如果没有url，尝试从originFileObj生成base64预览
    try {
        file.preview = await getBase64(file.originFileObj);
    } catch (e) {
        message.error('无法预览图片');
        return;
    }
  }
  previewImage.value = file.url || file.preview; // 优先使用服务器URL
  previewVisible.value = true;
  previewTitle.value = file.name || (file.url ? file.url.substring(file.url.lastIndexOf('/') + 1) : '图片预览');
};

// 移除了 validateForm 和相关的 watch，因为每个字段都通过 computed set 直接 emit 更新
// 表单的整体校验应该在父组件提交时进行，或者如果需要实时校验，可以另行实现
</script>

<style scoped>
/* 样式与您提供的一致，仅作微调和注释 */
.request-details-form {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 16px;
}
.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f0f0f0;
}
.task-title {
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}
.form-item-label-with-icon {
  display: flex;
  align-items: center;
  gap: 8px;
}
.point-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}
.origin-icon { background-color: #52c41a; }
.destination-icon { background-color: #ff4d4f; }

.request-details-form .ant-form-item { margin-bottom: 18px; }
.request-details-form .ant-form-item-label > label { font-weight: 500; color: #595959; }

/* 使 Ant Design Upload 组件的上传按钮区域更友好 */
.screenshot-uploader :deep(.ant-upload.ant-upload-select-picture-card) {
  width: 100%; /* 宽度占满 */
  height: 100px; /* 固定高度 */
  margin-bottom: 8px; /* 如果有已上传图片，与列表的间距 */
}
.screenshot-uploader :deep(.ant-upload-list-picture-card .ant-upload-list-item) {
  width: 100px; /* 预览图大小 */
  height: 100px; /* 预览图大小 */
}
</style>