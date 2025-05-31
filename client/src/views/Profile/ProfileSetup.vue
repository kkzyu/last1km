<template>
    <div class="page-container">
        <span class="back-icon" @click="$router.push('/profile')">
            <i class="fas fa-angle-left"></i>
        </span>
        <h2 class="title">设置</h2>
    </div>

    <div class="profile-info">
        <div class="personal-info last-info">
            <p class="description">消息通知</p>
            <span class="icon2"><i class="fas fa-angle-right"></i></span>
        </div>
    </div>
    <!-- Removed account actions -->
</template>

<script setup>
</script>

<style scoped>
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

.profile-info {
    display: flex;
    flex-direction: column;
    padding: 0 20px;
}

.personal-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 0;
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

/* Removed styles for .account-actions, .action-button, .switch, .logout */
</style>