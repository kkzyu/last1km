<template>
  <div class="address-search">
    <a-auto-complete
      v-model:value="searchValue"
      :options="searchOptions"
      :loading="isSearching"
      :placeholder="placeholder"
      @search="handleSearch"
      @select="handleSelect"
      @blur="handleBlur"
      allowClear
    >
      <template #option="{ value, label, address, location }">
        <div class="search-option">
          <div class="option-name">{{ label }}</div>
          <div class="option-detail">{{ address }}</div>
        </div>
      </template>
    </a-auto-complete>
    
    <!-- 显示选中的地址信息 -->
    <div v-if="selectedAddress" class="selected-address">
      <a-tag color="blue" closable @close="clearSelection">
        <i class="fas fa-map-marker-alt"></i>
        {{ selectedAddress.name }}
      </a-tag>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps } from 'vue';
import { mapAPI } from '@/api/api';
import { message } from 'ant-design-vue';

const props = defineProps({
  value: String,
  placeholder: {
    type: String,
    default: '输入地址关键词搜索'
  },
  type: String // 'origin' | 'destination'
});

const emit = defineEmits(['update:value', 'address-selected']);

const searchValue = ref(props.value || '');
const searchOptions = ref([]);
const isSearching = ref(false);
const selectedAddress = ref(null);

// 防抖搜索
let searchTimeout = null;

const handleSearch = (value) => {
  if (!value.trim()) {
    searchOptions.value = [];
    return;
  }
  
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    searchPlaces(value);
  }, 300);
};

const searchPlaces = async (keyword) => {
  if (!keyword.trim()) return;
  
  isSearching.value = true;
  try {
    const response = await mapAPI.searchPlaces(keyword);
    if (response.data.success) {
      searchOptions.value = response.data.data.map(place => ({
        value: place.name,
        label: place.name,
        address: place.address,
        location: place.location // { lat, lng }
      }));
    }
  } catch (error) {
    console.error('地址搜索失败:', error);
    message.error('地址搜索失败，请重试');
  } finally {
    isSearching.value = false;
  }
};

const handleSelect = (value, option) => {
  selectedAddress.value = {
    name: option.label,
    address: option.address,
    location: option.location
  };
  
  emit('update:value', value);
  emit('address-selected', {
    name: option.label,
    address: option.address,
    location: option.location,
    type: props.type
  });
};

const clearSelection = () => {
  selectedAddress.value = null;
  searchValue.value = '';
  emit('update:value', '');
  emit('address-selected', null);
};

const handleBlur = () => {
  // 如果没有选中具体地址但有输入值，保持输入值
  if (!selectedAddress.value && searchValue.value) {
    emit('update:value', searchValue.value);
  }
};

watch(() => props.value, (newValue) => {
  searchValue.value = newValue || '';
  if (!newValue) {
    selectedAddress.value = null;
  }
});
</script>

<style scoped>
.search-option {
  padding: 8px 0;
}

.option-name {
  font-weight: 500;
  color: #262626;
  margin-bottom: 2px;
}

.option-detail {
  font-size: 12px;
  color: #8c8c8c;
}

.selected-address {
  margin-top: 8px;
}

.address-search :deep(.ant-select-selection-placeholder) {
  color: #bfbfbf;
}
</style>