<template>
  <div class="container">
    <h2>게시판 목록</h2>
    <div class="actions">
      <button @click="fetchPosts" class="btn-refresh">새로고침</button>
      <button @click="$router.push('/write')" class="btn-write">글쓰기</button>
    </div>

    <table class="post-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>제목</th>
          <th>조회수</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="post in posts" :key="post.id">
          <td>{{ post.id }}</td>
          <td class="title-cell" @click="$router.push(`/posts/${post.id}`)">
            {{ post.title }}
          </td>
          <td>{{ post.view_count }}</td>
          <td>{{ formatDate(post.created_at) }}</td>
        </tr>
        <tr v-if="posts.length === 0">
          <td colspan="4">게시글이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const posts = ref([]);

const fetchPosts = async () => {
  try {
    const response = await api.get('/posts');
    // 백엔드에서 리스트를 반환하는 구조에 맞게 설정 (예: response.data)
    posts.value = response.data;
  } catch (err) {
    console.error("목록 로드 실패:", err);
    alert("게시글을 불러올 수 없습니다.");
  }
};

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString();
};

onMounted(fetchPosts);
</script>

<style scoped>
.container { max-width: 900px; margin: 0 auto; padding: 20px; }
.actions { margin-bottom: 15px; display: flex; gap: 10px; }
.post-table { width: 100%; border-collapse: collapse; }
.post-table th, .post-table td { border: 1px solid #ddd; padding: 12px; text-align: center; }
.title-cell { text-align: left; cursor: pointer; color: #42b883; font-weight: bold; }
.title-cell:hover { text-decoration: underline; }
.btn-write { background-color: #42b883; color: white; border: none; padding: 8px 16px; cursor: pointer; }
</style>