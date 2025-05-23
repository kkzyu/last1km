<template>
    <div class="create-request-view">
        <div class="view-header">
            <AddRequestButton @add-request-clicked="handleNewRequest" />
            <!-- You could add a title here if needed, e.g., <h1>创建委托</h1> -->
        </div>

        <div class="form-content-wrapper">
            <div v-if="orderStore.requests.length === 0" class="empty-state">
                <p>暂无委托，请点击上方按钮添加。</p>
            </div>
            <div v-else>
                <!-- Loop to render multiple request forms -->
                <div v-for="(request, index) in orderStore.requests"
                     :key="request.id || index" 
                     class="request-item-container">
                    <RequestDetailsForm
                        :request-id="request.id" 
                        :index="index"
                        v-model:origin="request.origin"
                        v-model:destination="request.destination"
                        v-model:description="request.description"
                        v-model:orderInfo="request.orderInfo"
                        v-model:taskAmount="request.amount"
                        @remove-request="handleRemoveRequest(index)"
                        @update:taskAmount="updateTotalAmount"
                    />
                </div>
            </div>
        </div>

        <!-- CheckoutBar is fixed, so its placement in template order is less critical for layout,
             but keeping it at the bottom is conventional. -->
        <CheckoutBar :total-task-amount="totalAmount" />
    </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'; // Added onMounted
import { useOrderStore } from '@/stores/orderStore';
import AddRequestButton from '@/components/Publish/AddRequestButton.vue';
import RequestDetailsForm from '@/components/Publish/RequestDetailsForm.vue';
import CheckoutBar from '@/components/Publish/CheckoutBar.vue';

const orderStore = useOrderStore();

// Ensure at least one form on mount if empty
onMounted(() => {
    if (orderStore.requests.length === 0) {
        orderStore.addRequest();
    }
});

const totalAmount = computed(() => {
    return orderStore.requests.reduce((sum, request) => {
        // Ensure amount is treated as a number, default to 0 if invalid
        const amount = parseFloat(request.amount);
        return sum + (isNaN(amount) ? 0 : amount);
    }, 0);
});

const handleNewRequest = () => {
    orderStore.addRequest();
};

// Optional: Implement remove request if RequestDetailsForm emits it
const handleRemoveRequest = (index) => {
    orderStore.removeRequest(index); // Assuming you add this method to your store
};


// updateTotalAmount is implicitly called when taskAmount changes due to v-model and computed property.
// If you need to do something specific beyond recalculating total, keep it. Otherwise, it might be redundant.
const updateTotalAmount = () => {
    // This function is fine if you need to log or perform other actions on individual amount updates.
    // The `totalAmount` computed property will automatically reflect changes.
    console.log('Individual task amount updated. New total:', totalAmount.value);
};

</script>

<style scoped>
.create-request-view {
    display: flex;
    flex-direction: column;
    background-color: #f4f6f8; /* Light background for the whole view */
    /* max-width: 390px; */
    width:100%;
    height:100%;
    margin: 0 auto; /* Center the view if it's not full width */
    position: relative; /* For CheckoutBar positioning if it weren't fixed to viewport */
}

.view-header {
    padding: 15px;
    background-color: #fff;
    /* border-bottom: 1px solid #e0e0e0; */ /* Optional: if you want a separator */
    /* Make AddRequestButton more prominent or centered if desired */
    display: flex;
    justify-content: flex-end; /* Aligns button to the right */
}

.form-content-wrapper {
    flex-grow: 1; /* Allows this area to take available space */
    overflow-y: auto; /* Enables scrolling for forms */
    padding: 15px 15px 0; /* Add top/horizontal padding */
    /*
      IMPORTANT: Add padding-bottom to prevent content from being hidden
      BEHIND the fixed CheckoutBar.
      CheckoutBar height (60px) + some buffer (10px)
    */
    scrollbar-width:none;
    -ms-overflow-style:none;
    padding-bottom: 75px; /* CHECKOUT_BAR_HEIGHT + BUFFER_FOR_GLOBAL_NAV (if any) + extra space */
}
.form-content-wrapper::-webkit-scrollbar {
  display: none;
}
.request-item-container {
    margin-bottom: 15px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    /* Add padding inside if RequestDetailsForm doesn't have its own */
    /* padding: 15px; */
}
.request-item-container:last-child {
    margin-bottom: 0; /* No margin for the last item before padding-bottom of wrapper */
}

.empty-state {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px; /* Or flex-grow: 1 to fill space */
    color: #777;
    font-size: 16px;
}

/* For better scroll performance on touch devices */
@media (hover: none) {
    .form-content-wrapper {
        -webkit-overflow-scrolling: touch;
    }
}
</style>