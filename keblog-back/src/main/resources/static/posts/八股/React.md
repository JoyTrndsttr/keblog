## 前言

### [也许，DOM 不是答案](https://www.ruanyifeng.com/blog/2015/02/future-of-dom.html)

#### Web App vs. Native App

比起手机App，网站有一些明显的优点。

> - 跨平台：所有系统都能运行
> - 免安装：打开浏览器，就能使用
> - 快速部署：升级只需在服务器更新代码
> - 超链接：可以与其他网站互连，可以被搜索引擎检索

但是，现实是怎样呢？

**（1）体验差。**手机App的操作流畅性，远超网站。

**（2）业界不支持。**所有公司的移动端开发重点，几乎都是原生app。

**（3）用户不在乎。**大多数用户都选择使用手机app，而不是网站。

如果将来有一天，Web app会成为主流，一定有一个前提，那就是它的性能可以赶上Native app。

#### Web app的性能瓶颈

**（1）Web基于DOM，而DOM很慢。**浏览器打开网页时，需要解析文档，在内存中生成DOM结构，如果遇到复杂的文档，这个过程是很慢的。可以想象一下，如果网页上有上万个、甚至几十万个形状（不管是图片或CSS），生成DOM需要多久？更不要提与其中某一个形状互动了。

**（2）DOM拖慢JavaScript。**所有的DOM操作都是同步的，会堵塞浏览器。JavaScript操作DOM时，必须等前一个操作结束，才能执行后一个操作。只要一个操作有卡顿，整个网页就会短暂失去响应。浏览器重绘网页的频率是60FPS（即16毫秒/帧），JavaScript做不到在16毫秒内完成DOM操作，因此产生了跳帧。用户体验上的不流畅、不连贯就源于此。

**（3）网页是单线程的。**现在的浏览器对于每个网页，只用一个线程处理。所有工作都在这一个线程上完成，包括布局、渲染、JavaScript执行、图像解码等等，怎么可能不慢？

**（4）网页没有硬件加速。**网页都是由CPU处理的，没用GPU进行图形加速。

#### FlipBoard的解决方案

**---- 他们没有使用DOM，而是将整个网站用canvas输出！**

你可以用手机打开[flipboard.com](https://flipboard.com/)，体验一下，看看跟Native app有没有差别。如果你没有帐号，可以直接打开[这里](https://flipboard.com/@flipboard/flipboard-picks-8a1uu7ngz)或[这里](https://flipboard.com/@flipboard/ten-for-today-k6ln1khuz)。

这个方案的出发点是这样的：如果将网页变成了一个个canvas，用户就等于在跟图片互动，这样就绕开了DOM，降低了操作时滞。而且，canvas可以被硬件加速，这样就提高了性能。具体的技术细节，可以参考[原文](http://engineering.flipboard.com/2015/02/mobile-web/)。canvas的转化基于React框架实现，FlipBoard 开发了一个专门的库[React-canvas](https://github.com/flipboard/react-canvas)，已经开源。

这个方案引发了很多争议（[这里](http://rachelnabors.com/2015/02/15/accessibility-vs-ux/)和[这里](http://christianheilmann.com/2015/02/15/flipboard-and-the-mobile-web-dream/)），主要是canvas只是一个位图，本身没有语义，如果要在它上面实现UI，等于HTML语言已有的东西都要再发明一遍，比如如何实现超链接、如何实现CSS效果等等。一些最简单的东西都变得很麻烦，因为canvas不是自适应的（responsive），文字在哪里断行，都要自己计算，而且用户也无法选中文本。另外，怎么让搜索引擎检索网页，解决起来也不是很容易。

#### 未来的路

**（1）多线程浏览器。**每个网页应该由多个线程进行处理，主线程只负责布局和渲染，而且应该在16毫秒内完成，JavaScript由worker线程执行，这样就不会发生堵塞了。Mozilla正在开发的[Servo](https://github.com/servo/servo)就是这样一个项目。

**（2）DOM的异步操作。**JavaScript对DOM的操作不再是同步的，而是触发后，交给Event Loop机制进行监听。

**（3）非DOM方案。**浏览器不再将网页处理成DOM结构，而是变为其他结构。React的[Virtual DOM](https://stackoverflow.com/questions/21109361/why-is-reacts-concept-of-virtual-dom-said-to-be-more-performant-than-dirty-mode)方案就是这一类的尝试，还有更激进的方案，比如用数据库取代DOM。

## 基本语法

### HTML Template

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <script src="../build/react.development.js"></script>
    <script src="../build/react-dom.development.js"></script>
    <script src="../build/babel.min.js"></script>
  </head>
  <body>
    <div id="example"></div>
    <script type="text/babel">

      // ** Our code goes here! **

    </script>
  </body>
</html>
```

### Render JSX

```js
ReactDOM.render(
  <h1>Hello, world!</h1>,
  document.getElementById('example')
);
```

### Use JavaScript in JSX

```js
var names = ['Alice', 'Emily', 'Kate'];

ReactDOM.render(
  <div>
  {
    names.map(function (name) {
      return <div>Hello, {name}!</div>
    })
  }
  </div>,
  document.getElementById('example')
);
```

上面代码体现了 JSX 的基本语法规则：

- 遇到 HTML 标签（以 `<` 开头），就用 HTML 规则解析
- 遇到代码块（以 `{` 开头），就用 JavaScript 规则解析。上面代码的运行结果如下

### Use array in JSX

```js
var arr = [
  <h1>Hello world!</h1>,
  <h2>React is awesome</h2>,
];
ReactDOM.render(
  <div>{arr}</div>,
  document.getElementById('example')
);
```

### Define a component

```js
class HelloMessage extends React.Component {
  render() {
    return <h1>Hello {this.props.name}</h1>;
  }
}

ReactDOM.render(
  <HelloMessage name="John" />,
  document.getElementById('example')
);
```

注意

- 在16.0版本之前使用的是 `React.createClass()` ，现在已被deprecated
- componet可以带参数，you can use `this.props.[attribute]` to access them, just like `this.props.name` of `<HelloMessage name="John" />` is John.
- 组件名首字母必须要大写
- React component should only have one top child node.

```js
// wrong
class HelloMessage extends React.Component {
  render() {
    return <h1>
      Hello {this.props.name}
    </h1><p>
      some text
    </p>;
  }
}

// correct
class HelloMessage extends React.Component {
  render() {
    return <div>
      <h1>Hello {this.props.name}</h1>
      <p>some text</p>
    </div>;
  }
}
```

