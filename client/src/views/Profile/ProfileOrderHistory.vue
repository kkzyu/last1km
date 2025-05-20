<template>
    <div class="page-container">
        <span class="icon"><i class="fas fa-angle-left" @click="$router.push('/profile')"></i></span>
        <h2 class="title">历史订单</h2>
    </div>
    <div v-for="order in orders" :key="order.id" class="orders">
        <div v-if="order.status === '已完成'" class="order-box">
            <div class="header">
                <span>订单{{ order.id }}</span>
                <span class="status">{{ order.status }}</span>
            </div>
            <div class="detail">
                <div>下单时间：{{ order.date }}</div>
                <div>总价：<i class="fa fa-cny"></i> 4.1</div>
            </div>

            <div class="stars"><span class="icon" v-for="n in 5" :key="n"><i class="fa fa-star"></i></span></div>
        </div>

    </div>

</template>

<script setup>
import information from '@/assets/data/information.json'

const orders = information.orders
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

.orders {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.order-box {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px;
    width: 85%;
    /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */
}

.header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;
}

.status {
    color: grey;
}

.detail div {
  margin: 8px 0;
  color: grey;
}

.stars {
  display: flex;
  color: #ffff00;
  font-size: 24px;
  gap: 10px;
  justify-content: end;
  margin-top: 0;
}
</style>