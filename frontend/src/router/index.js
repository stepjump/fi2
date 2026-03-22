import { createRouter, createWebHistory } from 'vue-router';
import PostList from '../components/PostList.vue';
import PostDetail from '../components/PostDetail.vue';
import PostWrite from '../components/PostWrite.vue'; // 1. 추가

const routes = [
  { path: '/', component: PostList },
  { path: '/posts/:id', component: PostDetail },
  { path: '/write', component: PostWrite }, // 2. 추가
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;