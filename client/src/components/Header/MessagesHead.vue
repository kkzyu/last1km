<template>
  <header class="messages-header">
    <h3>消息列表</h3>
    <button 
      @click="$emit('mark-all-read')" 
      :disabled="!hasUnreadMessages"
      title="一键已读" 
      aria-label="一键已读"
    >
      <svg 
        xmlns="http://www.w3.org/2000/svg" 
        width="20" 
        height="20"
        viewBox="0 0 24 24" 
        stroke-width="2" 
        stroke="currentColor" 
        fill="none" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        class="icon-broom"
      >
        <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
        <path d="M19.285 14.763a1.973 1.973 0 .01 -2.791 .013l-9.142 -9.142a1.973 1.973 0 0 0 -2.791 -2.791l-.103 .086a1.973 1.973 0 0 0 -.086 2.894l9.142 9.142a1.973 1.973 0 0 0 2.894 .086l.086 -.103a1.973 1.973 0 0 0 -.209 -2.785z" />
        <path d="M4 21h16" />
        <path d="M7 21v-2a2 2 0 0 1 2 -2h6a2 2 0 0 1 2 2v2" />
      </svg>
      <!-- 结束：扫把 SVG 图标 -->
    </button>
  </header>
</template>

<script setup>
defineProps({
  hasUnreadMessages: Boolean
})
</script>

<style scoped>
.messages-header {
  /* background-color: #2196F3; */
  color: black;
  padding-left: 15px;
  padding-right: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.messages-header button {
  padding: 0.5rem; /* 调整 padding 适应图标大小 */
  color: black; /* SVG 的 stroke="currentColor" 会继承这个颜色 */
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: inline-flex; /* 帮助 SVG 在按钮内垂直居中 */
  align-items: center;
  justify-content: center;
  line-height: 1; /* 确保图标不会撑开按钮高度 */
}

</style>