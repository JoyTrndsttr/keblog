<template>
  <el-container>
    <el-header><Head></Head></el-header>
    <div style="border:1px solid blue" @click="increment()">{{ count }}</div>
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
  },
  computed : {
    count () {
      return this.$store.state.count
    }
  },
  methods: {
    increment() {
      this.$store.commit('increment')
      console.log(this.$store.state.count)
    }
  }
}
</script>

<style scoped>
.el-header{
  position:sticky;
  top:0;
  background-color: beige;
}
.el-aside{
  //height: 60%;
  margin-top  : 20px;
  margin-right: 10%;
}
</style>
