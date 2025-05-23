<template>
    <div class="personal-portrait">
      <div class="avatar-container">
        <img class="avatar" src="/images/ProfilePortrait.jpg" alt="User avatar" />
      </div>
      <div class="user-info">
        <span class="username">kkzyu</span>
        <span class="gender-icon"><i class="fas fa-venus"></i></span>
      </div>
    </div>
  </template>
  
  <style scoped>
  .personal-portrait {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    margin: 20px 0 0 5px;
  }
  
  .avatar-container {
    flex-shrink: 0;
  }
  
  .avatar {
    object-fit: cover;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    border: 2px solid #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .username {
    font-size: 1.1rem;
    font-weight: 500;
    color: #333;
  }
  
  .gender-icon {
    color: deeppink;
    font-size: 0.9rem;
  }
  
  /* Responsive adjustments */
  @media (max-width: 480px) {
    .avatar {
      width: 50px;
      height: 50px;
    }
    
    .username {
      font-size: 1rem;
    }
  }
  </style>