<template>
    <div class="page-container">
        <span class="back-icon" @click="$router.push('/profile')">
            <i class="fas fa-angle-left"></i>
        </span>
        <h2 class="title">切换账号</h2>
    </div>

    <div class="profile-info">
        <div class="personal-info last-info">
            <p class="description"><img class="img" src="/images/ProfilePortrait.jpg" /> kkzyu</p>
            <span class="icon2">当前使用</span>
        </div>
        <div class="personal-info last-info">
            <p class="description"><span class="icon1"><i class="fa fa-plus-square-o"></i></span> 添加账号</p>
        </div>
    </div>
</template>

<script setup>
</script>

<style scoped>
@import url("https://lf3-cdn-tos.bytecdntp.com/cdn/expire-1-M/font-awesome/4.7.0/css/font-awesome.min.css");

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
    justify-content: space-between;
    padding: 20px;
    /* width: 100%; */
}

.personal-info {
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e0e0e0;
    align-items: center;
    padding: 16px 0;
}

.last-info {
    border-bottom: 1px solid #e0e0e0;
}

.description {
    display: flex;
    justify-content: start;
    align-items: center;
    gap: 10px;
}

.icon1 {
  font-size: 30px;
  color:grey;
  margin-left: 10px;
}

.icon2 {
    font-size: 20px;
    color: #02A7F0;
    cursor: pointer;
    display: flex;
    justify-content: end;
}

.img {
    object-fit: cover;
    border-radius: 50%;
    width: min(20vw, 40px);
    height: min(20vw, 40px);
}
</style>