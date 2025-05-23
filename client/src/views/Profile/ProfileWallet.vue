<template>
    <div class="page-container">
        <span class="back-icon" @click="$router.push('/profile')">
            <i class="fas fa-angle-left"></i>
        </span>
        <h2 class="title">钱包</h2>
    </div>
  <div class="profile-info">
    <div class="personal-info">
      <span class="icon1"><i class="fa fa-paypal"></i></span>
      <p class="description">零钱</p>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info last-info">
      <span class="icon1"><i class="fa fa-credit-card"></i></span>
      <p class="description">卡券</p>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
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
  padding: 20px;
  /* width: 100%; */
}

.personal-info {
  display: flex;
  justify-content: flex-start;
  border-top: 1px solid #e0e0e0;
  align-items: center;
  padding: 16px 0;
}

.last-info {
  border-bottom: 1px solid #e0e0e0;
}

.icon1 {
  font-size: 30px;
  padding: 0 10px 0 0;
  color:grey;
}

.description {
  flex-grow: 1;
  margin: 0 10px;
}

.icon2 {
  font-size: 30px;
  color:grey;
  cursor: pointer;
}
</style>