<template>
    <div class="profile-setup">
        <div class="page-container">
            <span class="back-icon" @click="$router.push('/profile')">
                <i class="fas fa-angle-left"></i>
            </span>
            <h2 class="title">设置</h2>
        </div>

        <div class="profile-info">
            <div class="personal-info last-info" @click="goToNotificationSettings">
                <p class="description">消息通知</p>
                <span class="icon2"><i class="fas fa-angle-right"></i></span>
            </div>
            
            <!-- 可以添加更多设置项 -->
            <div class="personal-info" @click="goToPrivacySettings">
                <p class="description">隐私设置</p>
                <span class="icon2"><i class="fas fa-angle-right"></i></span>
            </div>
            
            <div class="personal-info" @click="goToAbout">
                <p class="description">关于我们</p>
                <span class="icon2"><i class="fas fa-angle-right"></i></span>
            </div>
        </div>
        
        <div class="account-actions">
            <button class="action-button switch" @click="switchAccount">
                切换账号
            </button>
            <button class="action-button logout" @click="showLogoutModal" :disabled="isLoggingOut">
                {{ isLoggingOut ? '退出中...' : '退出登录' }}
            </button>
        </div>

        <!-- 退出登录确认弹窗 -->
        <div v-if="logoutModalVisible" class="modal-overlay" @click="hideLogoutModal">
            <div class="modal-content" @click.stop>
                <div class="modal-header">
                    <h3>确认退出</h3>
                </div>
                <div class="modal-body">
                    <p>确定要退出当前账号吗？</p>
                </div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" @click="hideLogoutModal">取消</button>
                    <button class="btn btn-danger" @click="confirmLogout" :disabled="isLoggingOut">
                        {{ isLoggingOut ? '退出中...' : '确认退出' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user.js';
import { message } from 'ant-design-vue';

const router = useRouter();
const userStore = useUserStore();

// 响应式数据
const logoutModalVisible = ref(false);
const isLoggingOut = ref(false);

// 显示退出登录确认弹窗
const showLogoutModal = () => {
    logoutModalVisible.value = true;
};

// 隐藏退出登录确认弹窗
const hideLogoutModal = () => {
    logoutModalVisible.value = false;
};

// 确认退出登录
const confirmLogout = async () => {
    try {
        isLoggingOut.value = true;
        
        // 清除用户数据
        userStore.logout();
        
        // 清除本地存储
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
        
        // 显示成功消息
        message.success('已成功退出登录');
        
        // 跳转到登录页面
        router.replace('/login');
        
    } catch (error) {
        console.error('退出登录失败:', error);
        message.error('退出登录失败，请重试');
    } finally {
        isLoggingOut.value = false;
        logoutModalVisible.value = false;
    }
};

// 切换账号
const switchAccount = () => {
    // 清除当前用户数据
    userStore.logout();
    localStorage.removeItem('authToken');
    localStorage.removeItem('userInfo');
    
    message.info('请登录其他账号');
    router.replace('/login');
};

// 跳转到消息通知设置
const goToNotificationSettings = () => {
    message.info('消息通知设置功能开发中...');
    // router.push('/profile/notification-settings');
};

// 跳转到隐私设置
const goToPrivacySettings = () => {
    message.info('隐私设置功能开发中...');
    // router.push('/profile/privacy-settings');
};

// 跳转到关于我们
const goToAbout = () => {
    message.info('关于我们功能开发中...');
    // router.push('/profile/about');
};
</script>

<style scoped>
.profile-setup {
    max-width: 390px;
    margin: 0 auto;
    min-height: 900px;
    background-color: #f5f5f7;
    position: relative;
}

.page-container {
    display: flex;
    padding: 20px;
    align-items: center;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 0;
    z-index: 10;
}

.back-icon {
    font-size: 18px;
    color: #333;
    cursor: pointer;
    transition: color 0.2s;
    margin-right: 15px;
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

.profile-info {
    display: flex;
    flex-direction: column;
    padding: 0 20px;
    margin-top: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.personal-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 0;
    border-bottom: 1px solid #f0f0f0;
    cursor: pointer;
    transition: background-color 0.2s;
}

.personal-info:hover {
    background-color: #f8f9fa;
}

.personal-info:last-child {
    border-bottom: none;
}

.description {
    font-size: 16px;
    color: #333;
    margin: 0;
    font-weight: 500;
}

.icon2 {
    font-size: 16px;
    color: #999;
}

.account-actions {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: calc(100% - 40px);
    max-width: 350px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 0 20px;
}

.action-button {
    padding: 14px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}

.action-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.action-button:active:not(:disabled) {
    transform: scale(0.98);
}

.switch {
    background-color: #f5f5f5;
    color: #333;
}

.switch:hover:not(:disabled) {
    background-color: #eaeaea;
}

.logout {
    background-color: #fff;
    color: #ff4444;
    border: 1px solid #ff4444;
}

.logout:hover:not(:disabled) {
    background-color: #ffeeee;
}

/* Modal 样式 */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background-color: #fff;
    border-radius: 8px;
    width: 90%;
    max-width: 320px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
    padding: 20px 20px 10px;
    border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
}

.modal-body {
    padding: 20px;
}

.modal-body p {
    margin: 0;
    font-size: 16px;
    color: #666;
    line-height: 1.5;
}

.modal-footer {
    padding: 10px 20px 20px;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.btn-secondary {
    background-color: #f5f5f5;
    color: #666;
}

.btn-secondary:hover:not(:disabled) {
    background-color: #e8e8e8;
}

.btn-danger {
    background-color: #ff4444;
    color: white;
}

.btn-danger:hover:not(:disabled) {
    background-color: #e63939;
}

/* 响应式设计 */
@media (max-width: 420px) {
    .profile-setup {
        max-width: 100%;
    }
    
    .account-actions {
        width: calc(100% - 40px);
    }
    
    .modal-content {
        width: 95%;
    }
}
</style>