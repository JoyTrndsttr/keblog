# Vue的特性

## Key的作用

[Vue的特性(一)：key的作用](https://yuguang.blog.csdn.net/article/details/100708542)

- key是为每个vnode指定唯一的id，在同级vnode的Diff过程中，可以根据key快速的进行对比，来判断是否为相同节点，利用 key 的唯一性生成 map 对象来获取对应节点，比遍历方式更快,指定key后,可以保证渲染的准确性(尽可能的复用 DOM 元素。)

- **key的特殊属性主要用在Vue的虚拟Dom算法中，在新旧`nodes（元素节点）`对比时辨识VNodes**
  - 如果不使用 key，Vue 会使用一种最大限度减少动态元素并且尽可能的尝试修复/再利用相同类型元素的算法。使用 key，它会基于 key 的变化重新排列元素顺序，并且会移除 key 不存在的元素。
  - 有相同父元素的子元素必须有独特的 key，重复的 key 会造成渲染错误。



# VueX

[入门Vuex你需要知道这些！](https://yuguang.blog.csdn.net/article/details/105204413)

- 定义：

  - 官方的解释是： Vuex 是一个专为 Vue.js 应用程序开发的状态管理模式。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。

  - 简而言之就是：让数据管理变得更清晰。

  - 这个状态自管理应用包含以下几个部分：

    - state，驱动应用的数据源；

    - view，以声明方式将 state 映射到视图；

    - actions，响应在 view 上的用户输入导致的状态变化。