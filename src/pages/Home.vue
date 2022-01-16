<template>
  <el-container>
    <el-header><Head></Head></el-header>
    <el-container>
      <el-main><Main></Main></el-main>
      <el-aside width="20%"><category></category></el-aside>
    </el-container>
  </el-container>
</template>

<script>
import Head from '../components/Head'
import Category from "./Category";
import Main from "./Main";
export default {
  name: "Home",
  components : {
    Head,
    Category,
    Main
  }
}
</script>

<style scoped>
.el-aside{
  //height: 60%;
  margin-top  : 20px;
  margin-right: 10%;
}
</style>
