# Vue

### Vue3与Vue2的区别

[vue2与vue3的区别](https://blog.csdn.net/weixin_43638968/article/details/108800361?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164260997516780255263306%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164260997516780255263306&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-108800361.pc_search_result_control_group&utm_term=vue3%E4%B8%8Evue2%E7%9A%84%E5%8C%BA%E5%88%AB&spm=1018.2226.3001.4187)

- vue2 的双向数据绑定是利用ES5 的一个 API Object.definePropert()对数据进行劫持 结合 发布订阅模式的方式来实现的。
  
- VUE实现双向数据绑定的原理就是利用了 Object.defineProperty() 这个方法重新定义了对象获取属性值(get)和设置属性值(set)的操作来实现的。
  
- set 与 get函数中使用了全局变量Dep，更新时通知watcher，watcher调用update函数执行compiler中的回调；设值时在dep中注册一个观察者。
  
  > - [Vue双向数据绑定原理解析及代码实现](https://blog.csdn.net/wuxy720/article/details/80151610?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239745516780255291368%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239745516780255291368&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-80151610.pc_search_result_cache&utm_term=vue%E5%8F%8C%E5%90%91%E7%BB%91%E5%AE%9A%E5%8E%9F%E7%90%86&spm=1018.2226.3001.4187)
  > - 要点：数据劫持+观察者（发布者-订阅者）模式
  > - 核心：Object.defineProperty()
  >   - 语法：Object.defineProperty(obj, prop, descriptor)
  >     - obj：要在其上定义属性的对象。
  >     - prop：要定义或修改的属性的名称。
  >     - descriptor：将被定义或修改的属性描述符。![Object.defineProperty](/Users/wangke/Desktop/收集/图片/发布者-订阅者模式.png)
  > - **碎片化文档**：DOM节点的容器，例如把创建的节点放容器中再插入DOM树可以只回流一次减少资源损耗
  > - **数据劫持**：如果使用appendChid方法将原dom树中的节点添加到DocumentFragment中时，会删除原来的节点
  
  - Vue的双向数据绑定在底层运用到了三大模块：Observer数据监听器，Compiler指令解析器和Watcher订阅者。
    - Observer负责对所有的数据对象里面所有的属性进行监听，也就是对**data**里面所有的属性进行监听。监听就是进行**数据劫持**，一旦监听到了数据的变化，它就会通知订阅者。
    - Compiler是指令解析器，用来扫描实例关联的模板，在扫描的过程中，它会对模板里面的指令进行解析，然后绑定指定的事件，它也会订阅模板里面的数据变化，绑定一个更新函数给到Watcher
    - Watcher 订阅者，watch用来关联observer以及compiler, 能够订阅并且收到所有属性变化的通知，然后同时他一旦订阅到了，就会执行指令绑定的相应的操作，然后通过它来更新对应的视图，通过调用update()方法来更新视图。update是watcher自身的一个方法，主要用于执行compiler里面的一些回调，因为compiler主要是用来扫描模板的，同时对里面的一些指令进行解析，绑定事件，绑定的事件有回调，也就是说 触发compiler里面的回调，从而更新界面。

![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/观察者模式.png)

- vue3 中使用了 es6 的 ProxyAPI 对数据代理。

  - 使用Object.defineProperty()的缺点：

    - Object.defineProperty无法监控到数组下标的变化，导致直接通过数组的下标给数组设置值，不能实时响应
    - Object.defineProperty只能劫持对象的属性,因此我们需要对每个对象的每个属性进行遍历

  - Proxy 可以理解成，在目标对象之前架设一层“拦截”，外界对该对象的访问，都必须先通过这层拦截，因此提供了一种机制，可以对外界的访问进行过滤和改写。

  - 相比于vue2.x，使用proxy的优势如下

    - defineProperty只能监听某个属性，不能对全对象监听

    - 可以省去for in、闭包等内容来提升效率（直接绑定整个对象即可）

    - 可以监听数组，不用再去单独的对数组做特异性操作 vue3.x可以检测到数组内部数据的变化


- 其他区别
  - Vue2使用选项类型API（Options API）对比Vue3合成型API（Composition API），旧的选项型API在代码里分割了不同的属性: data,computed属性，methods，等等。新的合成型API能让我们用方法（function）来分割，相比于旧的API使用属性来分组，`这样代码会更加简便和整洁`。
  - 生命周期钩子变化 setup（） onBeforedMounted（）
  - data变成setup+reactive来响应

### MVVM

**MVC：**[Vue双向数据绑定](https://blog.csdn.net/weixin_44585214/article/details/114481445?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164264928216780271964166%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164264928216780271964166&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-114481445.pc_search_result_control_group&utm_term=vue%E5%8F%8C%E5%90%91%E6%95%B0%E6%8D%AE%E7%BB%91%E5%AE%9A&spm=1018.2226.3001.4187)

- M是指业务模型，V是指用户界面，C则是控制器：

  - Model层用来存储业务的数据，一旦数据发生变化，模型将通知有关的视图。

    Model和View之间使用了观察者模式，View事先在此Model上注册，进而观察Model，以便更新在Model上发生改变的数据。

  - V即View视图, 视图层。

    view和controller之间使用了策略模式，View引入了Controller的实例来实现特定的响应策略。如果要实现不同的响应策略只要用不同的Controller实例替换即可。

  - 控制器是模型和视图之间的纽带。
    MVC将响应机制封装在controller对象中，当用户和你的应用产生交互时，控制器中的事件触发器就开始工作了。

[什么是MVVM](https://blog.csdn.net/suzan_bingtong/article/details/103438639?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239634516781685336967%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239634516781685336967&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-103438639.pc_search_result_cache&utm_term=MVVM&spm=1018.2226.3001.4187)

- 定义：Model-View-ViewModel的简写。它本质上就是MVC 的改进版。
  - M是逻辑方法加上数据，V就是用户看到的界面，VM就是逻辑方法加上界面渲染的代码，例如HTML。
  - 视图：就像在MVC和MVP模式中一样，视图是用户在屏幕上看到的结构、布局和外观（UI）。
  - 视图模型：视图模型是暴露公共属性和命令的视图的抽象。MVVM没有MVC模式的控制器，也没有MVP模式的presenter，有的是一个绑定器。在视图模型中，绑定器在视图和数据绑定器之间进行通信。
  - 模型：模型是指代表真实状态内容的领域模型（面向对象），或指代表内容的数据访问层（以数据为中心）。
  
- 优点：
  > - 低耦合：视图（View）可以独立于Model变化和修改，一个ViewModel可以绑定到不同的"View"上，当View变化的时候Model可以不变，当Model变化的时候View也可以不变。
  > - 可重用性：你可以把一些视图逻辑放在一个ViewModel里面，让很多view重用这段视图逻辑。
  > - 独立开发：开发人员可以专注于业务逻辑和数据的开发（ViewModel），设计人员可以专注于页面设计，使用Expression Blend可以很容易设计界面并生成xaml代码。
  > - 可测试：界面素来是比较难于测试的，测试可以针对ViewModel来写。
  
  - 比MVC/MVP精简了很多，不仅仅简化了业务与界面的依赖，还解决了数据频繁更新（以前用jQuery操作DOM很繁琐）的问题。
  - 在MVVM中，View不知道Model的存在，ViewModel和Model也察觉不到View，这种低耦合模式可以使开发过程更加容易，提高应用的可重用性。

### Vue生命周期

- 定义：Vue 实例从创建到销毁的过程，就是生命周期。也就是从开始创建、初始化数据、编译模板、挂载Dom→渲染、更新→渲染、卸载等一系列过程，我们称这是 Vue 的生命周期。

- 生命周期函数：

  1、beforeCreate（创建前）

  表示实例完全被创建出来之前，vue 实例的挂载元素$el和数据对象 data 都为 undefined，还未初始化。

  2、created（创建后）

  数据对象 data 已存在，可以调用 methods 中的方法，操作 data 中的数据，但 dom 未生成，$el 未存在 。

  3、beforeMount（挂载前）

  vue 实例的 $el 和 data 都已初始化，挂载之前为虚拟的 dom节点，模板已经在内存中编辑完成了，但是尚未把模板渲染到页面中。data.message 未替换。

  4、mounted（挂载后）

  vue 实例挂载完成，data.message 成功渲染。内存中的模板，已经真实的挂载到了页面中，用户已经可以看到渲染好的页面了。实例创建期间的最后一个生命周期函数，当执行完 mounted 就表示，实例已经被完全创建好了，DOM 渲染在 mounted 中就已经完成了。

  5、beforeUpdate（更新前）

  当 data 变化时，会触发beforeUpdate方法 。data 数据尚未和最新的数据保持同步。

  6、updated（更新后）

  当 data 变化时，会触发 updated 方法。页面和 data 数据已经保持同步了。

  7、beforeDestory（销毁前）

  组件销毁之前调用 ，在这一步，实例仍然完全可用。

  8、destoryed（销毁后）

- nextTick原理：[vue的nextTick原理](https://blog.csdn.net/chenzeze0707/article/details/90083725?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239717116781685354402%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239717116781685354402&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-90083725.pc_search_result_cache&utm_term=vue+nexttick%E5%8E%9F%E7%90%86&spm=1018.2226.3001.4187)

  - 定义：根据官方文档的解释，它可以在DOM更新完毕之后执行一个回调

  - nextTick是全局vue的一个函数，在vue系统中，用于处理dom更新的操作。vue里面有一个watcher，用于观察数据的变化，然后更新dom，vue里面并不是每次数据改变都会触发更新dom，而是将这些操作都缓存在一个队列，在一个事件循环结束之后，刷新队列，统一执行dom更新操作。 

    在vue生命周期的created()钩子函数进行的DOM操作要放在Vue.nextTick()的回调函数中，因为created()钩子函数执行的时候DOM并未进行任何渲染，而此时进行DOM操作是徒劳的，所以此处一定要将DOM操作的JS代码放进Vue.nextTick()的回调函数中。

    而与之对应的mounted钩子函数，该钩子函数执行时所有的DOM挂载和渲染都已完成，此时该钩子函数进行任何DOM操作都不会有个问题。 

### Vue组件通信

[Vue组件间的通信](https://blog.csdn.net/m0_37564404/article/details/82466289?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239787816780255229670%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239787816780255229670&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-82466289.pc_search_result_cache&utm_term=vue%E7%BB%84%E4%BB%B6%E9%80%9A%E4%BF%A1&spm=1018.2226.3001.4187)

- **使用props属性。**
  -   props主要用于父组件传递数据给子组件，是你可以在组件上注册一些自定义特性。当一个值传递给一个prop特性的时候，它就变成了那个组件实例的一个属性。这样在子组件就可以使用该该值。请注意：所有的prop都使得期父子prop之间形成了一个单向下行绑定，即父级prop的更新会向下流动到子组件，但是反过来就不行，子组件不能改变父组件的状态。
  - 每次父组件发生更新时，子组件中所有的prop都会被刷新为最新的值。
- **使用Vue自定义事件。**
  - 父组件可以在使用子组件的地方直接用 v-on来监听子组件触发的事件 。即父组件中使用 v-on绑定自定义事件，然后在子组件中使用 $emit(eventName,data)触发事件。
  - 每个Vue对象实例都实现了事件接口，所以可以使用 $on(eventName)监听事件，使用$emit 来触发事件.
- **消息订阅与发布(PubSubJS库)**
- **组件间通信：Slot** 
- **vuex通信**

### Vue diff策略

[Vue中的Diff算法](https://blog.csdn.net/qq_34179086/article/details/88086427?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239822316780269882554%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239822316780269882554&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-1-88086427.pc_search_result_cache&utm_term=vue+diff&spm=1018.2226.3001.4187)

- 为什么要用Diff算法
  - 由于在浏览器中操作DOM的代价是非常“昂贵”的，所以才在Vue引入了Virtual DOM
  - Virtual DOM是对真实DOM的一种抽象描述，不懂的朋友可以自行查阅相关资料。
- React的开发者结合Web界面的特点做出了两个大胆的假设，使得Diff算法复杂度直接从O(n^3)降低到O(n)，假设如下：
  - 两个相同组件产生类似的DOM结构，不同的组件产生不同的DOM结构；
  - 对于同一层次的一组子节点，它们可以通过唯一的id进行区分。
- Vue的Diff算法与上面的思路大体相似，只比较同级的节点，若找不到与新节点类型相同的节点，则插入一个新节点，若有相同类型的节点则进行节点属性的更新，最后删除新节点列表中不包含的旧节点。

### Vue 虚拟DOM

[vue中的虚拟dom](https://blog.csdn.net/yuan_me_da/article/details/103690141?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164239807516781683913555%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164239807516781683913555&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-3-103690141.pc_search_result_cache&utm_term=vue%E8%99%9A%E6%8B%9Fdom%EF%BC%88virtual+dom%EF%BC%89&spm=1018.2226.3001.4187)

- 虚拟DOM就是使用js的object模拟真实的dom，当状态发生变化，更新之前做diff，达到最少操作dom的效果
- 访问DOM是非常昂贵的，会造成相当多得性能浪费，所以我们试想，**当某个状态发生变化时，只更新与这个状态相关联的DOM节点**。虚拟DOM就是解决方案之一。**所以虚拟DOM旨在避免不必要的DOM操作**。
- vue为什么引入虚拟DOM?
  - vue1.0响应式粒度太细，Object.defineProperty()每个数据的修改都会通知watcher，进而通知dom去改变，对大型项目来说是一个噩梦！内存开销非常大。
  - vue2.0引入虚拟dom，通过diff之后再通知dom去改变，相对于1.0响应式的级别修改了，watcher只到组件，组件内部使用虚拟dom
- vue中虚拟DOM干了啥?
  - 提供与真实dom节点对应的虚拟节点vnode
  - 状态发生变化时，对比新旧两个vnode，更新视图。
- vue中的虚拟DOM如何创建？
  - `vue-loader` 允许我们直接在template中编写模板字符串，将内容提取出来给vue-template-compiler，Vue.js通过编译器将模板转换成渲染函数中的内容，执行这个函数可以得到一个vnode树，使用这个虚拟节点树就可以渲染页面了。

### Vue计算属性

计算属性只在相关响应式依赖发生改变时它们才会重新求值

### vue-router实现懒加载

[vue-router路由懒加载及实现的方式](https://blog.csdn.net/MISS_zhang_0110/article/details/118330741?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164208943416780357273028%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164208943416780357273028&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-118330741.pc_search_result_control_group&utm_term=vue-router%E5%AE%9E%E7%8E%B0%E6%87%92%E5%8A%A0%E8%BD%BD&spm=1018.2226.3001.4187)

定义：延迟加载，即在需要的时候进行加载，随用随载。

场景：项目打包时所有Component都会打包到一个js中，项目打开时加载很慢

使用：

​	语法：component:() => import(’./About.vue’)；

```js
//主要这句话
const router = new VueRouter({  
  routes: [   
   	  { path: '/about', 
   	  component:  () => import('./About.vue') }]
   })
```

#### vue loader的工作原理 

> webpack 是只识别 js 代码的。但是我们写的代码中有很多类型的文件，比如：.vue、.yaml、.json、.css、.tsx 等等这些后缀文件，这些文件都是不被 webpack 所识别的，因此需要在webapck 打包前进行“翻译”。loader 的作用就是“翻译”的作用，将非 js 文件进行转义成 js 代码，然后 webpack 才会识别。

将.vue文件转换为js代码以被webpack识别，用一个Parse函数将vue文件中js、html、css代码分离，然后包装一下给webpack

[vue-loader 源码分析](https://blog.csdn.net/qq_42535651/article/details/109155806?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164000539516780265484592%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164000539516780265484592&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-10-109155806.pc_search_insert_es_download&utm_term=vue+loader%E7%9A%84%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86+&spm=1018.2226.3001.4187)

#### 如果你自己设置vue loader该怎么做 

1. 检索所有vue文件，拿到路径、名字和内容
2. 找到Template标签，拿正则表达式匹配，把里面的内容拿出来就是html代码
3. 同理可以拿到js代码和css代码，然后存起来

#### vue的响应式怎么实现的

[vue的响应式](https://blog.csdn.net/qq_40619263/article/details/105600706?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164212929816780269862442%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164212929816780269862442&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-105600706.pc_search_result_control_group&utm_term=vue%E5%93%8D%E5%BA%94%E5%BC%8F&spm=1018.2226.3001.4187)

创建vue实例的时候，vue会将data中的成员代理给vue实例，目的是为了实现响应式

#### Vue好处的理解

- 视图,数据,结构分离
- 双向数据绑定
- 组件化
- 虚拟DOM

[vue的优点？](https://blog.csdn.net/a2724265459/article/details/107453015?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164005699116780271924335%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164005699116780271924335&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-107453015.pc_search_insert_es_download&utm_term=Vue%E4%BC%98%E7%82%B9&spm=1018.2226.3001.4187)

#### 对vue源码的学习情况
