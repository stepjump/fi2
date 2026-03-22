<template>
  <div class="container">
    <h2>새 글 작성</h2>
    <div class="form-group">
      <label>제목</label>
      <input v-model="post.title" placeholder="제목을 입력하세요" />
    </div>

    <div class="form-group">
      <label>비밀번호</label>
      <input v-model="post.password" type="password" placeholder="삭제 시 필요합니다" />
    </div>

    <div class="form-group">
      <label>내용</label>
      <textarea v-model="post.content" rows="10" placeholder="내용을 입력하세요"></textarea>
    </div>

    <div class="actions">
      <button @click="submitPost" class="btn-submit">등록하기</button>
      <button @click="$router.push('/')" class="btn-cancel">취소</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();

// parent_id는 기본적으로 0(서버에서 null처리됨)으로 설정
const post = ref({
  title: '',
  content: '',
  password: '',
  parent_id: null
});

const submitPost = async () => {
  // 간단한 유효성 검사
  if (!post.value.title || !post.value.content || !post.value.password) {
    return alert("모든 항목을 입력해주세요.");
  }

  try {
    const response = await api.post('/posts', post.value);
    alert("글이 성공적으로 등록되었습니다!");
    // 등록 후 목록 페이지로 이동
    router.push('/');
  } catch (err) {
    console.error("작성 실패:", err);
    alert(err.response?.data?.detail || "글 등록 중 오류가 발생했습니다.");
  }
};
</script>

<style scoped>
.container { max-width: 600px; margin: 0 auto; padding: 20px; text-align: left; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
label { font-weight: bold; margin-bottom: 5px; }
input, textarea { padding: 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; }
.actions { display: flex; gap: 10px; margin-top: 20px; }
.btn-submit { background-color: #42b883; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; flex: 1; }
.btn-cancel { background-color: #eee; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; }
.btn-submit:hover { background-color: #3aa876; }
</style>