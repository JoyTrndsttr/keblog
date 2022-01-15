<template>
  <div>
    <div class="box">
      <strong id="head-name">王柯的个人博客网站</strong>
       >
      <span id="head-home"><a href="/">首页</a></span>
       >
      <span id="head-blog"><a href="/">博客</a></span>

      <div id="search-field">搜索：<input></input></div>
    </div>
    <div class="line">content</div>
  </div>
</template>

<script>
export default {
name: "Head"
}
</script>

<style scoped>
  #head-name{
  }
  #search-field{
    position: absolute;
    right:20%;
  }

  .box{
    display: flex;
    margin-left: 5%;
    font-size: 1.2em;
  }

  .line{
    margin: 20px 20px 20px 20px;
    line-height: 1.2px;
    border-left: 40em solid #2c3e50;
    border-right: 40em solid #2c3e50;
    text-align: center;
  }
</style>
