<template>
    <div class="page-container">
        <span class="icon"><i class="fas fa-angle-left" @click="$router.push('/profile')"></i></span>
        <h2 class="title">设置</h2>
    </div>

    <div class="profile-info">
        <div class="personal-info last-info">
            <p class="description">消息通知</p>
            <span class="icon2"><i class="fas fa-angle-right"></i></span>
        </div>
    </div>
    <div class="account-actions">
        <button class="action-button switch" @click="$router.push('/profile/SwitchAccount')">
            切换账号
        </button>
        <button class="action-button logout">
            退出登录
        </button>
    </div>
</template>

<script setup>
</script>

<style scoped>
.page-container {
    display: flex;
    padding: 20px;
    text-align: center;
    justify-content: flex-start;
    align-items: center;
}

.icon {
    font-size: 30px;
    cursor: pointer;
    color: #333;
}

.title {
    width: 90%;
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
}

.profile-info {
    display: flex;
    flex-direction: column;
    padding: 0 20px;
}

.personal-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0;
    border-top: 1px solid #e0e0e0;
}

.last-info {
    border-bottom: 1px solid #e0e0e0;
}

.description {
    font-size: 1rem;
    color: #333;
    margin: 0;
}

.icon2 {
    font-size: 24px;
    color: #999;
    cursor: pointer;
}

.account-actions {
    position: absolute;
    bottom: 20px;
    left: 0;
    right: 0;
    padding: 0 20px;
    max-width: 450px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.action-button {
    padding: 14px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
}

.action-button:active {
    transform: scale(0.98);
}

.switch {
    background-color: #f5f5f5;
    color: #333;
}

.logout {
    background-color: #fff;
    color: #ff4444;
    border: 1px solid #ff4444;
}

/* For hover effects (optional) */
@media (hover: hover) {
    .switch:hover {
        background-color: #eaeaea;
    }
    .logout:hover {
        background-color: #ffeeee;
    }
}
</style>