#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os, sys, math, random, time, datetime, requests, urllib, json, sqlite3
import logging
from bs4 import BeautifulSoup


# 配置logging模块。filemode是追加模式（防止万一程序异常自动退出，然后debug后重新运行，不会覆盖掉之前的log记录）
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='test.log',
                    filemode='a')

# 37 in all
all_job_dict = {\
    '技术': ['后端开发', '移动开发', '前端开发', '测试', '运维', 'DBA', '高端技术职位', '项目管理', '硬件开发', '企业软件'],
    '产品': ['产品经理', '产品设计师', '高端产品职位'],
    '设计': ['视觉设计', '用户研究', '高端设计职位', '交互设计'],
    '运营': ['运营', '编辑', '客服', '高端运营职位'],
    '市场与销售': ['市场', '公关', '销售', '高端市场职位', '供应链', '采购', '投资'],
    '职能': ['人力资源', '行政', '财务', '高端职能职位', '法务'],
    '金融': ['投融资', '风控', '审计税务', '高端金融职位']
}

# 13 in all
all_city_list = ['北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津']

lagou_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive'
}

# 为了反反爬虫，在网上找了一些可用的高匿国内HTTP代理。以下list实际有重复，用len(set(http_pool))得到去重后有30个
# 爬虫运行完，根据记录，发现被封了7个
# 如果要使用此爬虫，请更新代理，因为这些代理有可能过期
http_pool = [
             'http://27.202.244.248:8888',
             'http://123.166.231.71:8888',
             'http://124.202.181.186:8118',
             'http://117.21.182.110:80',
             'http://101.96.11.29:80',
             'http://123.169.238.33:8888',
             'http://1.181.244.50:8888',
             'http://58.49.165.172:8118',
             'http://221.226.67.202:8118',
             'http://61.135.217.17:80',
             'http://114.95.145.25:8118',
             'http://182.44.13.153:8888',
             'http://123.132.199.161:8888',
             'http://61.135.217.7:80',
             'http://119.179.114.28:8888',
             'http://124.202.223.202:8118',
             'http://106.75.128.87:80',
             'http://182.36.167.121:8888',
             'http://112.253.2.61:8080',
             'http://121.237.139.222:8118',
             'http://124.202.223.202:8118',
             'http://119.179.114.28:8888',
             'http://222.39.112.12:8118',
             'http://124.202.179.242:8118',
             'http://106.75.128.87:80',
             'http://123.132.199.161:8888',
             'http://61.135.217.16:80',
             'http://106.75.128.88:80',
             'http://220.249.21.222:8118',
             'http://124.202.181.186:8118',
             'http://121.69.36.122:8118',
             'http://182.44.13.153:8888',
             'http://114.95.145.25:8118',
             'http://61.135.217.7:80',
             'http://182.44.13.153:8888',
             'http://61.135.217.3:80',
             'http://61.135.217.16:80',
             'http://222.39.64.13:8118',
             'http://106.75.128.87:80',
             'http://112.253.2.61:8080',
             'http://203.195.204.168:8080',
             'http://123.132.199.161:8888',
             'http://110.72.27.153:8123'             
            ]


def current_time():
    FILETIMEFORMAT = '%Y%m%d_%X'
    current_time = time.strftime(FILETIMEFORMAT, time.localtime()).replace(':', '')
    return str(current_time)

# 记录因第一次爬取不成功而要第二次发送AJAX请求的信息
these_are_time_out = []
# 记录被屏蔽的代理IP，它们已从http_pool里移除，可以节约更换代理尝试的时间
useless_url_list = []


# 如果数据库不存在，则新建数据库；存在会自动跳过
# positionId是爬取下来的信息中获得的，是唯一的。所以之后加入数据库时根据这个的唯一性，可能重复而数据库抛错，需要处理（跳过就行了）
# totalCount还是有必要的，因为LAGOU网只会显示30页的信息，每页15条，至多450条。这450条可以以部分代替整体做统计，但是不能代替职位总数。刚好JSON里这个字段就是职位总数
def newDB():
    print '新建数据库...'
    conn = sqlite3.connect('test.db')
    conn.text_factory = str
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS 
               lagou(
               id INTEGER PRIMARY KEY, positionId INTEGER UNIQUE, city TEXT, positionFirstType TEXT, \
               positionType TEXT, salary TEXT, financeStage TEXT, companySize TEXT, \
               jobNature TEXT, positionAdvantage TEXT, workYear TEXT, education TEXT, \
               companyShortName TEXT, companyLabelList TEXT, totalCount INTEGER
           )
    ''')
    cursor.close()
    conn.commit()
    conn.close()
    print '数据库初始化完毕...'


# 不要在sqlite数据库用Unicode，转成UTF-8编码
def byteify(input):
    if isinstance(input, dict):
        return {byteify(key):byteify(value) for key,value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


# 为了后面JSON要存入数据库的值做准备（是列表的要转成字符串，否则类型不对，不能插入数据库）
def value2str(input):
    if isinstance(input, list):
        if len(input) > 1:
            return ','.join(input)
        elif len(input) == 1:
            return input[0]
        else:
            return ''
    else:
        return input


# second_read是布尔值，第二次爬取为True; 第一次为False
# this_page_num为默认参数，因为每次调用此函数，都是从第一页开始
def crawl(job_name, city_name, headers, timeout, second_read, this_page_num = 1):
    # flag为了判断现在页数是否大于了最大页数
    flag = True
    url = 'http://www.lagou.com/jobs/positionAjax.json?&city=' + urllib.quote(city_name)
    
    while flag:
        lagou_params = {'first': 'false', 'pn': this_page_num, 'kd': job_name}
        try:
            # 始终是取http_pool中第一个，之后会pop(0)，以及再append()回来，形成队列
            lagou_proxies = {
              'http': http_pool[0],
              'https': 'http://10.10.1.10:1080'
            }
            s = requests.Session()
            # 这些print是为了方便在命令行上看爬取过程的，也没必要加入log里
            print '-----------'
            print '>>> session built'
            print 'this city_name:', city_name
            print urllib.quote(city_name)
            print 'this url:', url
            print 'this params kd, pn:', lagou_params['kd'], lagou_params['pn']
            print 'this proxy is:', lagou_proxies['http']
            r = s.get(url, params = lagou_params, headers = lagou_headers, proxies = lagou_proxies, timeout = timeout)
            print '>>> r built'
            print r.status_code
            # 如果请求成功
            if r.status_code == 200:
                print 'r_json begin'
                r_json = r.json()['content']['positionResult']
                print 'r_json finish'
                page_num = math.ceil(float(r_json['totalCount']) / 15)
                print 'totalCount:', r_json['totalCount']
                print 'page_num:', page_num
                # 最大页数取计算出的页数和30中小的那个
                max_page_num = (page_num if page_num <= 30 else 30)
                print 'max_page_num:', max_page_num
                job_json = r_json['result']
                # 对于没结果的要处理
                if len(job_json) < 1:
                    print 'length of job_json is 0'
                    break
                else:
                    print 'job_json begin'
                    job_json_length = len(job_json)
                    # 以下为把一页至多15条信息一一加入数据库，如果重复（根据positionId的唯一性）会自动跳过
                    # 这个以及数据库写入时会判重及及时向数据库提交事务，保证了万一（作者执行时并没有）出错导致程序出错，在更改bug后重新运行程序，既保留了之前已经爬取的数据，也不会重复保存记录，而且不需要人为去删除之前的文件
                    for i in range(job_json_length):
                        job_json_each = job_json[i]

                        positionId = job_json[i]['positionId']
                        city = job_json[i]['city']
                        positionFirstType = job_json[i]['positionFirstType']
                        positionType = job_json[i]['positionType']
                        salary = job_json[i]['salary']
                        financeStage = job_json[i]['financeStage']
                        companySize = job_json[i]['companySize']
                        jobNature = job_json[i]['jobNature']
                        positionAdvantage = job_json[i]['positionAdvantage']
                        workYear = job_json[i]['workYear']
                        education = job_json[i]['education']
                        companyShortName = job_json[i]['companyShortName']
                        companyLabelList = job_json[i]['companyLabelList']
                        totalCount = r_json['totalCount']

                        try:
                            conn = sqlite3.connect('test.db')
                            conn.text_factory = str
                            cursor = conn.cursor()
                            print '开始写入数据库'
                            cursor.execute(
                                '''INSERT INTO 
                                        lagou(
                                        id, positionId, city, positionFirstType, \
                                        positionType, salary, financeStage, companySize, \
                                        jobNature, positionAdvantage, workYear, education, \
                                        companyShortName, companyLabelList, totalCount) 
                                    VALUES(
                                        NULL, ?, ?, ?, \
                                        ?, ?, ?, ?, \
                                        ?, ?, ?, ?, \
                                        ?, ?, ?)
                                ''',
                                [positionId, city, positionFirstType, \
                                positionType, salary, financeStage, companySize, \
                                jobNature, positionAdvantage, workYear, education, \
                                companyShortName, value2str(companyLabelList), totalCount])
                                # companyLabelList是parameter 11，也就是说是以提供参数的数组，而且是数组下标为11，即第12个
                            # print '准备关闭游标'
                            cursor.close()
                            # print '游标已关闭，准备提交事务'
                            conn.commit()
                            # print '事务提交完毕，准备关闭数据库'
                            conn.close()
                            print '数据库已关闭，此条记录已入库'
                        except sqlite3.Error, e:
                            print '**********data exists:', positionId, e
                    
                    print 'job_json finish'
                    print '完成爬取%s市"%s"职位第%s页JSON信息...' % (city_name, job_name, str(this_page_num))
                    logging.info('完成爬取%s市"%s"职位第%s页JSON信息...' % (city_name, job_name, str(this_page_num)))
                    # 如果是二次爬取，只要爬要的那一页，不必要再爬取此页后面的页面了。于是在此就可以退出循环了。否则页面数加一，与最大页数比较，看是否还要继续爬取后一页
                    if second_read is True:
                        break
                    print '==========='
                    this_page_num += 1
                    if this_page_num == 1:
                        continue
                    if this_page_num > max_page_num:
                        flag = False
            if r.status_code == 500:
                # 服务器如果出错返回500状态码，自己抛了一个错误，后面处理是跟链接主机超时一样的
                raise Exception('status_code is 500')
        except Exception, e:
            # 下面各种异常处理保证了程序的健壮性
            print '*** error match request:', e
            # 以下是链接主机超时处理时换IP代理池里下一个代理
            if re.search('HTTPConnectionPool', str(e), flags=0) and re.search('Max retries exceeded with url', str(e), flags=0):
                http_pool_first_ele = http_pool.pop(0)
                http_pool.append(http_pool_first_ele)
                print '更换了IP代理'
                continue
            # 服务器如果出错返回500状态码，处理也是换IP代理池里下一个代理
            elif re.search('status_code is 500', str(e), flags=0):
                http_pool_first_ele = http_pool.pop(0)
                http_pool.append(http_pool_first_ele)
                print '500.更换了IP代理'
                continue
            # 处理也是换IP代理池里下一个代理
            elif re.search('Connection aborted', str(e), flags=0): 
                http_pool_first_ele = http_pool.pop(0)
                http_pool.append(http_pool_first_ele)
                print 'Connection aborted.更换了IP代理'
                continue
            # 以下是说明了此IP已被屏蔽，没有用了，从IP代理池中移除，加入到无用列表里去
            elif re.search('Exceeded 30 redirects', str(e), flags=0):
                useless_url = http_pool.pop(0)
                useless_url_list.append(useless_url)
                print '此链接无效或已被屏蔽，舍弃之:', useless_url
            # 以下是从主机读取数据超时，那么这次爬取就到此为止，并且把这些信息记录到要二次爬取的列表里
            elif re.search('HTTPConnectionPool', str(e), flags=0) and re.search('Read timed out', str(e), flags=0):
                http_pool_first_ele = http_pool.pop(0)
                http_pool.append(http_pool_first_ele)
                print '更换了IP代理'
                # 如果二次爬取时又出错了，不要管了，不需要三次爬取了。事实上，之后运行程序，共出现了34次二次爬取，而且二次爬取时都成功了
                if second_read is True:
                    break
                this_time_out = {}
                this_time_out['city_name'] = city_name
                this_time_out['params'] = lagou_params
                this_time_out['headers'] = lagou_headers
                this_time_out['proxies'] = lagou_proxies
                these_are_time_out.append(this_time_out)
                print '从主机读取超时，已加入二次读取队列:', this_time_out
                # 下面这个是防止是对于一个城市和职位的查询的第一个页面就出错，而此时没有获得任何JSON信息，所以人为定义最大页数为30，以防下面出现max_page_num这个变量未定义的错误
                if this_page_num == 1:
                    max_page_num = 30
                this_page_num += 1
                if this_page_num > max_page_num:
                    flag = False
                continue
            else:
                break



if __name__ == '__main__':
    begin_time = current_time()
    print '开始时间:', begin_time
    newDB()
    logging.info('http_pool_length:', len(http_pool))
    for key in all_job_dict:
        detail_kind_length = len(all_job_dict[key])
        # 对于每一个职位名 
        for i in range(detail_kind_length):
            # 在每个城市
            for j in all_city_list:
                # 先第一次爬取，设置超时时间为4秒
                crawl(all_job_dict[key][i], j, lagou_headers, 4, False)
                # 完成每个城市的爬取后，歇歇气，防止反爬虫机制封IP
                time.sleep(1 + random.random())
            # 完成每个职位名爬取后，不管怎样，换一次IP代理
            http_pool_first_ele = http_pool.pop(0)
            http_pool.append(http_pool_first_ele)
            print '更换了IP代理'
        print '==========================='
    print '========================================='
    for key in all_job_dict:
        print key, ':', value2str(all_job_dict[key])
    print '城市 :', value2str(all_city_list)
    print 'http_pool_length:', len(http_pool)
    print '要二次读取的数量:', len(these_are_time_out)
    print '要二次读取的详情:', these_are_time_out
    # 如果要二次读取的数量为0，也就意味着不要二次读取啦
    if len(these_are_time_out) > 0:
        print '''
        =========================================
        开始二次读取......
        ========================================='''
        for i in range(len(these_are_time_out)):
            job_name = these_are_time_out[i]['params']['kd']
            city_name = these_are_time_out[i]['city_name']
            headers = these_are_time_out[i]['headers']
            pn = these_are_time_out[i]['params']['pn']
            # 二次爬取时，超时时间设置的长了一些，为6秒。另外这个页数不是原来默认的1了，要根据之前保存的页数传进去
            crawl(job_name, city_name, headers, 6, True, pn)
        print '二次读取完成'
    # 看看有哪些代理IP被屏蔽了
    print '舍弃的代理:', useless_url_list
    print '所有已完成'
    print 'http_pool_length:', len(http_pool)
    finish_time = current_time()
    # 看看开始时间和最终时间
    # 最后我的结果是1.5小时得到了约64000行记录，平均1秒获得11.5行记录
    print '开始时间:', begin_time, '结束时间:', finish_time

