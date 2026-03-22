<template>
  <div v-if="post" class="container">
    <div class="post-header">
      <h1>{{ post.title }}</h1>
      <div class="meta">
        조회수: {{ post.view_count }} | 작성일: {{ new Date(post.created_at).toLocaleString() }}
      </div>
    </div>
    <hr />
    <div class="post-content">{{ post.content }}</div>
    
    <div class="post-actions">
      <button @click="$router.push('/')">목록으로</button>
      <button @click="handleDeletePost" class="btn-danger">삭제</button>
    </div>

    <hr />

    <div class="comment-section">
      <h3>댓글 ({{ comments.length }})</h3>
      <ul class="comment-list">
        <li v-for="comment in comments" :key="comment.id">
          <div class="comment-info">
            <strong>{{ comment.author }}</strong>
            <span class="date">{{ new Date(comment.created_at).toLocaleString() }}</span>
            <button @click="deleteComment(comment.id)" class="btn-small-del">삭제</button>
          </div>
          <p>{{ comment.content }}</p>
        </li>
      </ul>

      <div class="comment-form">
        <div class="form-row">
          <input v-model="newComment.author" placeholder="작성자" />
          <input v-model="newComment.password" type="password" placeholder="비밀번호" />
        </div>
        <textarea v-model="newComment.content" placeholder="댓글 내용을 입력하세요"></textarea>
        <button @click="submitComment">댓글 등록</button>
      </div>
    </div>
  </div>
  <div v-else>로딩 중...</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

const route = useRoute();
const router = useRouter();
const post = ref(null);
const comments = ref([]);
const newComment = ref({ author: '', password: '', content: '' });

const loadData = async () => {
  try {
    const id = route.params.id;
    const res = await api.get(`/posts/${id}`);
    post.value = res.data.post;
    comments.value = res.data.comments;
  } catch (err) {
    alert("게시글을 찾을 수 없습니다.");
    router.push('/');
  }
};

const submitComment = async () => {
  if (!newComment.value.content || !newComment.value.password) {
    return alert("내용과 비밀번호를 입력해주세요.");
  }
  try {
    await api.post(`/posts/${post.value.id}/comments`, newComment.value);
    newComment.value = { author: '', password: '', content: '' };
    loadData(); // 댓글 목록 갱신
  } catch (err) {
    alert("댓글 등록 실패");
  }
};

const deleteComment = async (commentId) => {
  const pw = prompt("댓글 삭제 비밀번호를 입력하세요.");
  if (!pw) return;
  try {
    // 우리가 만든 post_id와 comment_id를 모두 사용하는 API 호출
    await api.delete(`/posts/${post.value.id}/comments/${commentId}`, {
      data: { password: pw }
    });
    alert("댓글이 삭제되었습니다.");
    loadData();
  } catch (err) {
    alert(err.response?.data?.detail || "삭제 실패");
  }
};

const handleDeletePost = async () => {
  const pw = prompt("게시글 삭제 비밀번호를 입력하세요.");
  if (!pw) return;
  try {
    await api.delete(`/posts/${post.value.id}`, { data: { password: pw } });
    alert("게시글이 삭제되었습니다.");
    router.push('/');
  } catch (err) {
    alert("삭제 실패: 비밀번호를 확인하세요.");
  }
};

onMounted(loadData);
</script>

<style scoped>
.container { max-width: 800px; margin: 0 auto; padding: 20px; text-align: left; }
.post-content { min-height: 200px; padding: 20px 0; white-space: pre-wrap; line-height: 1.6; }
.meta { color: #888; font-size: 0.9em; }
.comment-section { margin-top: 40px; }
.comment-list { list-style: none; padding: 0; }
.comment-list li { border-bottom: 1px solid #eee; padding: 15px 0; }
.comment-info { display: flex; gap: 10px; align-items: center; margin-bottom: 5px; }
.date { font-size: 0.8em; color: #999; }
.comment-form { display: flex; flex-direction: column; gap: 10px; margin-top: 20px; background: #f9f9f9; padding: 15px; }
.form-row { display: flex; gap: 10px; }
.btn-small-del { color: #ff4d4f; border: none; background: none; cursor: pointer; font-size: 0.8em; }
.btn-danger { background-color: #ff4d4f; color: white; border: none; padding: 5px 10px; margin-left: 10px; cursor: pointer; }
</style>