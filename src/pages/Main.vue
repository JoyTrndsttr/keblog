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
        htmlContent : this.converter.makeHtml("# 性能优化\n" +
          "\n" +
          "总思路：\n" +
          "\n" +
          "- 降低请求量\n" +
          "- 加快请求速度\n" +
          "- 缓存\n" +
          "- 渲染\n" +
          "\n" +
          "## 网页性能优化\n" +
          "\n" +
          "- 减少http请求次数（合并css js 图片） \n" +
          "  - 合理设置HTTP缓存，变化不大的src走缓存\n" +
          "  - 减少不必要的请求\n" +
          "  - 减少作用链域的查找（保存局部变量）\n" +
          "- 根据域名划分内容\n" +
          "- 减少DNS查询\n" +
          "- 避免页面跳转\n" +
          "- 使用浏览器缓存\n" +
          "  - HTTP协议缓存请求，离线缓存mainifest，离线数据缓存localstorage\n" +
          "- 延迟加载、提前加载、并行加载\n" +
          "- 减少DOM元素数量，或将操作结果保存在一个局部变量中，不使用表达式（减少CADS）\n" +
          "- 减少iframe数量\n" +
          "- 避免404\n" +
          "\n" +
          "## 服务器优化\n" +
          "\n" +
          "- 使用CDN\n" +
          "- 添加Expires或Cache-Control报文头\n" +
          "- Gzip压缩传输文件\n" +
          "- 配置ETags\n" +
          "- 使用GET AJAX请求头\n" +
          "- 避免空的图片src\n" +
          "\n" +
          "### cookie\n" +
          "\n" +
          "- 减少cookie的大小和传输次数\n" +
          "- 页面内容使用无cookie的域名\n" +
          "\n" +
          "### css\n" +
          "\n" +
          "- 样式表放head（先加载css）\n" +
          "- 避免css表达式\n" +
          "- 用<link>代替@import\n" +
          "- 避免使用Filters\n" +
          "\n" +
          "### js\n" +
          "\n" +
          "- 脚本置底\n" +
          "- 使用外部js和css文件\n" +
          "- 精简js和css，去除重复脚本\n" +
          "- 减少DOM访问\n" +
          "- 使用智能事件处理\n" +
          "- 慎用with\n" +
          "- 减少作用域查找\n" +
          "\n" +
          "## 图片\n" +
          "\n" +
          "- 优化图片\n" +
          "- 使用css sprites\n" +
          "- 不要在HTML中缩放图片\n" +
          "- 使用小且可缓存的favicon.ico")
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
        this.axios.get("post/child?path='asd'")
          .then((response)=>{
            console.log(response.data)
            _this.htmlContent = this.converter.makeHtml(response.data)
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
