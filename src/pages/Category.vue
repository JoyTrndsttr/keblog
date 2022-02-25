<template>
  <div class="card">
    <h3 id="head3">分类</h3>
    <div v-on:click="getStatisticCharts">统计</div>
    <div v-for="category in Category"><a href="">{{category}}</a></div>
  </div>
</template>

<script>
export default {
  name: "Category",
  data() {
    return {
      Category : ["计算机网络","前端","Mac技巧",'学习经验']
    }
  },
  methods:{
    getStatisticCharts(){
      this.$store.commit("getCharts")
    }
  }
}
</script>

<style scoped>
.card{
  border-style: groove;
  border-width: 2px;
  border-radius: 30px;
}
#head3{
  padding: 10px;
  border-bottom: groove 2px;
  margin : 2px 15px 2px 15px;
}
</style>
