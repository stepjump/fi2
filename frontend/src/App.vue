<template>
  <div id="app">
    <nav>
      <router-link to="/">홈(게시판)</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
#app { font-family: Avenir, Helvetica, Arial, sans-serif; padding: 20px; }
nav { margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
nav a { text-decoration: none; color: #42b883; font-weight: bold; }
</style>