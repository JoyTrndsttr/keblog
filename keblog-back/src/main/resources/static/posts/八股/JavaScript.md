### var let const以及变量提升

### 模板字符串

### map和reduce区别

<img src="https://img-blog.csdn.net/20180226161552256" alt="img" style="zoom:50%;" />

【得分点】

map创建新数组、map返回处理后的值、forEach()不修改原数组、forEach()方法返回undefined

【参考答案】

标准回答

map 和 forEach 的区别：map有返回值，可以开辟新空间，return出来一个length和原数组一致的数组，即便数组元素是undefined或者是null。forEach默认无返回值，返回结果为undefined，可以通过在函数体内部使用索引修改数组元素。

加分回答

map的处理速度比forEach快，而且返回一个新的数组，方便链式调用其他数组新方法，比如filter、reduce

> let arr = [1, 2, 3, 4, 5];
>
> let arr2 = arr.map(value => value * value).filter(value => value > 10);
>
> // arr2 = [16, 25]

【延伸阅读】

forEach处理数组

> var arr = [1,2,3,4]
>
> arr.forEach((value, key) => {
>
>  return arr[key] = value * value;
>
> });

map处理数组

> var arr = [1,2,3,4]
>
> let list = arr.map(value => {
>
>  return value * value;
>
> });

reduce坑：[JS操作数组的reduce无法拿到初始值或者无法操作第一个值](https://blog.csdn.net/weixin_46176363/article/details/110443320?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164242503416780261913564%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164242503416780261913564&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-110443320.pc_search_result_control_group&utm_term=js+reduce%E5%88%9D%E5%A7%8B%E5%80%BC&spm=1018.2226.3001.4187)

### call apply bind的区别

call和apply区别主要是传参，call一个一个传或用ES6的spread数组,bind返回一个函数需要再次调用

```js
obj.myFunc.call(db, '1', '2')
obj.myFunc.apply(db, [1, 2])
obj.myFunc.bind(db, '1', '2')()
```

[call apply bind的区别](https://blog.csdn.net/qq_29918313/article/details/92767313?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163957393816780274187502%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=163957393816780274187502&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-92767313.pc_search_insert_es_download&utm_term=call+apply+bind%E7%9A%84%E5%8C%BA%E5%88%AB&spm=1018.2226.3001.4187)

### js事件循环机制的理解

主线程运行时会产生执行栈，栈中的代码调用某些api时，它们会在事件队列中添加各种事件，而栈中的代码执行完毕，就会读取事件队列中的事件，去执行那些回调，如此循环

<img src="/Users/wangke/Library/Application Support/typora-user-images/image-20211215214013066.png" alt="image-20211215214013066" style="zoom: 50%;" />

### js原型链的理解

从设计模式上来讲，原型链属于原型模式，本质是通过复制原型来创建新的对象。任何对象都有原型对象，原型可以继承，当访问对象成员的时候会从自身开始往原型链上找，直到找到Object然后undefined。

[js原型和原型链你只要看这一篇](https://blog.csdn.net/shuixiou1/article/details/81048816?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522163957605816780271599806%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=163957605816780271599806&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-81048816.pc_search_insert_es_download&utm_term=js%E5%8E%9F%E5%9E%8B%E9%93%BE&spm=1018.2226.3001.4187)

- ##### 构造函数的理解


```js
function Person() {}
var p = new Person();
```

用function声明的都是函数，而如果直接调用的话，那么Person()就是一个普通函数，**只有用函数new产生对象**时，这个函数才是new出来对象的**构造函数**。

- ##### 原型的理解


任何对象都有原型对象

对象由构造函数创建

对象的_ proto_属性=构造函数的prototype

对象的construct = 构造函数本身

- ##### 原型继承


```js
Person.prototype = parent
```

- ##### 属性搜索原则

当访问一个对象的成员的时候，会现在自身找有没有,如果找到直接使用如果没有找到，则去**原型链指向的对象的构造函数的prototype**中找，找到直接使用，没找到就返回undifined或报错。

### js数据类型

> 原始值类型：string number boolean null undifined
>
> 对象类型：object

1.基本类型：Underfined ,Null, [Boolean](https://so.csdn.net/so/search?q=Boolean&spm=1001.2101.3001.7020),Number,String

2.引用类型： Object，Array，Date，Function

### 判断类型

typeof判断基本数据类型（null会误判为object）

instanceof判断复杂数据类型（数组会判为object）

toString.call()准确判断数据类型

[js 判断数据类型](

### 回调函数理解

我们先来看看回调的英文定义：A callback is a function that is passed as an argument to another function and is executed after its parent function has completed。

　　字面上的理解，回调函数就是传递一个参数化的函数，就是将这个函数作为一个参数传到另一个主函数里面，当那一个主函数执行完之后，再执行传进去的作为参数的函数。走这个过程的参数化的函数 就叫做回调函数。换个说法也就是被作为参数传递到另一个函数（主函数）的那个函数就叫做 回调函数。

    　举一个别人举过的例子：约会结束后你送你女朋友回家，离别时，你肯定会说：“到家了给我发条信息，我很担心你。” 对不，然后你女朋友回家以后还真给你发了条信息。小伙子，你有戏了。其实这就是一个回调的过程。你留了个参数函数（要求女朋友给你发条信息）给你女朋友，然后你女朋友回家，回家的动作是主函数。她必须先回到家以后，主函数执行完了，再执行传进去的函数，然后你就收到一条信息了。

[JS回调函数——简单易懂有实例](https://blog.csdn.net/hu_belif/article/details/80284140)

### JS判断[] {} null undefiend

[js 对象{}与null的区别及[]](https://blog.csdn.net/bingqise5193/article/details/101114911?ops_request_misc=&request_id=&biz_id=102&utm_term=js%20%5B%5D%20null%20===&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-1-101114911.pc_search_result_control_group&spm=1018.2226.3001.4187)

判断数组为空用 [].length == 0

如果可能传过来null，也有可能传过来数组，并且不希望空数组执行语句，则可以 if（res && res.length）位置不能互换

判断对象为空用 if(Object.keys(obj).length)

### 闭包

[JavaScript之闭包，给自己的Js一场重生（系列七）](https://blog.csdn.net/jbj6568839z/article/details/106940646?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164234536216780366515463%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164234536216780366515463&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_positive~default-1-106940646.pc_search_result_control_group&utm_term=js%E9%97%AD%E5%8C%85&spm=1018.2226.3001.4187)

定义：

- #### 闭包是函数内部的子函数

- #### 闭包就是能够读取其他函数内部变量的函数，在本质上是函数内部和函数外部链接的桥梁

- #### 函数和对其周围状态（词法环境）的引用捆绑在一起构成闭包（closure）

### 箭头函数的this问题

[【ES6】箭头函数this指向问题【看这一篇就够啦！】](https://blog.csdn.net/weixin_43352901/article/details/107913194?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164234772816780265489001%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164234772816780265489001&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-1-107913194.pc_search_result_control_group&utm_term=%E7%AE%AD%E5%A4%B4%E5%87%BD%E6%95%B0this%E6%8C%87%E5%90%91&spm=1018.2226.3001.4187)

绑定定义时的作用域，而不是运行时所在的作用域

### Promise对象

链接：[Promise对象详解](https://blog.csdn.net/mafan121/article/details/72537142?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164205474216780271521782%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164205474216780271521782&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-72537142.pc_search_result_control_group&utm_term=promise%E5%AF%B9%E8%B1%A1&spm=1018.2226.3001.4187)

- Promise是抽象异步处理对象以及对其进行各种操作的组件。

- 有两种状态

  - promise对象被 resolve 时的处理(onFulfilled)
  - promise对象被 reject 时的处理(onRejected)

- 创建Promise对象分为两步

  - 创建Promise对象

    ```js
    new Promise(function(resolve,reject){
       //业务逻辑
       //处理结果正确就调用resolve方法
       //处理逻辑错误叫调用reject方法
    })
    ```

  - 调用Promise实例的then()、catch()方法，异步处理完成就执行then方法，处理异常就执行catch方法。

    ```js
    function asyncTest(){
       return new Promise(function (resolve, reject) {
            setTimeout(function () {
                resolve('Async Hello world');//使promise对象立即进入onResolved状态，并且将value参数传给then方法
              	//reject(error);             //使promise对象立即进入onRejected状态，并且将error参数传给catch方法
            }, 16);
        })
    }
    
    asyncTest().then(function (value) {    //then(fn):该方法是用来注册Promise实例的状态为onFulfilled时的回调函数
        console.log(value);    // => 'Async Hello world'
    }).catch(function (error) {            //catch(fn):该方法是用来注册Promise实例的状态为onRejected时的回调函数
        console.log(error);
    })
    ```

- 注意：then和catch返回的都是一个全新的Promise对象，在执行这两个方法后，不论返回的数据类型是什么，都会被包装成一个全新的Promise对象。返回的数据会传递到下一个链式方法里作为参数。

- Promise.all(array):

  - 接收一个 promise对象的数组作为参数，当这个数组里的所有promise对象全部变为resolve或reject状态的时候，它才会去调用  .then 方法。

  ```js
  var promise1 = new Promise(function (resolve){
      resolve("promise1 is resolve");
  });
  var promise2 = new Promise(function (resolve){
      resolve("promise2 is resolve");
  });
  
  function main(){
      return Promise.all([promise1,promise2])
  }
  main().then(function(value){
      console.log(value)
  })
  //执行结果:
  //["promise1 is resolve", "promise2 is resolve"]
  ```

- Promise.race(array):

  - 接收一个 promise对象的数组作为参数，当这个数组里只要有一个promise对象进入reject状态的时候，它才会去调用  .then  方法。

  ```js
  // delay毫秒后执行resolve
  function timerPromisefy(delay) {
      return new Promise(function (resolve) {
          setTimeout(function () {
              resolve(delay);
          }, delay);
      });
  }
  // 任何一个promise变为resolve或reject 的话程序就停止运行
  Promise.race([
      timerPromisefy(1),
      timerPromisefy(32),
      timerPromisefy(64),
      timerPromisefy(128)
  ]).then(function (value) {
      console.log(value);    // => 1
  });
  ```

