# webTimer
### 使用方法：
  
打开chrome的插件页面：chrome://extensions/

或者通过点击更多右上角菜单，进入工具->扩展程序，进入这个页面，

然后将chrome_extension.crx拖到这个页面即可使用。

现在插件保存每天的汇总数据，也就是能查看今天总共访问了那些域名及访问时间。

将实现年月日数据查询、汇总和分析功能，敬请期待:)

### 想法初衷：
最初想知道每天网站访问情况，所以想自己写了个，最开始实现是通过抓本机的tcp包，无奈规则很难指定，所以直接通过浏览器插件的形式来实现的，具体实现下面有说明。

### 插件工作流程：
chrome插件采集数据，每5分钟将采集的数据上传至服务端（现在服务端正在实现中），采集数据结构见sql文件。
    
### chrome插件：
数据采集参照的别人的实现方法[参考地址](https://github.com/dskang/webtimer)


### 效果图

当天访问记录效果图：

![image](https://github.com/EchoUtopia/webTimer/blob/master/chrome_extension/screen_2.png)


当前5分钟访问记录效果图：

![image](https://github.com/EchoUtopia/webTimer/blob/master/chrome_extension/screen_1.png)


    
