<template>
    <div class="page-container">
        <span class="back-icon" @click="$router.push('/profile')">
            <i class="fas fa-angle-left"></i>
        </span>
        <h2 class="title">历史订单</h2>
    </div>
    
    <div class="orders-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
            <div v-if="order.status === '已完成'" class="order-content">
                <div class="order-header">
                    <span class="order-id">订单 #{{ order.id }}</span>
                    <span class="order-status completed">{{ order.status }}</span>
                </div>
                <div class="order-details">
                    <div class="detail-item">
                        <i class="fa fa-clock-o"></i>
                        <span>{{ order.date }}</span>
                    </div>
                    <div class="detail-item">
                        <i class="fa fa-shopping-bag"></i>
                        <span>{{ order.items }}件商品</span>
                    </div>
                    <div class="detail-item total-price">
                        <i class="fa fa-cny"></i>
                        <span>{{ order.total }}</span>
                    </div>
                </div>
                
                <div class="rating-section">
                    <span class="rating-prompt">评价订单</span>
                    <div class="stars">
                        <span v-for="n in 5" :key="n" @click="rateOrder(order.id, n)">
                            <i class="fa fa-star" :class="{ 'rated': n <= (order.rating || 0) }"></i>
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import information from '@/assets/data/information.json'

const orders = information.orders

const rateOrder = (orderId, rating) => {
    // 这里可以添加评价逻辑
    console.log(`订单 ${orderId} 评价为 ${rating} 星`);
}
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

.orders-list {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.order-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.order-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.order-content {
    padding: 16px;
}

.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 1px solid #f0f0f0;
}

.order-id {
    font-weight: 600;
    color: #333;
}

.order-status {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
}

.order-status.completed {
    background-color: #e6f7ff;
    color: #1890ff;
}

.order-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
}

.detail-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #666;
    font-size: 14px;
}

.detail-item i {
    width: 16px;
    text-align: center;
    color: #999;
}

.detail-item.total-price {
    font-weight: 600;
    color: #333;
    margin-top: 8px;
}

.detail-item.total-price i {
    color: #ff4d4f;
}

.rating-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px dashed #eee;
}

.rating-prompt {
    font-size: 14px;
    color: #666;
}

.stars {
    display: flex;
    gap: 8px;
}

.stars span {
    cursor: pointer;
}

.stars i {
    color: #ddd;
    font-size: 18px;
    transition: color 0.2s;
}

.stars i.rated {
    color: #ffc53d;
}

.stars:hover i {
    color: #ffc53d;
}

.stars i:hover ~ i {
    color: #ddd;
}
</style>