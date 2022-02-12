### 一些定义

- **包含块**

  - 一个元素的box的定位和尺寸，会与某一矩形框有关，这个框就称之为包含块。
  - 元素会为它的子孙元素创建包含块，但是，并不是说元素的包含块就是它的父元素，元素的包含块与它的祖先元素的样式等有关系
  - 譬如：
    -  根元素是最顶端的元素，它没有父节点，它的包含块就是初始包含块
    - static和relative的包含块由它最近的块级、单元格或者行内块祖先元素的内容框（content）创建
    - fixed的包含块是当前可视窗口
    - absolute的包含块由它最近的position 属性为absolute、relative或者fixed的祖先元素创建
    - 如果其祖先元素是行内元素，则包含块取决于其祖先元素的direction特性
    - 如果祖先元素不是行内元素，那么包含块的区域应该是祖先元素的内边距边界

- **控制框**

  - 总结：

    - 如果一个框里，有一个块级元素，那么这个框里的内容都会被当作块框来进行格式化，因为只要出现了块级元素，就会将里面的内容分块几块，每一块独占一行（出现行内可以用匿名块框解决）
    - 如果一个框里，没有任何块级元素，那么这个框里的内容会被当成行内框来格式化，因为里面的内容是按照顺序成行的排列

  - 块框：

    - 块级元素会生成一个块框（Block Box），块框会占据一整行，用来包含子box和生成的内容

    - 块框同时也是一个块包含框（Containing Box），里面要么只包含块框，要么只包含行内框（不能混杂），如果块框内部有块级元素也有行内元素，那么行内元素会被匿名块框包围

    - 关于**匿名块框**的生成，示例：

      ```html
      <DIV>
      Some text
      <P>More text
      </DIV>
      ```

      - div生成了一个块框，包含了另一个块框p以及文本内容Some text，此时Some text文本会被强制加到一个匿名的块框里面，被div生成的块框包含（其实这个就是IFC中提到的行框，包含这些行内框的这一行匿名块形成的框，行框和行内框不同）
      - 换句话说:**如果一个块框在其中包含另外一个块框，那么我们强迫它只能包含块框，因此其它文本内容生成出来的都是匿名块框（而不是匿名行内框）**

  - 行内框：

    -  一个行内元素生成一个行内框

    - 行内元素能排在一行，允许左右有其它元素
      关于**匿名行内框**的生成，示例：

      ```html
      <P>Some <EM>emphasized</EM> text</P>
      ```

      - P元素生成一个块框，其中有几个行内框（如EM），以及文本Some ， text，此时会专门为这些文本生成匿名行内框

  - display属性的影响：

    - display的几个属性也可以影响不同框的生成：
      - block，元素生成一个块框
      - inline，元素产生一个或多个的行内框
      -  inline-block，元素产生一个行内级块框，行内块框的内部会被当作块块来格式化，而此元素本身会被当作行内级框来格式化（这也是为什么会产生BFC）
      -  none，不生成框，不再格式化结构中，当然了，另一个visibility: hidden则会产生一个不可见的框



### 三列布局

[CSS实现三列布局](https://blog.csdn.net/diaoweisang7683/article/details/101968366?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164212583316780269895365%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164212583316780269895365&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-101968366.pc_search_result_control_group&utm_term=css%E4%B8%89%E5%88%97%E5%B8%83%E5%B1%80&spm=1018.2226.3001.4187)

三列布局指的是两边两列定宽，中间的宽度自适应。

常用三种方法：

- 定位
  - 左右两栏选择绝对定位，固定于页面的两侧，中间的主体选择用[margin](https://so.csdn.net/so/search?q=margin&spm=1001.2101.3001.7020)确定位置
- 浮动
  - 让左右两边部分浮动，脱离文档流后对中间部分使用margin来自适应
- 弹性盒布局
  - 使用容器包裹三栏，并将容器的display设置为flex，左右两部分宽度设置为固定，中间flex设置为1，左右两边的值固定，所以中间的自适应

### CSS3

![IMG_3C7B1D1AE7FB-1](/Users/wangke/Desktop/收集/图片/IMG_3C7B1D1AE7FB-1.jpeg)

### flex布局

[CSS（三）flex布局（flex弹性布局详解）](https://blog.csdn.net/u014744118/article/details/99199806?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239174216780271966002%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239174216780271966002&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-99199806.pc_search_result_cache&utm_term=css+flex%E5%B8%83%E5%B1%80&spm=1018.2226.3001.4187)

- css3中新增的布局，得到了所有浏览器的支持，可以简便、完整、响应式地实现各种页面布局

- freecodecamp笔记

  ```
  设置display:flex
  float、clear、vertical-align不适用于flex
  flex-direction:row/column/row-reverse/column-reverse
  flex-wrap:nowrap/wrap/wrap-reverse
  flex:0 1 auto对应：
      flex-grow:2
      flex-shrink:1;//是值为2的两倍
      flex-basis:10em;//初始尺寸
  order:2 //改变顺序
  align-self:center/flex-end/... 单独改变
  ```

  ![img](C:\Users\Administrator\Desktop\来自mac\收集\收集\图片\0E95C42258FABCE19B4B8B5977BCB3BE.png)

- flex:0 1 auto

  - 这是默认情况，代表flex-grow flex-shrink felx-basis

  - flex-shrink

    - 该属性来设置，当父元素的宽度小于所有子元素的宽度的和时（即子元素会超出父元素），子元素如何缩小自己的宽度的。
    - `flex-shrink`的默认值为1，当父元素的宽度小于所有子元素的宽度的和时，子元素的宽度会减小。值越大，减小的越厉害。如果值为0，表示不减小。

    ```html
    <style>
      #box-container {
        display: flex;
        height: 500px;
      }
      #box-1 {
        background-color: dodgerblue;
        width: 100%;
        height: 200px;
        flex-shrink:1;
      }
    
      #box-2 {
        background-color: orangered;
        width: 100%;
        height: 200px;
        flex-shrink:2;
      }
    </style>
    
    <div id="box-container">
      <div id="box-1"></div>
      <div id="box-2"></div>
    </div>
    ```

    - 效果：

    ![image-20220117122014534](C:\Users\Administrator\Desktop\来自mac\收集\收集\图片\image-20220117122014534.png)

  - flex-grow
    - 该属性来设置，当父元素的宽度大于所有子元素的宽度的和时（即父元素会有剩余空间），子元素如何分配父元素的剩余空间。
    - `flex-grow`的默认值为0，意思是该元素不索取父元素的剩余空间，如果值大于0，表示索取。值越大，索取的越厉害。
  - flex-basis
    - 该属性来设置该元素的宽度。当然，`width`也可以用来设置元素宽度。如果元素上同时设置了`width`和`flex-basis`,那么`flex-basis`会覆盖`width`的值。

- flex实现九宫格布局

  - 链接：[css的flex布局实现响应式九宫格](https://blog.csdn.net/wakaka_cy/article/details/82782371?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239343416780357278654%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239343416780357278654&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-82782371.pc_search_result_cache&utm_term=css+flex%E4%B9%9D%E5%AE%AB%E6%A0%BC&spm=1018.2226.3001.4187)
  - 使用CSS中的calc（）：calc()可以计算不同单位的值，也可以嵌套，不过符号之间一定要有空格，虽然"*"、"/"之间可以没有，建议还是加上空格。例如：width:calc(100% - 30px)；
  - 要点：在一个div中设定9个div，定义class为block，把这个类设置宽度为容器宽度的三分之一少一点（留点margin），然后设置margin，height，border等
  - 代码：

  ```html
  <!-- css flex布局实现响应式九宫格以及calc()计算表达式的值 -->
  <!DOCTYPE html>
  <html>
  <style>
  .blockDiv{
      width: 100%;
      display:flex;
      flex-wrap: wrap;
  }
  .block{
      width: calc(calc(100% / 3) - 10px);
      margin:5px;
      height:50px;
      box-sizing: border-box;
      border:1px  solid #000;
  }
  </style>
  <body>
     <div class="blockDiv">
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
          <div class="block"></div>
      </div>
  </body>
  </html>
  ```