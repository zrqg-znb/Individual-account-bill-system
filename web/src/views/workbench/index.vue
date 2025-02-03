<template>
  <AppPage :show-footer="false">
    <div flex-1 class="workbench-container">
      <n-carousel
        autoplay
        interval="2000"
        style="height: 400px; border-radius: 8px; overflow: hidden;"
        :show-arrow="true"
        effect="fade"
      >
        <img
          class="carousel-img"
          src="/screens/1.png"
        />
        <img
          class="carousel-img"
          src="/screens/2.png"
        />
        <img
          class="carousel-img"
          src="/screens/3.png"
        />
        <img
          class="carousel-img"
          src="/screens/4.png"
        />
        <img
          class="carousel-img"
          src="/screens/5.png"
        />
      </n-carousel>
      <n-card title="系统概述" class="overview-card" style="margin-top: 24px">
        <p class="overview-text">
          个人账单管理系统是一个现代化的财务管理解决方案，采用FastAPI和Vue.js构建的全栈应用程序。本系统旨在帮助用户高效管理个人账单、跟踪消费记录，并提供直观的数据分析功能。
        </p>
      </n-card>
      <n-card title="核心功能" class="feature-card" style="margin-top: 24px">
        <n-list class="feature-list">
          <n-list-item>
            <n-tag type="success" round size="large">
              账单管理
            </n-tag>
            <p class="feature-desc">
              支持账单的创建、查看、更新和删除，可添加多个商品项目，支持批量操作
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag type="info" round size="large">
              商品结算
            </n-tag>
            <p class="feature-desc">
              灵活的商品结算功能，支持单品和批量结算，包含退货和退款处理
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag type="warning" round size="large">
              数据导出
            </n-tag>
            <p class="feature-desc">
              支持账单数据导出，方便用户进行账务统计和分析
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag type="error" round size="large">
              用户管理
            </n-tag>
            <p class="feature-desc">
              完善的用户权限管理，支持部门组织架构，确保数据安全
            </p>
          </n-list-item>
        </n-list>
      </n-card>
      <n-card title="技术特点" class="tech-card" style="margin-top: 24px; margin-bottom: 24px">
        <n-list class="tech-list">
          <n-list-item>
            <n-tag round size="large">
              后端架构
            </n-tag>
            <p class="tech-desc">
              采用FastAPI框架，提供高性能的异步API服务，使用Tortoise ORM进行数据管理
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag round size="large">
              前端技术
            </n-tag>
            <p class="tech-desc">
              基于Vue.js和Naive UI构建，提供现代化的用户界面和流畅的交互体验
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag round size="large">
              系统安全
            </n-tag>
            <p class="tech-desc">
              实现了完整的权限控制和审计日志，保障系统运行安全
            </p>
          </n-list-item>
          <n-list-item>
            <n-tag round size="large">
              扩展性
            </n-tag>
            <p class="tech-desc">
              模块化设计，支持功能扩展，便于后续系统升级和维护
            </p>
          </n-list-item>
        </n-list>
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { useUserStore } from "@/store";
import { NCarousel, NCard, NList, NListItem, NTag, NIcon } from "naive-ui";

const userStore = useUserStore();
</script>

<style scoped>
.workbench-container {
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.carousel-img {
  height: 100%;
  border-radius: 10px;
  margin: auto;
}

.overview-card :deep(.n-card-header) {
  font-size: 20px;
  font-weight: 500;
}

.overview-text {
  font-size: 16px;
  line-height: 1.6;
  color: #666;
}

.feature-card,
.tech-card {
  transition: all 0.3s ease;
}

.feature-card:hover,
.tech-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feature-list :deep(.n-list-item),
.tech-list :deep(.n-list-item) {
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  background: rgba(250, 250, 250, 0.8);
}

.feature-desc,
.tech-desc {
  margin: 12px 0 0 10px;
  font-size: 15px;
  color: #666;
  line-height: 1.5;
}

:deep(.n-tag) {
  padding: 6px 12px;
  font-size: 14px;
}

:deep(.n-tag .n-icon) {
  margin-right: 6px;
}
</style>
