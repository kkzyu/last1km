<template>
  <div class="page-container">
    <span class="icon1"><i class="fas fa-angle-left" @click="$router.push('/profile')"></i></span>
    <h2 class="title">个人资料</h2>
  </div>
  <div class="profile-info">
    <div class="personal-info">
      <p class="description">头像</p>
      <div class="empty-box"></div>
      <div class="info">
        <img class="img" src="/images/ProfilePortrait.jpg" />
      </div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info">
      <p class="description">昵称</p>
      <div class="empty-box"></div>
      <div class="info">
        kkzyu
      </div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info">
      <p class="description">性别</p>
      <div class="empty-box"></div>
      <div class="info">
        女
      </div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info">
      <p class="description">手机号</p>
      <div class="empty-box"></div>
      <div class="info">
        135******22
      </div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>

    <div class="personal-info last-info">
      <p class="description">地址</p>
      <div class="empty-box"></div>
      <div class="info">
        浙江 杭州***
      </div>
      <span class="icon2"><i class="fas fa-angle-right"></i></span>
    </div>
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

.empty-box {
  width: 60%;
}

.description {
    width: 20%;
}

.info {
    width: 40%;
    text-align: center;
}

.img {
    object-fit: cover;
    border-radius: 50%;
    width: min(20vw, 40px);
    height: min(20vw, 40px);
}

.icon1 {
  font-size: 30px;
  cursor: pointer;
}

.title {
    width: 90%;
}

.last-info {
  border-bottom: 1px solid #e0e0e0;
}
</style>