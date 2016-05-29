# lagou-job-report  
  
**从拉勾招聘小窥互联网行业发展。**
  
[点此查看结果报告](http://peggyzwy.github.io/lagou-job-report/)  
  
## 程序说明  
1. 运行lagouSpider.py后会得到一个数据库：test.db。这一步爬虫爬了1.5小时
2. 看看数据库，发现salary一列的内容各种各样，之后用ECharts作图要用到工资数据，我的目标是把工资归为salary_list = ['0-5k', '6-10k', '11-15k', '16-20k', '21-25k', '26-30k', '30k+']中的一个。为了追求尽可能大的准确性，我是人工判断整理的，如果不要那么精确，可以写个辅助程序。这一步在表lagou里添加了一列cleanedSalary  
3. 2步完成后，运行analyse.py。保证test.db和此程序在同一目录就好了。运行中，会在表lagou里新建一列developmentStage，还会新建一个表totalcount。最后Python会把查询结果转成JSON格式写入results_dict.js，在下一步中会被引入HTML中当做JS的全局变量，然后才可以给ECharts配置数据。因为是本地文件，没有用Ajax，所以写入的时候给它附了变量名，便于在HTML中引用，所以是js文件而不是存的json
4. index.html会引入ECharts的JS以及上面这个results_dict.js，动态插入数据，就可以在网页上看到可视化的数据了  

  
## 总结  
### SQLite  
1. SQLite数据库使用的是UTF-8编码方式，而传入的字符串若是ASCII编码或Unicode编码，会导致字符串格式错误。解决方案是在调用SQLite接口之前，先将字符串转换成UTF-8编码。以及text_factory属性，参考[Python sqlite3模块的text_factory属性的使用方法研究](http://www.bubuko.com/infodetail-806298.html) 。  
2. 如果字段选定了TEXT，就不能直接放数组进去，要先把数组变成字符串  
3. 在SQLite中新增一列：`ALTER TABLE table-name ADD COLUMN column-name column-type`  
4. SQLite不支持删除列的操作（好坑啊。。。）。  
   一种替代方法是：1）根据原表创建一张新表；2）删除原表；3）将新表重名为旧表的名称  

     
### Python及爬虫 
1. 在用request模块设置proxy时，开始忘了加端口，然后出现了UNKNOWN HOST的错误
2. 为了防止爬虫假死，建议在requests参数里设置timeout  
3. 在爬虫连接网络时，可能出现多种错误。一种ConnectTimeout，这是连接主机超时；还有一种是ReadTimeout，这是从主机读取数据超时  
4. 爬虫的稳定性和容错性。网络本来就存在不稳定性，连接超时，连接重置等是常见的不稳定现象，爬虫要充分妥当地处理这些问题  
5. 网络爬虫最常见的错误莫过于连接超时和连接被重置了，而这些错误又是偶然性的，可能同一个网页第一次连接超时，但第二次可能就正常了。所以在考虑到如何这些错误的连接，我的做法是把出问题的连接记录下来到一个数组里，等第一次所有网页爬完之后，再爬一次第一次有问题的网页
6. 开始我没有配置IP代理，就用的自己电脑，后来被封了。。。而且现在用电脑上拉勾网也上不去😭所以去网上找了些高匿HTTP代理，测试了下，放入了代理池里面
7. 拉勾网反爬虫机制似乎是不断重定向。自己代理池里的不重复的共有30个，爬完一次之后牺牲了7个😓  
8. 对数组进行反向操作。假设这个数组叫arr，如果用arr.reverse()是把数组本身改变了，不会返回值，如果程序里其他地方也有可能用到这个数组，千万不要这么写；用arr[::-1]复制一份就好啦  

### JavaScript和Python  
1. Python里用json.dumps()转成JSON后，注意到如果原来有布尔值，都变成字符串了，所以在拿到JSON数据的一方要注意去处理这个问题，否则就掉坑了  
2. 一起写的时候语法什么的容易一下子懵逼，不过这次比之前有次混淆好多了，可能是那之后JS又看了一遍，更熟了一些。所以这次写这个小项目的时候也有对比着记录。平时做好记录是好习惯！😊  
  
比如Python里面下面这种语句特别方便，但是JavaScript里面没有:  
  
	# Python
	for i in range(3):
		print i,  # output: 0 1 2  
		    
然后果然有人跟我有同样的想法，SO上面给出了代码：  
  
[JavaScript's implementation of Python's `range()`](http://stackoverflow.com/questions/8273047/javascript-function-similar-to-python-range) 
  
  	// JavaScript  
  	function range(start, stop, step) {
    if (typeof stop == 'undefined') {
        // one param defined
        stop = start;
        start = 0;
    }

    if (typeof step == 'undefined') {
        step = 1;
    }

    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
        return [];
    }

    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
        result.push(i);
    }

    return result;
	};  
	    
