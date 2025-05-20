<template>
  <div class="page-container">
    <span class="icon"><i class="fas fa-angle-left" @click="$router.push('/profile')"></i></span>
    <h2 class="title">钱包</h2>
  </div>
  
  <div class="profile-info">
    <div class="personal-info">
      <span class="icon1"><i class="fa fa-paypal"></i></span>
      <p class="description">零钱</p>
      <div class="empty-box"></div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info last-info">
      <span class="icon1"><i class="fa fa-credit-card"></i></span>
      <p class="description">卡券</p>
      <div class="empty-box"></div>
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
  text-align: center;
  justify-content: flex-start;
  align-items: center;
}

.icon {
  font-size: 30px;
  cursor: pointer;
}

.title {
    width: 90%;
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
}

.last-info {
  border-bottom: 1px solid #e0e0e0;
}

.icon1 {
  font-size: 30px;
  padding: 0 10px 0 0;
  color:grey;
  width: 10%;
}

.description {
  width: 30%;
}

.empty-box {
  width: 50%;
}

.icon2 {
  font-size: 30px;
  color:grey;
  cursor: pointer;
}
</style>