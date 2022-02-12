<template>
  <div>
<!--    <div id="main">ddd</div>-->
    <h1>性能优化</h1>
    <div id="blog" v-html="htmlContent"></div>
<!--    <div>separated</div>-->
<!--    <div>{{mdContent}}</div>-->

  </div>

</template>

<script>
  // document.getElementsByTagName('main').append(data.htmlContent)
  export default {
    name: "Main",
    data(){
      return {
        mdContent : "he",
        htmlContent : ""
      }
    },
    created() {
      this.getContent()
    },
    mounted() {
      const html = "<h1>aaaa</h1>"
      document.getElementById('main')[0].innerHTML = html
    },
    methods : {
      getContent(){
        let _this = this
        this.axios.get("post/content?path='/Users/wangke/WebstormProjects/keblog/keblog-back/src/main/resources/static/posts/八股'")
          .then((response)=>{
            console.log(response.data)
            _this.htmlContent = this.converter.makeHtml(response.data.content)
          })
          .catch((error)=>{
            console.log(error)
          })
      }
    }
  }
</script>

<style scoped>
#blog{
  margin-left: 20%;
  text-align: left;
}
</style>
