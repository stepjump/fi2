import { createRouter, createWebHistory } from 'vue-router';
import PostList from '../components/PostList.vue';
import PostDetail from '../components/PostDetail.vue';

const routes = [
  { path: '/', component: PostList },
  { path: '/posts/:id', component: PostDetail },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;