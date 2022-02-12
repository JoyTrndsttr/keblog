## 项目构建过程

- 在github上建立一个repository
- clone 
- 建立vue项目
- 配置git环境
- 安装使用Element组件 [Element](https://element.eleme.cn/#/zh-CN/component/quickstart)
  - `npm i element-ui -S`
  - babelrc设置按需引用
  - 安装其他babel组件
    - `cnpm install babel-plugin-component -D `
    - `cnpm install babel-preset-es2015 --save-dev`

## 路由

[Vue Router详细教程](https://blog.csdn.net/JDream111/article/details/107725322?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164224509316780366574152%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=164224509316780366574152&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-107725322.pc_search_result_control_group&utm_term=vue+router&spm=1018.2226.3001.4187)

**作用**：

vue-router是基于路由和组件的路由用于设定访问路径，将路径和组件映射起来。在vue-router的单页面应用中, 页面的路径的改变就是组件的切换。

**安装和使用**：

- 使用webpack，`npm install vue-router --save`

- 在模块化工程中使用它(因为是一个插件, 所以可以通过Vue。use()来安装路由功能)

  - 第一步：导入路由对象，并且调用 Vue.use(VueRouter)

  - 第二步：创建路由实例，并且传入路由映射配置

    <img src="/Users/wangke/Library/Application Support/typora-user-images/image-20220115194205104.png" alt="image-20220115194205104" style="zoom:50%;" />

  - 第三步：在Vue实例中挂载创建的路由实例

    <img src="/Users/wangke/Library/Application Support/typora-user-images/image-20220115194258749.png" alt="image-20220115194258749" style="zoom:50%;" />

- **使用vue-router:**

  - 第一步: 创建路由组件

    <img src="/Users/wangke/Library/Application Support/typora-user-images/image-20220115194546476.png" alt="image-20220115194546476" style="zoom:50%;" />

  - 第二步: 配置路由映射: 组件和路径映射关系

  - 第三步: 使用路由

    <img src="/Users/wangke/Library/Application Support/typora-user-images/image-20220115194834228.png" alt="image-20220115194834228" style="zoom:50%;" />

## 安装一个模块（showdown）

[vue使用markdown编辑器和把md渲染成html](https://blog.csdn.net/weixin_44823731/article/details/105266066?ops_request_misc=&request_id=&biz_id=102&utm_term=vue%20markdown%E6%8F%92%E4%BB%B6&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-9-105266066.pc_search_result_control_group&spm=1018.2226.3001.4187)

步骤：

- `cnpm install showdown --save`  安装完后可以在node-modules中看到showdown
- main.js中全局配置

<img src="/Users/wangke/Library/Application Support/typora-user-images/image-20220116171558274.png" alt="image-20220116171558274" style="zoom:50%;" />

- 使用`var htmlContent = this.converter.makeHtml(mdContent)`

扩展：

### --save的作用

[npm install、npm install --save与npm install --save-dev区别](https://blog.csdn.net/qq_30378229/article/details/78463930?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-1.pc_relevant_default&utm_relevant_index=2)

**npm install X:**

- 会把X包安装到node_modules目录中
- 不会修改package.json
- 之后运行npm install命令时，不会自动安装X

**npm install X –-save:**

- 会把X包安装到node_modules目录中
- 会在[package](https://so.csdn.net/so/search?q=package&spm=1001.2101.3001.7020).json的dependencies属性下添加X
- 之后运行npm install命令时，会自动安装X到node_modules目录中
- 之后运行npm install
  –production或者注明NODE_ENV变量值为production时，会自动安装msbuild到node_modules目录中

**npm install X –-save-dev:**

- 会把X包安装到node_modules目录中
- 会在package.json的devDependencies属性下添加X
- 之后运行npm install命令时，会自动安装X到node_modules目录中
- 之后运行npm install
  –production或者注明NODE_ENV变量值为production时，不会自动安装X到node_modules目录中

**使用原则:**

运行时需要用到的包使用–save，否则使用–save-dev。

## 使用Vuex

安装：`cnpm install vuex@next --save`(Vue2.x安装vuex3.x)



