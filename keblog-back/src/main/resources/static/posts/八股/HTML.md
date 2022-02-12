# HTML

### 常见的状态码有哪些

- 200——表明该请求被成功地完成，所请求的资源发送回客户端
- 302——重定向，服务器要求浏览器重新发送一个请求
- 304——自从上次请求后，请求的网页未修改过，请客户端使用本地缓存
- 400——客户端请求有错（譬如可以是安全模块拦截）
- 401——请求未经授权
- 403——禁止访问（譬如可以是未登录时禁止）
- 404——资源未找到
- 500——服务器内部错误
- 503——服务不可用

### HTTP缓存策略

强制缓存优先于协商缓存进行，若强制缓存(Expires和Cache-Control)生效则直接使用缓存，若不生效则进行协商缓存(Last-Modified / If-Modified-Since和Etag / If-None-Match)，协商缓存由服务器决定是否使用缓存，若协商缓存失效，那么代表该请求的缓存失效，重新获取请求结果，再存入浏览器缓存中；生效则返回304，继续使用缓存，主要过程如下：
<img src="https://img-blog.csdnimg.cn/20210328152529389.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzM5OTAzNTY3,size_16,color_FFFFFF,t_70" alt="在这里插入图片描述"  />

> - 强缓存（200 from cache）时，浏览器如果判断本地缓存未过期，就直接使用，无需发起http请求
> - 协商缓存（304）时，浏览器会向服务端发起http请求，然后服务端告诉浏览器文件未改变，让浏览器使用本地缓存

### Connection为keep_alive

[前端网络与安全之connection为keep-alive是什么意思？](https://blog.csdn.net/leelxp/article/details/108096660?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522164238901416780271595514%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=164238901416780271595514&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-2-108096660.pc_search_result_cache&utm_term=connection+%E4%B8%BA+keep_alive&spm=1018.2226.3001.4187)

- keep-alive 是客户端和服务端的一个约定，如果开启 keep-alive，则服务端在返回 response 后不关闭 TCP 连接；同样的，在接收完响应报文后，客户端也不关闭连接，发送下一个 HTTP 请求时会重用该连接。
- keep-alive 技术创建的目的，就是能在多次 HTTP 之间重用同一个 TCP 连接，从而减少创建/关闭多个 TCP 连接的开销

## HTML5

特性：

- 语义化，web内容有序规范，便于阅读，爬虫解析，维护
- 网络标准统一，减少不需要的插件，跨平台
- webSocket，WebStorage，webworker独立线程

### webStorage

Web Storage的目的是为了克服由cookie带来的一些限制，当数据需要被严格控制在客户端上时，无须持续地将数据发回服务器。Web Storage的两个主要目标是：

- 提供一种在cookie之外存储会话数据的途径。
- 提供一种存储大量可以跨会话存在的数据的机制。

包括：

- SessionStorage：同源同窗口，浏览器没关闭一直存在
- localStorage：永久存储

### websocket

- 来源：
  - HTTP 无状态协议 request->response 每次都要带鉴别信息
  - websocket 持久化协议 一次握手
- 特点：
  - 事件驱动：建立连接后，允许服务端主动向客户端发东西
  - 异步
  - 使用ws或wss协议的客户端socket
  - 推送

### webWorker

- 为单线程的js创造多线程环境
- 后台、解决计算密集型和高延迟任务，结果返回主线程