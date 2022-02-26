<template>
  <div>
<!--    <div id="main">ddd</div>-->
    <h1>{{ Title }}</h1>
    <div id="echarts" v-show="show.charts"></div>
    <div id="blog" v-html="htmlContent" v-show="show.content">{{htmlContent}}}</div>
    <div v-for="post in content" v-on:click="getContent(post)" v-show="show.list">{{post.name}}</div>
<!--    <div>separated</div>-->
<!--    <div>{{mdContent}}</div>-->

  </div>

</template>

<script>
  import  * as echarts from 'echarts'
  // document.getElementsByTagName('main').append(data.htmlContent)
  export default {
    name: "Main",
    data(){
      return {
        mdContent : "he",
        htmlContent : "",
        content : {},
        Title : "博客",
        charts : [],
        show : {
          "charts" : false,
          "content": false,
          "list"   : false
        }
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
            _this.show = {charts:false,content:false,list:true}
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
    computed: {
      listenContent(){
        return this.$store.state.content
      }
    },
    watch   : {
      listenContent:function (content){
         if(content===0){
           // this.getContent()
         }
         else if(content===1){
           this.showCharts()
         }
      }
    },
    methods : {
      getContent({path:path,name:name}){
        let _this = this
        this.axios.get("post/content?path="+path)
          .then((response)=>{
            if(response.data.status===0){
              //说明是文章
              console.log(response.data)
              _this.htmlContent = this.converter.makeHtml(response.data.content)
              _this.show = {charts:false,content:true,list:false}
            }
            else{
              //说明是文件夹
              console.log(response.data)
              _this.content = response.data.content
              _this.show = {charts:false,content:false,list:true}
            }
            _this.$store.commit("postSelected",name)
            console.log(_this.$store.state.navigation)
          })
          .catch((error)=>{
            console.log(error)
          })
      },
      async showCharts(){
        console.log("showCharts")
        var _this = this
        //获取数据
        await this.axios.get("post/charts")
          .then(response=>{
            console.log(response.data.content)
            _this.charts = response.data.content
          })
        var chart = echarts.init(document.getElementById('echarts'),null,{width:600,height:400})
        window.onresize = function (){chart.resize()}//监听图标容器的大小并改变图标大小
        //随便取一份数据
        var option = {
          legend: {},
          tooltip: {},
          dataset: {
            // 用 dimensions 指定了维度的顺序。直角坐标系中，如果 X 轴 type 为 category，
            // 默认把第一个维度映射到 X 轴上，后面维度映射到 Y 轴上。
            // 如果不指定 dimensions，也可以通过指定 series.encode
            // 完成映射，参见后文。
            dimensions: ['name', 'size'],
            source: _this.charts
          },
          xAxis: { type: 'category' },
          yAxis: {},
          series: [{ type: 'bar' }]
        };
        chart.setOption(option)
        _this.Title = "数据统计"
        _this.show = {charts:true,content:false,list:false}
      }
    }
  }
</script>

<style scoped>
#blog{
  margin-left: 20%;
  text-align: left;
}

#echarts{
  width: 600px;
  height: 400px;
  //border: 2px solid red;
  display: flex;
  justify-content: center;
  margin:auto;
}

#echarts::after{
  left:40px;
}

</style>
