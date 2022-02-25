<template>
  <div>
<!--    <div id="main">ddd</div>-->
    <h1>{{ Title }}</h1>
    <div id="echarts" style="width: 600px;height: 400px"></div>
    <div id="blog" v-html="htmlContent">{{htmlContent}}}</div>
    <div v-for="post in content" v-on:click="getContent(post)">{{post.name}}</div>
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
              console.log(response.data)
              _this.htmlContent = this.converter.makeHtml(response.data.content)
            }
            else{
              console.log(response.data)
              _this.content = response.data.content
            }
            _this.$store.commit("postSelected",name)
            console.log(_this.$store.state.navigation)
          })
          .catch((error)=>{
            console.log(error)
          })
      },
      showCharts(){
        console.log("showCharts")
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
            dimensions: ['product', '2015', '2016', '2017'],
            source: [
              { product: 'Matcha Latte', '2015': 43.3, '2016': 85.8, '2017': 93.7 },
              { product: 'Milk Tea', '2015': 83.1, '2016': 73.4, '2017': 55.1 },
              { product: 'Cheese Cocoa', '2015': 86.4, '2016': 65.2, '2017': 82.5 },
              { product: 'Walnut Brownie', '2015': 72.4, '2016': 53.9, '2017': 39.1 }
            ]
          },
          xAxis: { type: 'category' },
          yAxis: {},
          series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
        };
        chart.setOption(option)
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
