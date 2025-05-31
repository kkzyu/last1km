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
        <span style="font-size: 12px; color: #999;">*可自动识别商家、商品和取件信息</span>
      </div>
      </a-upload>

      <div v-if="fileList.length > 0" class="ai-controls">
        <a-button 
          size="small" 
          type="link" 
          :loading="isAnalyzing"
          @click="reAnalyzeImage"
          :disabled="!props.request.image"
        >
          <i class="fas fa-robot"></i>
          {{ isAnalyzing ? 'AI识别中...' : '重新AI识别' }}
        </a-button>
        <span v-if="hasAnalyzed" class="analyzed-tip">
          <i class="fas fa-check-circle"></i>
          已完成AI识别
        </span>
        
        <!-- 显示识别到的原始文本（调试用） -->
        <a-button 
          v-if="recognizedText && showDebugInfo" 
          size="small" 
          type="text" 
          @click="showRawText = !showRawText"
        >
          {{ showRawText ? '隐藏' : '查看' }}识别文本
        </a-button>
      </div>

      <!-- 显示原始识别文本（调试用） -->
      <div v-if="showRawText && recognizedText" class="debug-text">
        <h4>原始识别文本：</h4>
        <pre>{{ recognizedText }}</pre>
      </div>

      <a-modal :open="previewVisible" :title="previewTitle" :footer="null" @cancel="handlePreviewCancel">
        <img alt="预览图片" style="width: 100%" :src="previewImage" />
      </a-modal>
    </a-form-item>

    <a-form-item>
      <template #label>
        <span>物品描述</span>
        <a-tooltip title="商家名称 + 主要商品名称">
          <i class="fas fa-question-circle" style="margin-left: 4px; color: #999;"></i>
        </a-tooltip>
      </template>
      <a-textarea 
        v-model:value="computedDescription" 
        placeholder="例如：山离家砂锅鲜烧饺 - 卤烧鸡翅尖·砂锅鲜烧饺单人份" 
        :rows="2" 
      />
    </a-form-item>
    
    <a-form-item>
      <template #label>
        <span>取件信息</span>
        <a-tooltip title="外卖柜位置、取件码、联系方式等">
          <i class="fas fa-question-circle" style="margin-left: 4px; color: #999;"></i>
        </a-tooltip>
      </template>
      <a-textarea 
        v-model:value="computedOrderInfo" 
        placeholder="例如：蓝田(东门)蓝田外卖柜 alanni ****1847" 
        :rows="3" 
      />
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
import { PlusOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { orderAPI } from '@/api/api';

const props = defineProps({
  index: { type: Number, required: true },
  request: {
    type: Object,
    required: true,
    default: () => ({
        origin: '',
        destination: '',
        description: '',
        orderInfo: '',
        amount: 0,
        selected: true,
        image: null
    })
  }
});

const emit = defineEmits(['update:request']);

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
const fileList = ref([]);
const previewVisible = ref(false);
const previewImage = ref('');
const previewTitle = ref('');

const isAnalyzing = ref(false);
const hasAnalyzed = ref(false);
const recognizedText = ref(''); // 存储原始识别文本
const showRawText = ref(false); // 控制是否显示原始文本
const showDebugInfo = ref(process.env.NODE_ENV === 'development'); // 只在开发环境显示调试信息

const API_BASE_URL = 'http://localhost:5000';

// 监听 props.request.image
watch(() => props.request.image, (newImageFilename) => {
  if (newImageFilename && typeof newImageFilename === 'string') {
    fileList.value = [{
      uid: '-1',
      name: newImageFilename,
      status: 'done',
      url: `${API_BASE_URL}/static/uploads/${newImageFilename}`
    }];
  } else if (!newImageFilename && fileList.value.length > 0) {
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
  return false; 
};

const handleUploadChange = async (info) => {
  const currentFile = info.file;

  if (currentFile.status === 'removed') {
    fileList.value = [];
    emitUpdateRequest({ image: null });
    recognizedText.value = ''; // 清空识别文本
    hasAnalyzed.value = false; // 重置分析状态
    return;
  }

  const fileToUpload = currentFile.originFileObj || currentFile;

  if (!fileToUpload || !(fileToUpload instanceof File)) {
    return;
  }
  
  const isJpgOrPng = fileToUpload.type === 'image/jpeg' || fileToUpload.type === 'image/png';
  const isLt2M = fileToUpload.size / 1024 / 1024 < 2;

  if (!isJpgOrPng || !isLt2M) {
    message.error('图片格式或大小不符合要求，已取消上传。');
    fileList.value = fileList.value.filter(f => f.uid !== currentFile.uid); 
    if (fileList.value.length === 0) {
        emitUpdateRequest({ image: null });
    }
    return;
  }

  const formData = new FormData();
  formData.append('image', fileToUpload);

  const tempFileEntry = {
        uid: currentFile.uid || Date.now().toString(),
        name: fileToUpload.name,
        status: 'uploading',
        percent: 50,
   };
   fileList.value = [tempFileEntry];

  try {
    console.log('开始上传图片...');
    const response = await orderAPI.uploadOrderImage(formData);
    if (response.data && response.data.success) {
      const serverFilename = response.data.data.filename;
      emitUpdateRequest({ image: serverFilename });
      
      fileList.value = [{
        uid: tempFileEntry.uid,
        name: fileToUpload.name,
        status: 'done',
        url: `${API_BASE_URL}/static/uploads/${serverFilename}`,
        originFileObj: fileToUpload
      }];
      message.success('图片上传成功!');

      console.log('图片上传成功，等待500ms后开始AI分析...');
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const token = localStorage.getItem('authToken');
      if (!token) {
        message.error('认证信息在上传过程中丢失，请重新登录');
        return;
      }

      await analyzeOrderImage(serverFilename);
    } else {
      throw new Error(response.data.message || '图片上传失败');
    }
  } catch (error) {
    console.error('上传错误:', error);
    message.error(error.message || '图片上传失败');
    fileList.value = fileList.value.filter(f => f.status !== 'uploading');
    if(fileList.value.length === 0) {
        emitUpdateRequest({ image: null });
    }
  }
};

const analyzeOrderImage = async (filename) => {
  if (!filename) {
    message.warning('请先上传订单截图');
    return;
  }

  const token = localStorage.getItem('authToken');

  if (!token) {
    message.error('认证信息丢失，请重新登录');
    window.location.href = '/login';
    return;
  }

  isAnalyzing.value = true;
  
  // 使用更可靠的loading处理方式
  let loadingMessage;
  try {
    loadingMessage = message.loading('AI正在识别订单信息...', 0);
  } catch (e) {
    console.warn('创建loading消息失败:', e);
  }

  try {
    console.log('准备调用AI分析API，文件名:', filename);
    const response = await orderAPI.analyzeOrderImage({ filename });
    
    console.log('AI分析响应:', response);
    
    if (response.data && response.data.success) {
      const { description, orderInfo, recognizedText: rawText } = response.data.data;
      
      // 存储原始识别文本用于调试
      recognizedText.value = rawText || '';
      
      // 只有当字段为空时才自动填充，避免覆盖用户已输入的内容
      const updates = {};
      
      if (description && !props.request.description) {
        updates.description = description;
      }
      if (orderInfo && !props.request.orderInfo) {
        updates.orderInfo = orderInfo;
      }
      
      if (Object.keys(updates).length > 0) {
        emitUpdateRequest(updates);
        hasAnalyzed.value = true;
        
        // 先关闭loading再显示成功消息
        if (loadingMessage) {
          try {
            message.destroy(loadingMessage);
          } catch (e) {
            console.warn('销毁loading消息失败:', e);
          }
          loadingMessage = null;
        }
        
        message.success('AI识别完成！已自动填充订单信息');
        
        // 在开发环境下显示详细信息
        if (showDebugInfo.value) {
          console.log('AI识别结果:', {
            description,
            orderInfo,
            rawText
          });
        }
      } else {
        hasAnalyzed.value = true;
        
        // 先关闭loading再显示提示消息
        if (loadingMessage) {
          try {
            message.destroy(loadingMessage);
          } catch (e) {
            console.warn('销毁loading消息失败:', e);
          }
          loadingMessage = null;
        }
        
        message.info('AI识别完成，但未检测到新信息或信息已存在');
      }
    } else {
      throw new Error(response.data.message || 'AI识别失败');
    }
  } catch (error) {
    console.error('AI分析详细错误:', {
      message: error.message,
      response: error.response,
      stack: error.stack
    });
    
    // 先关闭loading再显示错误消息
    if (loadingMessage) {
      try {
        message.destroy(loadingMessage);
      } catch (e) {
        console.warn('销毁loading消息失败:', e);
      }
      loadingMessage = null;
    }
    
    if (error.response?.status === 500) {
      message.error('AI识别服务暂时不可用，请手动填写信息');
    } else if (error.message.includes('认证失败') || error.message.includes('Token')) {
      message.error('登录状态已过期，请重新登录');
      localStorage.removeItem('authToken');
      localStorage.removeItem('userInfo');
      setTimeout(() => {
        window.location.href = '/login';
      }, 1500);
    } else {
      message.error('AI识别失败，请手动填写信息');
    }
  } finally {
    // 确保在任何情况下都清除状态
    isAnalyzing.value = false;
    
    // 最后的保险措施：如果loading消息还存在，强制清除
    if (loadingMessage) {
      try {
        message.destroy(loadingMessage);
      } catch (e) {
        console.warn('最终销毁loading消息失败:', e);
      }
    }
    
    // 强制清除所有loading类型的消息
    try {
      message.destroy();
    } catch (e) {
      console.warn('清除所有消息失败:', e);
    }
  }
};

const reAnalyzeImage = async () => {
  if (!props.request.image) {
    message.warning('请先上传订单截图');
    return;
  }
  
  // 确保重置状态
  isAnalyzing.value = false;
  hasAnalyzed.value = false;
  recognizedText.value = '';
  
  // 清除可能存在的消息
  try {
    message.destroy();
  } catch (e) {
    console.warn('清除消息失败:', e);
  }
  
  // 短暂延迟后开始分析
  await new Promise(resolve => setTimeout(resolve, 100));
  await analyzeOrderImage(props.request.image);
};

const handlePreviewCancel = () => {
  previewVisible.value = false;
};

const handlePreview = async (file) => {
  if (!file.url && !file.preview && file.originFileObj) {
    try {
        file.preview = await getBase64(file.originFileObj);
    } catch (e) {
        message.error('无法预览图片');
        return;
    }
  }
  previewImage.value = file.url || file.preview;
  previewVisible.value = true;
  previewTitle.value = file.name || (file.url ? file.url.substring(file.url.lastIndexOf('/') + 1) : '图片预览');
};
</script>

<style scoped>
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
.ai-controls {
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.analyzed-tip {
  font-size: 12px;
  color: #52c41a;
  display: flex;
  align-items: center;
  gap: 4px;
}

.ai-controls .ant-btn-link {
  padding: 0;
  height: auto;
  font-size: 12px;
}

.debug-text {
  margin-top: 12px;
  padding: 12px;
  background-color: #f5f5f5;
  border-radius: 6px;
  border-left: 4px solid #1890ff;
}

.debug-text h4 {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.debug-text pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 12px;
  color: #333;
  background: none;
}

.origin-icon { background-color: #52c41a; }
.destination-icon { background-color: #ff4d4f; }

.request-details-form .ant-form-item { margin-bottom: 18px; }
.request-details-form .ant-form-item-label > label { font-weight: 500; color: #595959; }

.screenshot-uploader :deep(.ant-upload.ant-upload-select-picture-card) {
  width: 100%;
  height: 100px;
  margin-bottom: 8px;
}
.screenshot-uploader :deep(.ant-upload-list-picture-card .ant-upload-list-item) {
  width: 100px;
  height: 100px;
}
</style>