<template>
    <div class="personal-portrait">
        <div class="about">
            <img class="img" src="/images/ProfilePortrait.jpg" />
        </div>
        <div class="about">
            kkzyu <span class="icon"><i class="fas fa-venus"></i></span><br/>
            193****1935
        </div>
    </div>
</template>

<style scoped>
.personal-portrait {
    display: flex;
    justify-content: flex-start;
    margin-left:20px;
}

.img {
    object-fit: cover;
    border-radius: 50%;
    width: min(20vw, 60px);
    height: min(20vw, 60px);
}

.about {
    padding: 0 5px;
}

.icon {
    color:deeppink;
}
</style>