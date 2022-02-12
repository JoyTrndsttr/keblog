# JS好好学习总结

## this指向,this、call、bind

[this指向详解，思维脑图与代码的结合，让你一篇搞懂this、call、apply。系列（一）](https://yuguang.blog.csdn.net/article/details/106479511)

### this指向

<img src="https://img-blog.csdnimg.cn/20200602110330766.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2piajY1Njg4Mzl6,size_16,color_FFFFFF,t_70#pic_center" alt="img" style="zoom:25%;" />

### call、apply和bind

<img src="https://img-blog.csdnimg.cn/20200602153648211.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2piajY1Njg4Mzl6,size_16,color_FFFFFF,t_70#pic_center" alt="img" style="zoom:25%;" />

要点与补充：

- 调用构造函数实现继承：

  ```js
  function Product(name, price) {
  	this.name = name;
  	this.price = price;
  }
  
  function Food(name, price) {
  	Product.call(this, name, price); //
  	this.category = food;
  }
  
  var hotDog = new Food('hotDog', 20);
  ```

- 实现call

  ```js
  Function.prototype.setCall = function (obj) {
      var obj = obj || window;
      obj.fn = this;
      var args = [];
      for(var i = 1, len = arguments.length; i < len; i++) {
      	args.push('arguments[' + i + ']');
    	}
    	var result = eval('obj.fn(' + args +')');
    	delete obj.fn;
    	return result;
  };
  // 测试一下
  var value = 2;
  var obj = { value: 1 };
  
  function bar(name, age) {
    	console.log(this.value);
    	return {
      	value: this.value,
      	name: name,
      	age: age
    	}
  }
  bar.setCall(null); // 2
  console.log(bar.setCall(obj, 'yuguang', 18));
  ```

  - 补充：[js中的eval方法详解（一）–eval方法的初级应用](https://blog.csdn.net/weixin_39256994/article/details/81953200?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164249265016780366574950%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164249265016780366574950&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-81953200.pc_search_result_control_group&utm_term=js+eval&spm=1018.2226.3001.4187)

- bind：返回一个原函数的拷贝，并拥有指定的 this 值

- 箭头函数的this从其作用链域的上一层获得

- 结合代码理解：

  - ```js
    var name = 'window'
    
    var person1 = {
        name: 'person1',
        show1: function () {
            console.log(this.name)
        },
        show2: () => console.log(this.name),
        show3: function () {
            return function () {
                console.log(this.name)
            }
        },
        show4: function () {
            return () => console.log(this.name)
        }
    }
    var person2 = { name: 'person2' }
    
    person1.show1()									//返回person1，this作为对象的属性被调用，this为指向该对象（person1）
    person1.show1.call(person2)			//返回person2，this作为对象的属性被调用，this通过call绑定为person2
    
    person1.show2()									//返回window，箭头函数从自己作用域的上一层继承window
    person1.show2.call(person2)			//返回window，箭头函数从自己作用域的上一层继承window
    
    person1.show3()()								//返回window，person1.show3()返回一个普通函数，this作为普通函数被调用指向全局对象
    person1.show3().call(person2)		//返回person2，person1.show3()返回一个普通函数，this通过call绑定person2
    person1.show3.call(person2)()		//返回window，person1.show3的this绑定person2，通过调用返回一个普通函数，console																	 中的this作为普通函数被调用指向全局对象
    
    person1.show4()()								//返回person1，person1.show4()返回一个箭头函数，从作用链域上一层继承this
    person1.show4().call(person2)		//返回person2，person1.show4()返回一个箭头函数，从作用链域上一层继承this
    person1.show4.call(person2)()   //返回person2，person2.show4的this绑定person2，通过调用返回一个箭头函数，																				console中的this从作用链域上一层继承this
    ```

## 从原型到原型链

[从原型到原型链，修炼JavaScript内功这篇文章真的不能错过！系列（二）](https://yuguang.blog.csdn.net/article/details/106555301)

![原型链示意图](/Users/wangke/Desktop/收集/图片/format,png.png)

### 构造函数与construct

- 构造函数和普通函数的区别在于，使用**new**生成实例的函数就是构造函数，直接调用的就是普通函数。
- `constructor` 返回创建实例对象时构造函数的引用。此属性的值是对函数本身的引用，而不是一个包含函数名称的字符串。
  - 在JavaScript中，每个具有原型的对象都会自动获得constructor属性。除了：arguments、Enumerator、Error、Global、Math、RegExp等一些特殊对象之外，其他所有的JavaScript内置对象都具备constructor属性。例如：Array、Boolean、Date、Function、Number、Object、String等。

- 模拟一个new

  ```js
  var objectNew = function(){
      // 从object.prototype上克隆一个空的对象
      var obj = new Object(); 
      // 取得外部传入的构造器，这里是Person
      var Constructor = [].shift.call( arguments );
      // 更新，指向正确的原型
      obj.__proto__ = Constructor.prototype; //知识点，要考、要考、要考 
      // 借用外部传入的构造器给obj设置属性
      var ret = Constructor.apply(obj, arguments);
      // 确保构造器总是返回一个对象
      return typeof ref === 'object' ? ret : obj;
  }
  ```

- 原型
  - prototype(显式原型）:每个对象都拥有一个原型对象，类是以函数的形式来定义的。prototype表示该函数的原型，也表示一个类的成员的集合。**（个人理解：相当于构造函数与类的关系，但这个“类”是个原型对象）**
  - _ proto_(隐式原型)：这是每一个JavaScript对象(除了 null )都具有的一个属性，叫`__proto__`，这是一个访问器属性（即 getter 函数和 setter 函数），通过它可以访问到对象的内部`[[Prototype]]` (一个对象或 null )。每个引用类型的隐式原型都指向它的构造函数的显式原型。**（个人理解：相当于对象与类的关系）**
  - 原型的原型：原型对象是通过`Object`构造函数生成的，实例的 `__proto__` 指向构造函数的 `prototype` ，可以理解成，`Object.prototype()`是所有对象的根对象

### 原型链

每个对象拥有一个原型对象，通过 `__proto__` 指针指向上一个原型 ，并从中继承方法和属性，同时原型对象也可能拥有原型，这样一层一层，最终指向 `null`。**这种关系被称为原型链** (prototype chain)，通过原型链一个对象会拥有定义在其他对象中的属性和方法。

补充：

- `person.constructor === Person.prototype.constructor`（即`person.__proto__.construct`) 因为当获取 person.constructor 时，其实 person 中并没有 constructor 属性,当不能读取到constructor 属性时，会从 person 的原型也就是 Person.prototype 中读取，正好原型中有该属性
- 其次是 proto ，绝大部分浏览器都支持这个非标准的方法访问原型，然而它并不存在于 Person.prototype 中，实际上，它是来自于 Object.prototype ，与其说是一个属性，不如说是一个 getter/setter，当使用 obj.__ proto__ 时，可以理解成返回了 Object.getPrototypeOf(obj)。
- 继承意味着复制操作，然而 JavaScript 默认并不会复制对象的属性，相反，JavaScript 只是在两个对象之间创建一个关联，这样，一个对象就可以通过委托访问另一个对象的属性和函数，所以与其叫继承，**委托**的说法反而更准确些。

## 作用域与作用域链

[从作用域到作用域链，思维脑图+代码示例让知识点一目了然！系列（三）](https://yuguang.blog.csdn.net/article/details/106618708)

![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/作用域与作用链域.png)

### 作用域

- 变量的可用性范围

- JavaScript 采用是词法作用域(lexical scoping)，也就是静态作用域：

  - 函数的作用域在函数定义的时候就决定了

  与之对应的还有一个动态作用域：

  - 函数的作用域是在函数调用的时候才决定的；

- 实例分析

  ```js
  var value = 1;
  function foo() {
      console.log(value);
  }
  function bar() {
      var value = 2;
      foo();
  }
  bar();
  ```

  - 执行`bar`函数，函数内部形成了局部作用域；
  - 声明value变量，并赋值2
  - 执行`foo`函数，函数foo的作用域内没有`value`这个变量，它会向外查找
  - 根据词法作用域的规则，函数定义时，`foo`的外部作用域为全局作用域
  - 打印**结果是1**
  - 如果是动态作用域的话：结果**就是2**

- 全局作用域与局部作用域

  ```js
  var a = 100;
  function fn(){
  	a = 1000;
  	console.log('a1-',a);
  }
  console.log('a2-',a);
  fn();
  console.log('a3-',a);
  // a2- 100 // 在当前作用域下查找变量a => 100
  // a1- 1000 // 函数执行时，全局变量a已经被重新赋值
  // a3- 1000 // 全局变量a => 1000
  
  function fn(){
      var name="余光";
      function childFn(){
          console.log(name);
      }
      childFn(); // 余光
  }
  console.log(name); // name is not defined
  ```

### 作用域链

- 当查找变量的时候都发生了什么？
  - 会先从当前上下文的变量对象中查找；
  - 如果没有找到，就会从父级(词法层面上的父级)执行上下文的变量对象中查找；
  - 一直找到全局上下文的变量对象，也就是全局对象；
  - 作用域链的顶端就是全局对象；
  - 这样由多个执行上下文的变量对象构成的链表就叫做**作用域链**，从某种意义上很类似原型和原型链。

- 作用域链和原型继承查找时的区别：
  - 查找一个普通对象的属性，但是在当前对象和其原型中都找不到时，会返回undefined
  - 查找的属性在作用域链中不存在的话就会抛出ReferenceError。
- 作用域嵌套：既然每一个函数就可以形成一个作用域（词法作用域 || 块级作用域），那么当然也会存在多个作用域嵌套的情况，他们遵循这样的查询规则：
  - 内部作用域有权访问外部作用域
  - 外部作用域无法访问内部作用域;（真是是这样吗？）
  - 兄弟作用域不可互相访问

## 执行上下文

[JavaScript中的执行上下文，既然遇见了这篇图文并茂的文章，干脆看完吧！（系列四）](https://yuguang.blog.csdn.net/article/details/106668345)

### 定义与类型

- 定义
  - 当函数执行时，会创建一个称为执行上下文的内部对象。一个执行上下文定义了一个函数执行时的环境；
  - 当一个函数被调用时，会创建一个活动记录（有时候也称为执行上下文）。这个记录会包含函数在哪里被调用（调用栈）、函数的调用方式、传入的参数等信息 ；
  - 每个函数在被定义时，就会有一个[[scope]]属性，这个属性里保存着作用域链，而执行的前一刻都会创建一个OA对象，这个对象就是执行上下文，这个OA对象会被插入[[scope]]中作用域链的最顶端，这个对象里保存着函数体声明的所有变量、参数和方法。一个OA对象的有序列表。

- 执行上下文的类型
  - 全局执行上下文：只有一个，浏览器中的全局对象就是 window 对象，this 指向这个全局对象。
  - 函数执行上下文：存在无数个，只有在函数被调用的时候才会被创建，每次调用函数都会创建一个新的执行上下文。
  - Eval 函数执行上下文： 指的是运行在 eval 函数中的代码，很少用而且不建议使用。

### 执行栈

- 定义
  - 执行栈，也叫调用栈，具有 LIFO（后进先出）结构，用于存储在代码执行期间创建的所有执行上下文。
  - 首次运行JS代码时，会创建一个全局执行上下文并Push到当前的执行上下文栈中。每当发生函数调用，引擎都会为该函数创建一个新的函数执行上下文并push到当前执行栈的栈顶。
  - 当栈顶函数运行完成后，其对应的函数执行上下文将会从执行栈中pop出，上下文控制权将移到当前执行栈的下一个执行上下文。

## 变量对象VO

[JavaScript中的变量对象，简约却不简单（系列五）](https://yuguang.blog.csdn.net/article/details/106793254)

当 JavaScript 代码执行一段可执行代码(executable code)时，会创建对应的执行上下文(execution context)。

对于每个执行上下文，都有三个重要属性：变量对象(Variable object，VO)、作用域链(Scope chain)、this

### 变量对象

- 定义：在函数上下文中，我们用活动对象(activation object, AO)来表示变量对象，活动对象和变量对象其实是一个东西：
  - 变量对象是规范上的或者说是引擎实现上的，不可在 JavaScript 环境中访问
  - 只有到当进入一个执行上下文中，这个执行上下文的变量对象才会被激活，所以才叫 activation object，而只有被激活的变量对象，也就是活动对象上的各种属性才能被访问。
- 分类：
  - **全局变量对象**：全局对象是预定义的对象，作为 JavaScript 的全局函数和全局属性的占位符。通过使用全局对象，可以访问所有其他所有预定义的对象、函数和属性。
    - 可以通过 this 引用，在客户端 JavaScript 中，全局对象就是 Window 对象。
    - 全局对象是由 Object 构造函数实例化的一个对象。
    - 预定义了一堆，嗯，一大堆函数和属性。
    - 作为全局变量的宿主（很牛的样子）
    - 客户端 JavaScript 中，全局对象有 window 属性指向自身。
    - 全局上下文中的`变量对象`就是全局对象！
  - **函数上下文中的变量对象**：
    - 在函数执行上下文中，VO是不能直接访问的，此时由`活动对象`(activation object,缩写为AO)扮演`VO`的角色。
    - 活动对象是在进入函数上下文时刻被创建的，它通过函数的arguments属性初始化。arguments属性的值是Arguments对象
    - Arguments对象是活动对象的一个属性，它包括如下属性：
      - callee — 指向当前函数的引用
      - length — 真正传递的参数个数
      - properties-indexes (字符串类型的整数) 属性的值就是函数的参数值(按参数列表从左到右排列)。
      - properties-indexes内部元素的个数等于arguments.length. properties-indexes 的值和实际传递进来的参数之间是共享的。

- 执行过程
  - 进入执行上下文（分析）
    - 当进入执行上下文时，这时候还没有执行代码，变量对象会包括：
      - 函数的所有形参 (如果是函数上下文)
        - 由名称和对应值组成的一个变量对象的属性被创建
        - 没有实参，属性值设为 undefined
      - 函数声明
        - 由名称和对应值（函数对象(function-object)）组成一个变量对象的属性被创建
        - 如果变量对象已经存在相同名称的属性，则完全替换这个属性
      - 变量声明
        - 由名称和对应值（undefined）组成一个变量对象的属性被创建；
        - 如果变量名称跟已经声明的形式参数或函数相同，则变量声明不会干扰已经存在的这类属性
  - 代码执行
    - 在代码执行阶段，会顺序执行代码，根据代码，修改变量对象的值

- 总结：
  - 全局上下文的变量对象初始化是全局对象;
  - 函数上下文的变量对象初始化只包括 Arguments 对象;
  - 在进入执行上下文时会给变量对象添加形参、函数声明、变量声明等初始的属性值;
  - 在代码执行阶段，会再次修改变量对象的属性值;

- 比较迷的思考题

  ```js
  console.log(foo);
  
  function foo(){
      console.log("foo");
  }
  
  var foo = 1;
  ```

  - 会打印函数，而不是 undefined 。这是因为在进入执行上下文时，首先会处理函数声明，其次会处理变量声明，如果如果变量名称跟已经声明的形式参数或函数相同，则变量声明不会干扰已经存在的这类属性。

## 立即调用函数

[JavaScript之深入理解立即调用函数表达式（IIFE），你对它的理解，决定了它的出镜率（系列六）](https://yuguang.blog.csdn.net/article/details/106824296)

要点：

- `function` 这个关键字，既可以当做语句，也可以当做表达式，如果function出现在行首，一律解析成语句，可以使用（）括住，因为JavaScript里`括弧()`里面不能包含语句

场景：

- 隔离作用域：IIFE最常见的功能，就是隔离作用域，在ES6之前JS原生也没有块级作用域的概念，所以需要函数作用域来模拟。
- 惰性函数：DOM事件添加中，为了兼容现代浏览器和IE浏览器，我们需要对浏览器环境进行一次判断（？？？意义何在）

注意：

- 当函数变成立即执行的函数表达式时，表达式中的变量不能从外部访问。
- 将 IIFE 分配给一个变量，不是存储 IIFE 本身，而是存储 IIFE 执行后返回的结果。

## 闭包

[JavaScript之闭包，给自己的Js一场重生（系列七）](https://yuguang.blog.csdn.net/article/details/106940646)

定义：

- 闭包代码块创建该代码块的上下文中数据的结合
- 闭包就是能够读取其他函数内部变量的函数，在本质上是函数内部和函数外部链接的桥梁
- 不同的角度对闭包的解释不同的,**闭包是函数内部的返回的子函数**这句话本身没错，但要看从什么角度出发：
  - ECMAScript中，闭包指的是：
    - 从理论角度：所有的函数,因为它们都在创建的时候就将上层上下文的数据保存起来了。哪怕是简单的全局变量也是如此，因为函数中访问全局变量就相当于是在访问自由变量，这个时候使用最外层的作用域。
    - 从实践角度：以下函数才算是闭包：即使创建它的上下文已经销毁，它仍然存在（比如，内部函数从父函数中返回）
      在代码中引用了自由变量

解释：

```js
var scope = "global scope";
function checkscope(){
    var scope = "local scope";
    function f(){
        return scope;
    }
    return f;
}

var foo = checkscope();
foo(); // local scope
```

- 执行上下文栈和执行上下文的变化情况:

  - 进入全局代码，创建全局执行上下文，全局执行上下文压入执行上下文栈

  - 全局执行上下文初始化

  - 执行 checkscope 函数，创建 checkscope 函数执行上下文，checkscope 执行上下文被压入执行上下文栈

  - checkscope 执行上下文初始化，创建变量对象、作用域链、this等

  - checkscope 函数执行完毕，checkscope 执行上下文从执行上下文栈中弹出

  - 执行 f 函数，创建 f 函数执行上下文，f 执行上下文被压入执行上下文栈

  - f 执行上下文初始化，创建变量对象、作用域链、this等

  - f 函数执行完毕，f 函数上下文从执行上下文栈中弹出

![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/闭包举例.png)

-  f 执行上下文维护了一个作用域链：

  - f 函数依然可以读取到 `checkscopeContext.AO` 的值；

  - 当 f 函数引用了 checkscopeContext.AO 中的值的时候，即使 `checkscopeContext` 被销毁了，JavaScript 依然会让 `checkscopeContext.AO` 活在内存中;

  - f 函数依然可以通过 f 函数的作用域链找到它，正是因为 JavaScript 做到了这一点，从而实现了闭包这个概念。

注意：

- **同一个上下文创建的闭包是共用一个`[[scope]]`属性的**，某个闭包对其中`[[Scope]]`的变量做修改会影响到其他闭包对其变量的读取

- 思考

  ```js
  var arr = []
  for(var i = 0; i < 10; i++){
      arr[i] = function () {
          console.log(i)
      }
  }
  arr[0](); // 10
  arr[1](); // 10
  arr[2](); // 10
  arr[3](); // 10
  ```

  - **同一个上下文中创建的闭包是共用一个[[Scope]]属性**

  ```js
  var arr = []
  for(var i = 0; i < 10; i++){
      arr[i] = (function (i) {
          return function () {
              console.log(i);
          }
      })(i)
  }
  arr[0](); // 0
  arr[1](); // 1
  arr[2](); // 2
  arr[3](); // 3
  ```

  - 通过立即执行匿名函数的方式隔离了作用域，当执行 arr[0] 函数的时候，arr[0] 函数的作用域链发生了改变
  - 总结：
    - 函数内的所有内部函数都共享一个父作用域，因此创建的闭包是共用的。
    - 利用闭包隔离作用域的特性可以解决共享作用域的问题

## 参数传值与求值策略

[JavaScript中的参数传递(求值策略)，ECMAScript中所有函数的参数都是按值传递吗（系列八）](https://yuguang.blog.csdn.net/article/details/107111529)

### 值传递与引用传递

- 值传递
  - ECMAScript中所有函数的参数都是按值传递的
- 引用传递
  - 函数接收的不是值的拷贝，而是对象的隐式引用。

- （以下有疑问）
- 参数的值是调用者传递的对象值的拷贝(copy of value），函数内部改变参数的值不会影响到外面的对象（该参数在外面的值
- 按引用传递：函数内部对参数的任何改变都是影响该对象在函数外部的值，因为两者引用的是同一个对象，也就是说：这时候参数就相当于外部对象的一个别名。
- 共享传递不可能去解除引用和改变对象本身，但可以去修改该对象的属性值。

## JS基本数据类型

[JavaScript中的基本数据类型，地基同样重要（系列九）](https://yuguang.blog.csdn.net/article/details/107151991)

- 原始数据类型值 primitive type，比如`Undefined`,`Null`,`Boolean`,`Number`,`String`。

  - 存储在栈（stack）中的简单数据段
  - 它们的值**直接存储在变量访问的位置**。
  - 它可以直接存储，是因为这些原始类型占据的空间是固定的，所以可将他们存储在较小的内存区域 – `栈`中
  - 这样存储便于迅速查寻变量的值。
  - 基本类型的值是按值访问的，且基本类型的值是不可变的。

  ```js
  var str = "123hello321";
  str.toUpperCase();     // 123HELLO321
  console.log(str);      // 123hello321
  
  var a = 1;
  var b = true;
  console.log(a == b);    // == 只进行值的比较
  console.log(a === b);   // === 不仅进行值得比较，还要进行数据类型的比较
  ```

- 引用类型值，也就是对象类型 Object type,`比如Object`,`Array`,`Function`,`Date`等。

  - 存储在堆（heap）中的对象
  - 存储在变量处的值是一个指针（point），指向存储对象的内存地址。
  - 引用类型的值是按引用访问的，且引用类型的值是`可变`的。
  - 变量存储的是可以打开保存数据的房间的`钥匙`
  - `存储钥匙地址`的大小是固定的，所以把它存储在栈中对变量性能无任何负面影响。
  - 统称为 Object 类型。细分的话，有：Object、Array、Date、RegExp、Function
  - **引用类型的比较是引用的比较：**

  ```js
  var obj1 = {};    // 新建一个空对象 obj1
  var obj2 = {};    // 新建一个空对象 obj2
  console.log(obj1 == obj2);    // false
  console.log(obj1 === obj2);   // false
  ```

注意：

- JavaScript中的变量是没有类型的，`变量a`可以随时持有任何类型的`值`。换个角度来理解就是，JavaScript不做“类型强制”；也就是说，语言引擎不要求变量总是持有与其初始值同类型的值。
- typeof检测不总是对的

## 类型检测

[JavaScript专题（六）类型检测](https://yuguang.blog.csdn.net/article/details/108130316)

- typeof检测：

  - 注意：`typeof null => 'object'` 且 `typeof function(){} => 'function'`

    ![在这里插入图片描述](/Users/wangke/Desktop/收集/图片/typeof.png)

    ```js
    // 基本数学API和属性
    typeof Math.LN2 === 'number'; // true  Math的属性
    typeof Infinity === 'number'; // true 无穷
    typeof NaN === 'number'; // true 特殊的数字类型，not a number
    // 被强转称数字的其他数据类型
    typeof Number('str') === 'number'; // Number('str') => NaN => number
    
    typeof (typeof 1) === 'string'; // typeof always returns a string
    typeof String(1) === 'string'; // 强转成字符串
    
    typeof Boolean(1) === 'boolean'; // 强制类型转换
    typeof !!(1) === 'boolean'; // two calls of the ! (logical NOT) operator are equivalent to Boolean()
    
    typeof Symbol() === 'symbol'
    typeof Symbol('foo') === 'symbol'
    
    typeof undefined === 'undefined';
    typeof { name: '余光' } === 'object';
    typeof null === 'object'; // true,值得我们注意恰恰是这个null,typeof 对它的处理返回的是object
    //typeof检测函数返回的也是object，这是因为从规范上看function实际上是object的一个子类型。
    typeof function() {} === 'function';
    typeof class C {} === 'function';
    ```

  - null和undefined

    - null：特指对象的值未设置。它是 JavaScript 基本类型 之一。它不是全局对象的一个属性;在 API 中，null 常在返回类型应是一个对象，但没有关联的值的地方使用。

    - undefined：表示声明但未被赋值的变量类型，你可以使用undefined和严格相等或不相等操作符来决定一个变量是否拥有值。

    - 当检测 null 或 undefined 时，注意相等 `==`与`===`两个操作符的区别 ，前者会执行类型转换
      - typeof检测时两者的返回值不同
      - 代表的含义不同

    ```js
    typeof null        // "object" (因为一些以前的原因而不是'null')
    typeof undefined   // "undefined"
    null === undefined // false
    null  == undefined // true
    null === null // true
    null == null // true
    !null //true
    isNaN(1 + null) // false
    isNaN(1 + undefined) // true
    ```

- instanceof检测
  - instanceof 运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的原型链上。
- constructor检测
  - 有时候我们不希望匹配父类型，只希望匹配当前类型，那么我们可以用constructor来判断
-  Object.prototype.toString
  - toString无法区分原始类型及其构造对象
    - 我们认为Number、Boolean这种类型在被构造器构造出来后的类型应该是`对象`；
    - 但toString都会返回[object number]等原始类型；

## 类型转换

[JavaScript专题（七）类型转换](https://yuguang.blog.csdn.net/article/details/108751454)

- 显式类型转换

  - 显式类型转换主要是指通过 String、Number、Boolean 等构造方法转换相应的字符串、数字、布尔值

  ```js
  const str = String(1);
  const num = Number("123.3"); //number:123.3
  ```

  - 这是显式的情况——类型的转换的动作是由我们主动发起的。

-  隐式类型转换

  ```js
  const newStr1 = 1 + "str"; // '1str'
  const newStr2 = "hello" + [89, 150.156, "mike"]; // 'hello89,150.156,mike'
  ```

- 注意：

  - 所有对象(包括数组和函数)都转换为 `true`

  ```js
  console.log(Boolean(new Boolean(false))); // true
  ```

- toString

  - 所有的对象除了`null`和`undefined`之外的任何值都具有`toString`方法，通常情况下，它和使用`String`方法返回的结果一致。
  - `Object.prototype.toString` 方法会根据这个对象的[[class]]内部属性，返回由 "[object " 和 class 和 “]” 三个部分组成的字符串。
  - 数组：将每个数组元素转换成一个字符串，并在元素之间添加逗号后合并成结果字符串。
  - 函数：返回源代码字符串。

  ```js
  [1, 2, 3, 4].toString(); // "1,2,3,4"
  [].toString(); // ""
  function func() {
    console.log();
  }
  func.toString(); // "function func () { console.log() }"
  ```

- valueOf
  - valueOf 方法返回这个对象本身，数组、函数、正则简单的继承了这个默认方法，也会返回对象本身。日期是一个例外，它会返回它的一个内容表示: 1970 年 1 月 1 日以来的毫秒数。
- ToPrimitive//????没弄懂
  - String 方法转化一个值的时候：
    - 基本类型：参照 “原始值转字符” 的对应表
    - 引用类型：调用一个`ToPrimitive`方法，将其转为基本类型，然后再参照 “原始值转字符” 的对应表进行转换。
  - 这个返回原始值的方法接受一个输入参数 和一个可选的参数来表示转换类型：
    - input，表示要处理的输入值，如果传入的 input 是 Undefined、Null、Boolean、Number、String 类型，直接返回该值。
    - PreferredType，非必填，表示希望转换成的类型，有两个值可以选，Number 或者 String。当不传入 PreferredType 时，如果 input 是日期类型，相当于传入 String，否则，都相当于传入 Number。
  - 如果是 ToPrimitive(obj, Number)，处理步骤如下：
    1. 如果 obj 为 基本类型，直接返回
    2. 否则，调用 valueOf 方法，如果返回一个原始值，则 JavaScript 将其返回。
    3. 否则，调用 toString 方法，如果返回一个原始值，则 JavaScript 将其返回。
    4. 否则，JavaScript 抛出一个类型错误异常。
  - 如果是 ToPrimitive(obj, String)，处理步骤如下：
    1. 如果 obj 为 基本类型，直接返回
    2. 否则，调用 toString 方法，如果返回一个原始值，则 JavaScript 将其返回。
    3. 否则，调用 valueOf 方法，如果返回一个原始值，则 JavaScript 将其返回。
    4. 否则，JavaScript 抛出一个类型错误异常。
- 

## 变量提升与预编译

[JavaScript专题（一）变量提升与预编译，一起去发现Js华丽的暗箱操作](https://yuguang.blog.csdn.net/article/details/107390368)

### JS预编译

引擎会在解释JavaScript代码之前首先对其进行编译。编译阶段中的一部分工作就是找到所有的声明，并用合适的作用域将它们关联起来

### 变量提升

- **只有声明会被提升，而赋值和其他代码逻辑会在执行到代码的位置时才会生效**
- 每个作用域都会进行提升操作
- 函数会被首先提升，然后才是变量
- 函数字面量不会进行函数提升
- let和const声明的变量不会进行变量提升
  - let命令改变了语法行为，它所声明的变量一定要在声明后使用，否则报错。

```js
foo();
var foo; // 1
function foo(){
    console.log('余光');
}
foo = function(){
    console.log('小李');
}

//解析成以下

function foo(){
    console.log('余光');
}
foo(); // 余光
foo = function(){
    console.log('小李');
}
```

`var foo` 因为是一个重复声明，且优先级`低于函数声明`所以它被忽略掉了。

```js
foo();
var foo = function(){
    console.log(1);
}
// TypeError: foo is not a function
```

这段程序中：

- 变量标识符foo被提升并分配给所在作用域（在这里是全局作用域），因此在执行foo()时不会导致ReferenceError（），而是会提示你 foo is not a function。
- 然后就是执行foo，foo此时并没有赋值（注意变量被提升了）。由于对undefined值进行函数调用而导致非法操作，因此抛出TypeError异常。

总结：

- 变量提升：函数声明和变量声明总是会被解释器悄悄地被"提升"到方法体的最顶部，但变量的初始化不会提升；
- 函数提升：函数声明可以被看作是函数的整体被提升到了代码的顶部，但函数字面量表达式并不会引发函数提升；
- 函数提升优先与变量提升；
- let和const可以有效的规避变量提升

## 数组去重的方法

[JavaScript专题（二）数组去重，会就要会的理直气壮](https://yuguang.blog.csdn.net/article/details/107544166)

- 双层循环
  - 利用splice并修正下标
  - 利用push到新数组并检查
- indexOf includes 只需一层循环
  - 识别NaN时只能用includes
  - includes会认为空的值是undefined而includes不会

- sort排序+push到新数组
- filter
- 键值对
  - 两种方法
    - 统计每个元素出现的次数，obj：{1: 3, 2: 2, 3: 3}, 返回这个`obj`的`key`而不管他们的`value`
    - 只元素首次出现，再次出现则证明他是重复元素（结合filter）
  - 问题
    - 对象的属性是字符串类型的，即本身`数字1`和`字符串‘1’`是不同的，但保存到对象中时会发生隐式类型转换，导致去重存在一定的隐患。
    - 考虑到string和number的区别（typeof 1 === ‘number’， typeof ‘1’ === ‘string’），所以我们可以使用 `typeof item + item` 拼成字符串作为 key 值来避免这个问题：

- ES6

  - set   注意转换：[...new Set(array)]或 Array.from(new Set(arr))

  - map对象 

  - Map 对象保存键值对，并且能够记住键的原始插入顺序。任何值(对象或者原始值) 都可以作为一个键或一个值。

    - Map.prototype.has(key)：返回一个布尔值，表示Map实例是否包含键对应的值。
    - Map.prototype.set(key, value)：设置Map对象中键的值。返回该Map对象。

    ```js
    function unique (arr) {
        const newMap = new Map()
        return arr.filter((a) => !newMap.has(a) && newMap.set(a, 1));
    }
    ```

## 防抖

[JavaScript专题（三）防抖](https://yuguang.blog.csdn.net/article/details/107642581)

//仅作初略了解

目的：**降低一个函数的触发频率，以提高性能或避免资源浪费**

原理：事件触发`n秒无操作后`才执行

## 节流

[JavaScript专题（四）节流](https://yuguang.blog.csdn.net/article/details/107796115)

核心：**如果你持续触发某个事件，特定的时间间隔内，只执行一次**

两种实现方式：

- 时间戳
  - 我们取出当前的时间戳 `now`；
  - 然后减去之前**执行时**的时间戳(首次值为 0 ) `prev`；
  - 如果大`now - prev > wait`，证明时间区间维护结束，执行指定事件，更新`prev`；
- 定时器
  - 创建定时器`timer`，记录当前是否在**周期**内；
  - 判断定时器是否存在，若存在则直接结束，否则执行事件；
  - `wait`时间之后再次执行，并清掉定时器；

## 深浅拷贝

[JavaScript专题（五）深浅拷贝](https://yuguang.blog.csdn.net/article/details/107964274)

浅拷贝：

- slice() concat()对引用类型都是浅拷贝
- Object.assign()拷贝的是（可枚举）属性值，假如源值是一个对象的引用，它仅仅会复制其引用值

深拷贝：

- JSON实现
  - 步骤：
    - 定义一个包含都过类型的数组`arr`
    - JSON.stringify(arr), 将一个 JavaScript 对象或值转换为 `JSON 字符串`
    - JSON.parse(xxx), 方法用来解析JSON字符串，构造由字符串描述的`值或对象`
  - 我们可以理解为，将原始数据转换为`新字符串`，再通过`新字符串`还原为一个`新对象`，这中改变数据类型的方式，间接的绕过了拷贝对象引用的过程，也就谈不上影响原始数据。
  - 限制：这种方式成立的根本就是保证数据在“中转”时的完整性，而JSON.stringify()将值转换为相应的JSON格式时也有缺陷
    - undefined、任意的函数以及 symbol 值，在序列化过程中会被忽略（出现在非数组对象的属性值中时）或者被转换成 null（出现在数组中时）。
    - 函数、undefined 被单独转换时，会返回 undefined，如JSON.stringify(function(){})和JSON.stringify(undefined)
    - 对包含循环引用的对象（对象之间相互引用，形成无限循环）执行此方法，会抛出错误。
    - NaN 和 Infinity 格式的数值及 null 都会被当做 null。
    - 其他类型的对象，包括 Map/Set/WeakMap/WeakSet，仅会序列化可枚举的属性。

- deepCopy实现

```js
var deepCopy = function(obj) {
    if (typeof obj !== 'object') return;
    var newObj = obj instanceof Array ? [] : {};
    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            newObj[key] = typeof obj[key] === 'object' ? deepCopy(obj[key]) : obj[key];
        }
    }
    return newObj;
}
```

## ES6

### let

[ES6基础：let和const](https://yuguang.blog.csdn.net/article/details/108240559)

- let拒绝提升

- 经典的问题的for循环问题

  ```js
  const arr = [];
  for (var i = 0; i < 10; i++) {
      arr[i] = () => { console.log(i) }
  }
  arr[0](); // 10
  arr[1](); // 10
  arr[2](); // 10
  ```

  - 变量i是var命令声明的，在全局范围内都有效，所以全局只有一个变量i。每一次循环，变量i的值都会发生改变，而循环内被赋给数组a的函数内部的console.log(i)，里面的i指向的就是全局的i。也就是说，所有数组a的成员里面的i，指向的都是同一个i，导致运行时输出的是最后一轮的i的值，也就是 10。
  - 改为let声明：`变量i`是`let`声明的，当前的i只在本轮循环有效，所以每一次循环的i其实都是一个新的变量，虽然输出的变量都叫`i`，但他们已经存在于不同的作用域之中了。

-  let不能在同一个代码块中重复声明

- let 声明的变量存在“暂时性死区”

  ```js
  if (true) {
    // TDZ开始
    tmp = 'abc'; // ReferenceError
    console.log(tmp); // ReferenceError
    let tmp; // TDZ结束
    console.log(tmp); // undefined
    tmp = 123;
    console.log(tmp); // 123
  }
  ```

### Const

- const绝大部分特点和let一样，但是它声明是一个只读的常量。一旦声明，常量的值就不能改变。
- const 不存在变量提升
- const 不允许重复声明
- const 声明的变量存在“暂时性死区”
- const 声明的变量的存储地址不可写
- 对于复合类型的数据（主要是对象和数组），变量指向的内存地址，保存的只是一个指向实际数据的指针，const只能保证这个指针是固定的（即总是指向另一个固定的地址），至于它指向的数据结构是不是可变的，就完全不能控制了。因此，将一个对象声明为常量必须非常小心。

### 块级作用域

- ES6的块级作用域——**有大括号（ {}或() ）**，如果没有大括号，JavaScript 引擎就认为不存在块级作用域。
- 用var的风险
  - 内层变量可能会覆盖外层变量。
  - 第二种场景，用来计数的循环变量泄露为全局变量。

### 变量解构赋值

[ES6基础：变量的解构赋值](https://yuguang.blog.csdn.net/article/details/108327427)

数组解构赋值的作用：

- 同时赋值多个变量

- 解构嵌套数组

- 相同“模式”的不完全解构

  ```js
  let [a, b, c] = [1, 2, 3, 4]; // 1 2 3
  let [a, b, c, d] = [1, 2, 3]; // 1 2 3 undefined
  let [a, [b, c, [d, e]]] = [1, [2, 3, [4, 5, 6]]]; // 1 2 3 4 5
  
  //可以赋默认值
  let [a = true] = [];
  a // true
  
  //注意，ES6 内部使用严格相等运算符（===），判断一个位置是否有值。所以，只有当一个数组成员严格等于undefined，默认值才会生效。
  let [x = 1] = [undefined];
  x // 1
  let [x = 1] = [null];
  x // null
  ```

  - 注意：
    - 数组的解构是根据它的位置（模式）对应的
    - 解构操作允许有默认值，但一定是已经声明的。
    - 如果等号的右边不是数组（或者严格地说，不是可遍历的结构）那么将会报错

对象的解构赋值：

- 根据属性解构对象，对象的解构与数组有一个重要的不同。数组的元素是按次序排列的，变量的取值由它的位置决定；而对象的属性没有次序，变量必须与属性同名，才能取到正确的值。
- 如果属性不一样必须写成这样：

```js
let { foo: baz } = { foo: 'aaa', bar: 'bbb' };
baz // "aaa"

let obj = { first: 'hello', last: 'world' };
let { first: f, last: l } = obj; // 起了个别名
f // 'hello'
l // 'world'
```

函数参数的解构赋值：

- 解构对象类型参数

  ```js
  function fetch(option){
      var name = option.name;
      var age = option.age;
      var like = option.like;
  }
  
  // ES6
  function fetch({ name, age, like }) {
      // 参数经历了 let { name, age, like } = option
  }
  ```

- 解构数组类型参数

  ```js
  const arr = [
      [1, 1],
      [2, 2],
      [3, 3],
      [4, 4]
  ];
  const newArr = arr.map(([x, y]) => x + y);
  newArr // [ 2, 4, 6, 8 ]
  ```

- 为参数设定默认值,可以避免许多拿不到数据的情况

  ```js
  function func({ name = '余光', age = 23, like = 'FE' }) {
      console.log(name, age, like);
  }
  const options = { name: '余光' }
  func(options);
  ```

### 箭头函数

[ES6基础：箭头函数](https://yuguang.blog.csdn.net/article/details/109535841)

箭头函数和普通函数的区别：

- 没有this
  - 箭头函数没有 this，所以需要通过查找作用域链来确定 this 的值。
  - 箭头函数中的 this，就绑定在它最近一层非箭头函数的 this.
  - 一句话理解：箭头函数内部的 this 是词法作用域，由上下文确定。

- 没有 arguments
  - 箭头函数没有自己的 `arguments` 对象，这不一定是件坏事，因为箭头函数可以访问外围函数的 arguments 对象

- 不能通过 new 关键字调用
  - 箭头函数并没有 `[[Construct]]` 方法，不能被用作构造函数，如果通过 new 的方式调用，会报错

### Iterator 和 for...of

[ES6基础：Iterator和for...of](https://yuguang.blog.csdn.net/article/details/109780419)

- 迭代器
  - 通过 Symbol.iterator 创建一个迭代器，指向当前数据结构的起始位置
  - 随后通过 next 方法进行向下迭代指向下一个位置：
    - next 方法会返回当前位置的对象，对象包含了 value 和 done 两个属性;
    - value 是当前属性的值;
    - done 用于判断是否遍历结束，done 为 true 时则遍历结束;
  - `Iterator` 接口的目的，就是为所有数据结构，提供了一种统一的访问机制。当使用 for…of 循环遍历某种数据结构时，该循环会自动去寻找 Iterator 接口
  - 原生具备 Iterator 接口的数据结构有:Array，Map，Set，String，TypedArray，函数的 arguments 对象，NodeList 对象

- for...of

  - for…of 语句在可迭代对象上创建一个迭代循环，调用自定义迭代钩子，并为每个不同属性的值执行语句——MDN
  - 一个数据结构只要部署了`Symbol.iterator`属性，就被视为具有 `iterator` 接口，就可以用`for...of`循环遍历它的成员。
  -  `for...of`循环内部调用的是数据结构的`Symbol.iterator`方法

  ```js
  var arr = ["a", "b", "c", "d"];
  //for…in 循环读取键名
  for (let a in arr) {
    console.log(a); // 0 1 2 3
  }
  //for…of 循环读取键值
  for (let a of arr) {
    console.log(a); // a b c d
  }
  ```

### Generator

### rest参数

### 模板字符串

```js
//多行字符串
let multiStr = `
    <div class="box">
        <div class="hd">
            <h2>模块标题</h2>
        </div>
        <div class="bd">
            <!--模板内容-->
        </div>
    </div>
`;

//嵌入变量
for(var i = 6; i < 10; i++){
    var strHtml = `<li>${i}个元素</li>`;
    $(".list").append(strHtml);

```

- 格式：` 
- 可以作普通的字符串来使用
- 会保存格式，可以通过使用trim()方法将格式清除.
- 可以嵌入变量，可以嵌入任意合法的js表达式,可以进行算术运算以及对对象属性的引用

### 类

```js
class Thermostat{
  constructor(Fahrenheit ){
    this._Fahrenheit  = Fahrenheit ;
  }
  //getter
  get temperature(){
    return 5/9 * (this._Fahrenheit  - 32);
  }
  // setter
  set temperature(Celsius){
    this._Fahrenheit  = Celsius * 9.0 / 5 + 32;
  }
}
const thermos = new Thermostat(76); // Setting in Fahrenheit scale
let temp = thermos.temperature; // 24.44 in Celsius
thermos.temperature = 26;
temp = thermos.temperature; // 26 in Celsius
```

### 模块化管理

```js
//export共享代码
ES5:
export const add = (x, y) => {
  return x + y;
}
ES6:
const add = (x, y) => {
  return x + y;
}
export { add, subtract };

//import复用代码
import { add, subtract } from './math_functions.js';
//或者：
import * as myMathModule from "./math_functions.js";
myMathModule.add(2,3);
myMathModule.subtract(5,3);

//export default
export default function add(x, y) {
  return x + y;
}
export default function(x, y) {
  return x + y;
}
//default只能有一个，两种方式都可以
import add from "./math_functions.js";
//add具体取什么名字是无所谓的
```

### Promise

```js
const makeServerRequest = new Promise((resolve, reject) => {
  let responseFromServer = false;
  if(responseFromServer) {
    resolve("We got the data");
  } else {  
    reject("Data not received");
  }
});

makeServerRequest.then(result => {
  console.log(result);
});

makeServerRequest.catch(error => {
  console.log(error)
})
```

### es7 Async await

[async和await的讲解](https://blog.csdn.net/xgangzai/article/details/81269989?ops_request_misc=&request_id=&biz_id=102&utm_term=async%20await&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-81269989.pc_search_result_control_group&spm=1018.2226.3001.4187)

- **函数执行的时候，一旦遇到await就会先返回，等到异步操作结束，再接着执行函数体内后面的语句。**
- **await +（promise命令/原始类型的值），而async 函数返回一个promise对象 可以作为await命令的参数**
- 
