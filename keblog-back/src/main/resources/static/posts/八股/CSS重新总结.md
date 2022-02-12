# 选择器的权重和优先级

[CSS基础：谈谈选择器的权重和优先级](https://yuguang.blog.csdn.net/article/details/113888600)

- 浏览器通过优先级来判断哪些属性值与一个元素最为相关，从而在该元素上应用这些属性值。

- 优先级是由匹配的选择器中每一种选择器类型的 数值 决定的。

- 当同一个元素有多个声明的时候，优先级才会有意义。因为每一个直接作用于元素的 CSS 规则总是会接管/覆盖（take over）该元素从祖先元素继承而来的规则。

- 当优先级与多个 CSS 声明中任意一个声明的优先级相等的时候，CSS 中最后的那个声明将会被应用到元素上。

- 优先级

  ![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/优先级.png)

  - 每一组选择器在判断优先级的时，是相加的关系
  - `!important` 规则时，此声明将覆盖任何其他声明
  - !important 是一个坏习惯，应该尽量避免
  - 两条相互冲突的带有 !important 规则的声明被应用到相同的元素上时，拥有更大优先级的声明将会被采用。

# 盒模型

[CSS基础：简述CSS盒模型](https://yuguang.blog.csdn.net/article/details/113932715)

<img src="https://img-blog.csdn.net/2018082008592117?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2piajY1Njg4Mzl6/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70" alt="img" style="zoom: 50%;" />

- 内边距 padding：包围在内容区域外部的空白区域
  - 内边距位于边框和内容区域之间，不能为负
  - 可以设置`padding padding-top padding-right padding-bottom padding-left`
  - 更改类.container的内边距,可以在容器和方框之间留出空间
- 外边距 margin:盒子和其他元素之间的空白区域
  - 外边距是盒子周围一圈看不到的空间。它会把其他元素从盒子旁边推开。 外边距属性值可以为正也可以为负。设置负值会导致和其他内容重叠。无论使用标准模型还是替代模型，外边距总是在计算可见部分后**额外添加**。
  - 可以设置`margin: 10px //等于 margin-top: 10px margin-right: 10px margin-bottom: 10px margin-left: 10px`
  - 外边距折叠：如果有两个外边距相接的元素，这些外边距将合并为一个外边距，即最大的单个外边距的大小。
- 边框 border：边框盒包裹内容和内边距
  - 它是在边距和填充框之间绘制的。
    - 如果您正在使用标准的盒模型，边框的大小将添加到框的宽度和高度。
    - 如果您使用的是替代盒模型，那么边框的大小会使内容框更小，因为它会占用一些可用的宽度和高度。
  - 可以设置：`border-top border-right border-bottom border-left border-width border-style border-color`
  - 还可以设置：`border-top-width border-top-style border-top-color`等

## 标准盒模型和替代模型（IE）

- 在标准模型中，如果你给盒设置 `width` 和 `height`，实际设置的是 `content box`。 padding 和 border 再加上设置的宽高一起决定整个盒子的大小，如果使用标准模型，则宽度 = 410px (300 + 50 + 50 + 5 + 5)，由**margin之外**的其他属性组成。

  <img src="/Users/wangke/Desktop/收集/图片/标准盒模型.png" alt="在这里插入图片描述" style="zoom:50%;" />

- 在替代模型中，内容宽度 = 该宽度 - border - padding。

<img src="https://img-blog.csdnimg.cn/2021022214422319.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2piajY1Njg4Mzl6,size_16,color_FFFFFF,t_70" alt="在这里插入图片描述" style="zoom:50%;" />

- 默认浏览器会使用标准模型。如果需要使用替代模型，可以通过为其设置 box-sizing: border-box 来实现。
- 如果你希望所有元素都使用替代模式，而且确实很常用，设置 box-sizing 在 元素上，然后设置所有元素继承该属性

```css
html {
  box-sizing: border-box;
}
*, *::before, *::after {
  box-sizing: inherit;
}
```

## 块级盒子与内联盒子

**块级盒子：**

特点：

- 盒子会在内联的方向上扩展并占据父容器在该方向上的所有可用空间，在绝大数情况下意味着盒子会和父容器一样宽
- 每个盒子都会换行
- width 和 height 属性可以发挥作用
- 内边距（padding）, 外边距（margin） 和 边框（border） 会将其他元素从当前盒子周围“推开”

常见的块级元素：

`div, h1~h6, p, form, ul, li, ol, dl, address, hr, menu, table, fieldset`

**内联盒子：**

特点：

- 盒子不会产生换行。
- width 和 height 属性将不起作用。
- 垂直方向的内边距、外边距以及边框会被应用但是不会把其他处于 inline 状态的盒子推开。
- 水平方向的内边距、外边距以及边框会被应用且会把其他处于 inline 状态的盒子推开。

常见行内元素：

`a, span, label, strong, em, br, img, input, select, textarea, cite`

# Position

[CSS基础：浅谈position](https://yuguang.blog.csdn.net/article/details/113976499)

## 文档流

- "文档流"是在对布局进行任何更改之前，在页面上显示"块"和"内联"元素的方式。通常是从上至下，从左到右的形式
- 一旦某部分脱离了"流"，它就会独立地工作

## 定位

定位的整个想法是允许我们覆盖上面描述的基本文档流行为

- **静态定位**：`position: static;`

- **相对定位**：`position: relative`

```css
.positioned {
    position: relative;
    top: 30px;
    left: 40px;
    background: #E6F7FF;
}
```

```html
<div class="box">
    <h2 class="positioned">二级标题</h2>
    <h3>副标题</h3>
    <p>我是段落1</p>
    <p>我是段落2，我包含了有意思的标签<span>我是span标签</span>,除了span标签还有它——<a href="https://www.baidu.com">我是a标签</a>,你看他们都不会导致新起一行
    </p>
</div>
```

<img src="/Users/wangke/Desktop/收集/图片/相对定位.png" alt="在这里插入图片描述" style="zoom:50%;" />

使用position: relative，不会让元素脱离文档流，目标元素会基于自己原本的位置进行定位

- **绝对定位**：`position: absolute;`

绝对定位将元素从文档流中拖出来，然后使用left、right、top、bottom属性相对于其最接近的一个具有定位属性的父包含块进行绝对定位。如果不存在这样的包含块，则相对于body元素，即相对于浏览器窗口。

- **固定定位**：`position: fixed;`

绝对定位固定元素是相对于元素或其最近的定位祖先，而固定定位固定元素则是相对于浏览器视口本身。 这意味着您可以创建固定的有用的UI项目，如持久导航菜单。

- **粘性定位**：`position: sticky;`

sticky允许被定位的元素表现得像相对定位一样，直到它滚动到某个阈值点（例如，从视口顶部起10像素）为止，此后它就变得固定了。

## z-index

一旦使用定位，就可能使元素重叠,使用`z-index: 3;`控制覆盖，值越大越在上面

# BFC

[CSS基础：CSS的上下文之BFC](https://yuguang.blog.csdn.net/article/details/114021930)

- 定义：BFC全称”Block Formatting Context”, 中文为“块级格式化上下文”。是Web页面的可视CSS渲染的一部分，是块盒子的布局过程发生的区域，也是浮动元素与其他元素交互的区域。
- 下列方式会创建块格式化上下文
  - 根元素（`<html>`）
  - 浮动元素（元素的 `float` 不是 none）
  - 绝对定位元素（元素的 position 为 absolute 或 fixed）
  - display 为 inline-block、table-cells、flex
  - overflow 计算值不为 visible 的块元素
- 块格式化上下文包含创建它的元素内部的所有内容。
- BFC属于普通的文档流，具有 BFC 特性的元素可以看作是隔离了的独立容器，容器里面的元素不会在布局上影响到外面的元素，它有一套渲染规则，它决定了其子元素将如何定位，以及和其他元素的关系和相互作用。

## 外边距折叠

- 同一个BFC下，外边距会发生折叠
- 同一个BFC中，相邻的兄弟元素之间的相对的margin-bottom和margin-top会进行合并，并且显示的是较大值。
- 想要解决这样的问题，我们可以通过将两个child放置于不同的BFC中

## margin塌陷

现象：

- box元素存在外边距100px，相对于body的效果生效了，毫无疑问；

- child元素存在外边距50px，相对于box的效果仅左侧生效了，存在疑问；

解释：

- 有了2.1小节的经验，大家会猜测是不是margin再次发生了合并？也可以，但更合理的形容叫 “margin塌陷”。
- 父子相邻嵌套的元素在垂直方向的margin会发生塌陷，并取最大值。
- 拿例子中的box元素举例，box作为顶，子元素向外称起50px却失效了，可以理解为顶塌陷了。

## BFC 可以包含浮动的元素（清除浮动）

- **现象：**
  - child因为浮动，脱离了文档流；
  - box盒子的高度只计算了border；
- **解释：**
  - 因为子元素已经脱离了文档流，所以父元素在计算高度时忽略了它；
- **解决：**
  - 触发容器的 BFC，使得容器包裹着浮动元素。

## BFC 解决文字环绕的问题

浮动的目的。最初时，浮动只能用于图像（某些浏览器还支持表的浮动），目的就是为了允许其他内容（如文本）“围绕”该图像。而后来的CSS允许浮动任何元素。

**现象：**

- 给左侧子元素设置了左浮动，使得文字环绕在它周围，但为什么文字会被环绕，而不是被遮挡？

**解释：**

看到float会脱离文档流，这是相对于盒子模型来说的。但它没有脱离文本流。

- 文档流是相对于盒子模型讲的

- 文本流是相对于文子段落讲的

元素浮动之后，会让它脱离文档流，也就是说当它后面还有元素时，其他元素会无视它所占据了的区域，直接在它身下布局。但是文字却会认同浮动元素所占据的区域，围绕它布局，也就是没有脱离文本流。

在MDN上提到，该元素从网页的正常流动(文档流)中移除，尽管仍然保持部分的流动性（与绝对定位相反）。

**解决**:

将包裹文字的元素置为BFC

# 层叠上下文

[CSS基础：CSS的上下文之层叠上下文](https://yuguang.blog.csdn.net/article/details/114145737)

定义：

- 层叠上下文，英文称作”stacking context”. 我们假定用户正面向（浏览器）视窗或网页，而 HTML 元素沿着其相对于用户的一条虚构的 z 轴排开，层叠上下文就是对这些 HTML 元素的一个三维构想。众 HTML 元素基于其元素属性按照优先级顺序占据这个空间。

- 我们可以把层叠上下文同样可以理解成是元素的属性。

下列方式会形成层叠上下文：

- position 值为 static 以外的值，且 z-index 值不为 auto;
- flex (flexbox) 容器的子元素，且 z-index 值不为 auto;
- grid (grid) 容器的子元素，且 z-index 值不为 auto;
- opacity 属性值小于 1 的元素;
- transform属性 不为none的元素;

总结：

- 在层叠上下文中，子元素同样也按照上面解释的规则进行层叠。 重要的是，其子级层叠上下文的 z-index 值只在父级中才有意义。
- 子级层叠上下文被自动视为父级层叠上下文的一个独立单元。

## 层叠水平

“层叠水平”，英文称作”stacking level”，决定了同一个层叠上下文中元素在z轴上的显示顺序。网页中的每个元素都是独立的个体，他们一定是会有一个类似的排名排序的情况存在。而这个排名排序、论资排辈就是我们这里所说的“层叠水平”。

但注意，每一个层叠上下文内部的子元素都不会突破包裹它的上下文。

**普通元素的层叠水平优先由层叠上下文决定，因此，层叠水平的比较只有在当前层叠上下文元素中才有意义。**

- 举例：

  ![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/层叠水平.png)

- 现象：
  - 在这个例子中，每个被定位的元素都创建了独自的层叠上下文，因为他们被指定了定位属性和 z-index 值。我们把层叠上下文的层级列在下面：
  - DIV #1
    DIV #2
    DIV #3
    	DIV #4
    	DIV #5
  - 不同层的z-index他们的意义只相对于同一个层叠上下文。你会发现z-index：100的也没有覆盖z-index：1的。

- **结论：**
  - 千万不要把层叠水平和CSS的z-index属性混为一谈。没错，某些情况下z-index确实可以影响层叠水平，但是，只限于定位元素以及flex盒子的孩子元素；而层叠水平所有的元素都存在。

## 层叠上下文的特性

- 准则
  - 谁大谁上：当具有明显的层叠水平标示的时候，如识别的z-indx值，在同一个层叠上下文领域，层叠水平值大的那一个覆盖小的那一个。通俗讲就是官大的压死官小的。
  - 后来居上：当元素的层叠水平一致、层叠顺序相同的时候，在DOM流中处于后面的元素会覆盖前面的元素。
    在CSS和HTML领域，只要元素发生了重叠，都离不开上面这两个黄金准则。
- 特性
  - 层叠上下文的层叠水平要比普通元素高；
  - 层叠上下文可以嵌套，内部层叠上下文及其所有子元素均受制于外部的层叠上下文。
  - 每个层叠上下文和兄弟元素独立，也就是当进行层叠变化或渲染的时候，只需要考虑后代元素。
  - 每个层叠上下文是自成体系的，当元素发生层叠的时候，整个元素被认为是在父层叠上下文的层叠顺序中。

# Flex布局

[CSS之关于弹性盒子 你了解哪些（flex基本属性详解](https://yuguang.blog.csdn.net/article/details/114285620)

- Flex定义:

  - Flex 是 Flexible Box 的缩写，意为"弹性布局"，用来为盒状模型提供最大的灵活性。
  - **注意：**这是您需要在父容器上设置的唯一属性，它的所有直接子容器将自动变为flex项目。

  ```css
  .box{
      display: flex;
      display: -webkit-flex; /* 如果 Webkit 内核浏览器 */
      display: inline-flex; /* 如果 你希望它是行内元素 */
  }
  ```

- **弹性盒子**的属性:

  - 采用 Flex 布局的元素，称为 Flex 容器（flex container），简称"容器"。

  - 它的所有子元素自动成为容器成员，称为 Flex 项目（flex item），简称"项目"。

- 容器默认存在两根轴：

  - 水平的主轴（main axis）
    - 主轴的开始位置叫做`main-start`;
    - 结束位置叫做`main-end`;

  - 垂直的交叉轴（cross axis）

    - 交叉轴的开始位置叫做`cross-start`;
    - 结束位置叫做`cross-end`;

    ![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/flex.png)

- 属性

  - flex-direction属性

    - flex-direction属性决定主轴的方向（即项目的main-axis方向）。
    - 取值：
      - row（默认值）：主轴为水平方向，起点在左端。
      - row-reverse：主轴为水平方向，起点在右端。
      - column：主轴为垂直方向，起点在上沿。
      - column-reverse：主轴为垂直方向，起点在下沿。

  - flex-wrap属性

    - 最初的flexbox概念是在一行中设置其项目的容器。该flex-wrap属性控制flex容器是以单行还是多行布置其项目，以及新行的堆叠方向。

    - 取值：

      - nowrap（默认值）：项目显示在一行中，默认情况下会缩小它们以适应Flex容器的宽度;

      - wrap：如果需要，从左到右和从上到下，弹性项目将显示在多行中;

      - wrap-reverse：如果需要，从左到右和从下到上，弹性项目将显示在多行中;

  -  flex-flow

    - flex-flow属性是flex-direction属性和flex-wrap属性的简写形式，默认值为row nowrap。

  - justify-content属性

    - 使flex项目沿着flex容器当前行的主轴对齐。当一行上的所有伸缩项目都不灵活或已达到最大大小时，它有助于分配剩余的可用空间。

    - 取值：（下面假设主轴为从左到右。）

      - flex-start（默认值）：左对齐；

      - flex-end：右对齐；

      - center： 居中；

      - space-between：两端对齐，项目之间的间隔都相等；

      - space-around：每个项目两侧的间隔相等。

  - align-items属性

    - align-items属性定义项目在交叉轴上如何对齐。

    - 取值：（下面假设交叉轴从上到下。）

      - stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

      - flex-start：交叉轴的起点对齐。

      - flex-end：交叉轴的终点对齐。

      - center：交叉轴的中点对齐。

      - baseline: 项目的第一行文字的基线对齐。

  -  align-content属性

    - align-content属性定义了多根轴线的对齐方式。如果项目只有一根轴线，该属性不起作用。
    - 当存在多个轴时，此属性会在Flex容器内将Flex容器的轴线以接近justify-content的方式对齐。
    - 取值：
      - flex-start：与交叉轴的起点对齐。
      - flex-end：与交叉轴的终点对齐。
      - center：与交叉轴的中点对齐。
      - space-between：与交叉轴两端对齐，轴线之间的间隔平均分布。
      - space-around：每根轴线两侧的间隔都相等。所以，轴线之间的间隔比轴线与边框的间隔大一倍。
      - stretch（默认值）：轴线占满整个交叉轴。

- 项目的属性

  - order

    - order属性定义项目的排列顺序。数值越小，排列越靠前，默认为0。

  -  flex-grow

    - 此属性指定的缩放，该属性确定当分配正的自由空间时，`缩放项目`相对于`容器`中其余`其余项目`将增长多少。
    - 注意：flex-grow：默认为0，即如果存在剩余空间，也不放大。

  - flex-shrink属性

    - flex-shrink的参数指定弹性收缩因子，该因子确定在分配负的自由空间时，弹性项目相对于弹性容器中其余弹性项目将收缩多少。

  - flex-basis属性

    - flex-basis属性定义了在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小。
    - 该属性采用与width和height属性相同的值，并在根据弹性系数分配可用空间之前指定弹性项目的初始主要尺寸。

  - flex

    - 此属性是`flex-grow`，`flex-shrink`和`flex-basis`的简写。默认值为`0 1 auto`。

    - 该属性有两个快捷值：

      - auto (1 1 auto)

      - none (0 0 auto)

  - align-self属性

    - `align-self`属性允许单个项目有与其他项目不一样的对齐方式，可覆盖align-items属性。默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch。

# Grid布局

[CSS进阶之关于网格布局(Grid) 你了解哪些](https://yuguang.blog.csdn.net/article/details/116856395)

- 基本概念

  - “容器”和“项目”
    - 采用网格布局的区域，称为"容器"（container）。容器内部采用网格定位的子元素，称为"项目"（item）
    - 最外层的`<div>`元素就是容器，内层的三个`<div>`元素就是项目
    - 注意：项目只能是容器的顶层子元素（直属子元素），不包含项目的子元素。Grid 布局只对项目生效。
  - 行、列、单元格
    - 容器里面的水平区域称为"行"（row），垂直区域称为"列"（column）。
    - 行和列隔开的格子，被称作“单元格”
  - 网格线
    - 划分网格的线（单元格），称为"网格线"（grid line）。水平网格线划分出行，垂直网格线划分出列。

- 容器基本属性

  - display

    - 当给元素设置为`display: grid;`后，默认情况下，容器元素都是块级元素，但也可以设成行内元素`display: inline-grid;`。

  - grid-template-columns、grid-template-rows

    - grid-template-columns: 定义每一列的列宽
    - grid-template-rows: 定义每一行的行高。

  - repeat()方法

    - repeat()接受两个参数，第一个参数是重复的次数（上例是 3），第二个参数是所要重复的值。
    - repeat()重复某种模式也是可以的。

    ```css
    <style>
      .grid {
        grid-template-rows: repeat(3, 100px);
        grid-template-columns: repeat(3, 100px);
      }
    </style>
    ```

  - auto-fill 关键字

    - 有时，单元格的**大小是固定的**，但是**容器的大小不确定**。如果希望每一行（或每一列）容纳尽可能多的单元格，这时可以使用 auto-fill 关键字表示自动填充。

    ```css
    .grid {
      grid-template-columns: repeat(auto-fill, 100px);
      grid-template-rows: repeat(2, 100px);
    }
    ```

  - fr(片段)

    - 网格布局提供了**fr 关键字**（fraction 的缩写，意为"片段"）。如果两列的宽度分别为 1fr 和 2fr，就表示后者是前者的两倍。
    - fr 可以与绝对长度的单位结合使用，这时会非常方便：例如下面会显示为第一列 100px，剩余宽度内第三列是是第二列的二倍

    ```css
    .grid {
      display: grid;
      grid-template-columns: 1fr 2fr;
      /*grid-template-columns: 100px 1fr 2fr;*/
    }
    ```

  - auto

    - auto 关键字表示由浏览器自己决定长度。
    - `grid-template-columns: 100px auto 100px;`

  - 网格线的名称

    - `grid-template-columns`属性和`grid-template-rows`属性里面，还可以使用方括号，指定每一根网格线的名字，方便以后的引用。
    - `grid-template-columns: [c1] 100px [c2] auto [col-3 c3] 100px;`

  - grid-row-gap、grid-column-gap、grid-gap 属性

    - grid-row-gap属性设置行与行的间隔（行间距）
    - grid-column-gap属性设置列与列的间隔（列间距）
    - grid-gap`grid-gap: <grid-row-gap> <grid-column-gap>`，它是行列间距的缩写

  - grid-template-areas 属性

    - 网格布局允许指定"区域"（area），一个区域由单个或多个单元格组成。grid-template-areas 属性用于定义区域。

    ```css
    .grid {
      display: grid;
      grid-template-columns: 100px 100px 100px;
      grid-template-rows: 100px 100px 100px;
      grid-template-areas:
        "a b c"
        "d e f"
        "g h i";
    }
    .a {
        grid-area: a; // 表示它代表grid容器内的a项目
    }
    ```

  - justify-items、align-items、place-items 属性

    - justify-items：设置单元格内容的水平位置（左中右）；
    - align-items：设置单元格内容的垂直位置（上中下）；
    - 取值范围：
      - start：对齐单元格的起始边缘。
      - end：对齐单元格的结束边缘。
      - center：单元格内部居中。
      - stretch：拉伸，占满单元格的整个宽度（默认值）。
    - **place-items 是上面两个属性的简写形式**：`place-items: <align-items> <justify-items>;`，

  - justify-content、align-content、place-content 属性

    - justify-content 属性是整个内容区域在容器里面的水平位置（左中右）
    - align-content 属性是整个内容区域的垂直位置（上中下）。
    - 同样`place-content`也是前两个属性的简写形式。

  - grid-auto-columns、grid-auto-rows 属性

    - 有时候，一些项目的指定位置，在现有网格的外部。比如网格只有3列，但是某一个项目指定在第5行。这时，浏览器会自动生成多余的网格，以便放置项目。
    - `grid-auto-columns`属性和`grid-auto-rows`属性用来设置，浏览器自动创建的多余网格的列宽和行高。

- 项目基本属性
  - 垂直网格线
    - grid-column-start：项目左起始网格线
    - grid-column-end：项目右结束网格线
    - grid-row-start 项目上起始网格线
    - grid-row-end 项目下结束网格线
    - grid-column：是`grid-column-start`和`grid-column-end`的合并简写形式
    - grid-row：`grid-row-start`和`grid-row-end`的合并简写形式
  - grid-area 属性
    - grid-area属性指定项目放在哪一个区域。
    - **注意：**grid-area还有另一种使用方式，他可以作为作为`grid-row-start`、`grid-column-start`、`grid-row-end`、`grid-column-end`的合并简写形式，直接指定项目的位置。
    - `grid-area: 1 / 1 / 2 / 2;`