<template>
  <div>
<!--    <div id="main">ddd</div>-->
    <h1>{{ Title }}</h1>
    <div id="blog" v-html="htmlContent">{{htmlContent}}}</div>
    <div v-for="post in content" v-on:click="getContent(post.path)">{{post.name}}</div>
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
        htmlContent : "",
        content : {},
        Title : "博客"
      }
    },
    created() {
      // this.getContent()
      let _this = this
      _this.$nextTick(()=>{
        _this.axios.get("post/init")
          .then((response)=>{
            console.log(response.data)
            _this.content = response.data.content
          })
          .catch((error)=>{
            console.log(error)
          })
      })
    },
    mounted() {
      // const html = "<h1>aaaa</h1>"
      // document.getElementById('main')[0].innerHTML = html
    },
    methods : {
      getContent(path){
        let _this = this
        this.axios.get("post/content?path="+path)
          .then((response)=>{
            if(response.data.status===0){
              console.log(response.data)
              _this.htmlContent = this.converter.makeHtml(response.data.content)
            }
            else{
              console.log(response.data)
              _this.content = response.data.content
            }
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
