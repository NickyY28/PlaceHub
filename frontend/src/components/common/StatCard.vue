<template>
  <div class="col-lg-3 col-md-6 col-sm-12 mb-4">
    <div class="card border-0 shadow-sm h-100 stat-card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h6 class="text-muted mb-2">
              {{ title }}
            </h6>

            <h2 class="fw-bold mb-0">
              {{ value }}
            </h2>
          </div>

          <div class="icon-box">
            <i :class="icon"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  value: [String, Number],
  icon: String,
});
</script>

<style scoped>
.stat-card {
  border-radius: 16px;
  transition: 0.25s;
}
.stat-card:hover {
  transform: translateY(-4px);
}

.icon-box {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #0d6efd15;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-box i {
  font-size: 26px;
  color: #0d6efd;
}
</style>
