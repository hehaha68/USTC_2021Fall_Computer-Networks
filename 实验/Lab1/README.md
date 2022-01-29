#### 实验简介
example.txt 是一个配置文件示例，DNS Relay Server 根据配置文件来决定如何响应请求。
1. 当请求的域名不在配置文件中时，将请求转发给一个正常的DNS Server ，然后将收到的response回复客户端。
2. 当请求的域名在配置文件中有对应的非0.0.0.0 ip地址，将该ip地址返回给客户端
3. 当请求的域名在配置文件中对应ip地址为0.0.0.0 ，将DNS response 报文中Rcode置为3表示域名不存在，然后将地址返回给客户端。

#### 配置文件
example.txt 文件中

    0.0.0.0 pic1.zhimg.com
    0.0.0.0 pic2.zhimg.com
    0.0.0.0 pic3.zhimg.com
    0.0.0.0 pic4.zhimg.com
    0.0.0.0 static.zhimg.com
    0.0.0.0 picb.zhiming.com
上述条目 *.zhiming.com 网址对应的ip全部为0.0.0.0，是为了拦截知乎首页(www.zhihu.com) 广告的设置

    182.61.200.7 www.baidu.com
    127.0.0.1 www.test1.com  

182.61.200.7 是通过命令 nslookup www.baidu.com 返回的ip地址。示意你可以对指定的域名返回错误的ip地址，进行dns污染，将客户端重定向到另一个你想要用户访问的网站。按照上述配置当你浏览器访问www.test1.com 的时候会访问到我们自定义的一个网站主页(一个简单的html)