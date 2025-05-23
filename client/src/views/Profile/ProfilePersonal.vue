<template>
    <div class="page-container">
        <span class="back-icon" @click="$router.push('/profile')">
            <i class="fas fa-angle-left"></i>
        </span>
        <h2 class="title">个人资料</h2>
    </div>

    <!-- 个人信息列表 -->
    <div class="profile-list">
      <!-- 头像 -->
      <div class="profile-item">
        <span class="item-label">头像</span>
        <div class="item-content">
          <img class="avatar" src="/images/ProfilePortrait.jpg" alt="用户头像" />
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <!-- 昵称 -->
      <div class="profile-item">
        <span class="item-label">昵称</span>
        <div class="item-content">
          <span class="item-value">kkzyu</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <!-- 性别 -->
      <div class="profile-item">
        <span class="item-label">性别</span>
        <div class="item-content">
          <span class="item-value">女</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <!-- 手机号 -->
      <div class="profile-item">
        <span class="item-label">手机号</span>
        <div class="item-content">
          <span class="item-value">135******22</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>

      <!-- 地址 -->
      <div class="profile-item last-item">
        <span class="item-label">地址</span>
        <div class="item-content">
          <span class="item-value">浙江 杭州***</span>
          <i class="fas fa-angle-right arrow-icon"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 基础样式 */
.page-container {
    display: flex;
    padding: 20px;
    align-items: center;
    background-color: #f8f9fa;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 0;
    z-index: 10;
}

.back-icon {
    font-size: 24px;
    color: #333;
    cursor: pointer;
    transition: color 0.2s;
}

.back-icon:hover {
    color: #1890ff;
}

.title {
    flex: 1;
    text-align: center;
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
}
/* 列表样式 */
.profile-list {
  padding: 0 16px;
}

.profile-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f5f5f5;
}

.last-item {
  border-bottom: 1px solid #e0e0e0;
}

.item-label {
  font-size: 16px;
  color: #333;
}

.item-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.item-value {
  font-size: 14px;
  color: #666;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #f0f0f0;
}

.arrow-icon {
  color: #999;
  font-size: 14px;
}

/* 交互效果 */
.back-button:hover,
.profile-item:hover {
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .profile-header {
    padding: 12px;
  }
  
  .profile-item {
    padding: 12px 0;
  }
  
  .item-label {
    font-size: 15px;
  }
  
  .item-value {
    font-size: 13px;
  }
  
  .avatar {
    width: 36px;
    height: 36px;
  }
}
</style>