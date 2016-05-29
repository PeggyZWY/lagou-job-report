#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 思路：在这个Python文件里处理好所有的数据，并把结果输出为一个JS文件，然后在HTML那里，直接引入这里写出的JS文件，把这些处理好的数据当成全局变量
# 此程序中包含把totalCount重新建一个表:totalcount；在表lagou中新建了一列developmentStage
# 
# 并请注意：在这个程序运行之前，需要对原本爬虫爬下来的salary一列数据进行整理。原本这一列中是各种各样的，最后目标是归为salary_list = ['0-5k', '6-10k', '11-15k', '16-20k', '21-25k', '26-30k', '30k+']中的一个。为了追求尽可能大的准确性，我是人工判断整理的，如果不要那么精确，可以写个辅助程序。

import sqlite3, json, re

all_job_dict = {
    '技术': ['后端开发', '移动开发', '前端开发', '测试', '运维', 'DBA', '项目管理', '硬件开发', '企业软件', '高端技术职位'],
    '产品': ['产品经理', '产品设计师', '高端产品职位'],
    '设计': ['视觉设计', '用户研究', '交互设计', '高端设计职位'],
    '运营': ['运营', '编辑', '客服', '高端运营职位'],
    '市场与销售': ['市场/营销', '公关', '销售', '供应链', '采购', '投资', '高端市场职位'],
    '职能': ['人力资源', '行政', '财务', '法务', '高端职能职位'],
    '金融': ['投融资', '风控', '审计税务', '高端金融职位']
}
all_city_list = ['北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津']

# 大分类
first_type_list = ['技术', '产品', '设计', '运营', '市场与销售', '职能', '金融']
# print first_type_list

# 细分分类
specific_type_list = []
for first_type in first_type_list:
    specific_type_list.extend(all_job_dict[first_type])

# 大分类和细分分类一起 
both_first_and_specific_type_list = first_type_list[:]
both_first_and_specific_type_list.extend(specific_type_list)

salary_list = ['0-5k', '6-10k', '11-15k', '16-20k', '21-25k', '26-30k', '30k+']
companysize_list = ['少于15人', '15-50人', '50-150人', '150-500人', '500-2000人', '2000人以上']
financestage_list = ['初创型(未融资)', '初创型(天使轮)', '初创型(不需要融资)', '成长型(A轮)', '成长型(B轮)', '成长型(不需要融资)', '成熟型(C轮)', '成熟型(D轮及以上)', '成熟型(不需要融资)', '上市公司']
developmentstage_list = ['初创型', '成长型', '成熟型', '上市公司']
education_list = ['学历不限', '中专/高中', '大专', '本科', '硕士', '博士']
workyear_list = ['应届毕业生', '1年以下', '1-3年', '3-5年', '5-10年', '10年以上', '不限']

# all_data是要JSON化，然后写入JS文件再传给前端的JS，作为全局变量
all_data = {}


def newDB():
    print '新建表...'
    conn_new = sqlite3.connect('test.db')
    conn_new.text_factory = str
    cursor_new = conn_new.cursor()
    cursor_new.execute(
        '''CREATE TABLE IF NOT EXISTS 
               totalcount(
               id INTEGER PRIMARY KEY, positionFirstType TEXT, \
               positionType TEXT, city TEXT, totalCount INTEGER
           )
    ''')
    cursor_new.close()
    conn_new.commit()
    conn_new.close()
    print '表"totalcount"初始化完毕...'

    for position_first_type in all_job_dict:
        position_type_list = all_job_dict[position_first_type]
        for i in range(len(position_type_list)):
            this_specific_type = position_type_list[i]
            for j in range(len(all_city_list)):
                this_city = all_city_list[j]
                total_count = total_count_for_city_and_positiontype(this_city, this_specific_type)
                try:
                    conn = sqlite3.connect('test.db')
                    conn.text_factory = str
                    cursor = conn.cursor()
                    # print '开始写入数据库'
                    cursor.execute(
                        '''INSERT INTO
                                totalcount(
                                id, positionFirstType, positionType, city, totalCount)
                            VALUES(NULL, ?, ?, ?, ?)
                        ''',
                        [position_first_type, this_specific_type, this_city, total_count])
                    cursor.close()
                    conn.commit()
                    conn.close()
                    # print '数据库已关闭，此条记录已入库'
                except sqlite3.Error, e:
                    print 'data exists:', positionType, city, e


def add_column_developmentStage():
    try:
        conn = sqlite3.connect('test.db')
        conn.text_factory = str
        cursor = conn.cursor()
        # 测试到底存在不存在这一列，因为第二次运行时就存在了
        cmd = 'select * from lagou where developmentStage="初创型"'
        cursor.execute(cmd)
        cursor.close()
        conn.commit()
        conn.close()
    except sqlite3.Error, e:
        print 'sqlite3 error: ', cmd, e
        # 如果存在此列，则跳过。防止第二次运行此函数时出错
        if re.search('duplicate column name', str(e), flags=0):
            print '此列已存在，跳过此函数'
            return False
        elif re.search('no such column', str(e), flags=0):
            print '此列尚未存在，所以现在在表lagou中新建一列developmentStage'

            conn = sqlite3.connect('test.db')
            conn.text_factory = str
            cursor = conn.cursor()
            cmd0 = 'ALTER table lagou add column developmentStage TEXT'
            cmd1 = 'UPDATE lagou set developmentStage="初创型" where (financeStage="' + financestage_list[0] + '" or financeStage="' + financestage_list[1] + '" or financeStage="' + financestage_list[2] + '")'
            cmd2 = 'UPDATE lagou set developmentStage="成长型" where (financeStage="' + financestage_list[3] + '" or financeStage="' + financestage_list[4] + '" or financeStage="' + financestage_list[5] + '")'
            cmd3 = 'UPDATE lagou set developmentStage="成熟型" where (financeStage="' + financestage_list[6] + '" or financeStage="' + financestage_list[7] + '" or financeStage="' + financestage_list[8] + '")'
            cmd4 = 'UPDATE lagou set developmentStage="上市公司" where financeStage="' + financestage_list[9] + '"'
            cursor.execute(cmd0)
            cursor.execute(cmd1)
            cursor.execute(cmd2)
            cursor.execute(cmd3)
            cursor.close()
            conn.commit()
            conn.close()
            print '在表lagou中新建一列developmentStage已完成'


def get_key_of_the_largest_value(d):
    sorted_d = sorted(d.items(), key = lambda d:d[1])
    print sorted_d
    result = sorted_d[len(sorted_d) - 1][0]
    return result


def total_count_for_city_and_positiontype(city, positionType):
    count = {}
    conn = sqlite3.connect('test.db')

    if positionType == 'DBA':
        positionType = 'dba'
    cmd = 'SELECT id, city, positionType, totalCount FROM lagou WHERE (city = "' + city + '" and positionType = "' + positionType + '")'
    print 'cmd:', cmd
    cursor = conn.execute(cmd)
    fetch_all = cursor.fetchall()
    cursor.close()
    conn.close()

    if len(fetch_all) < 1:
        return 0

    for each_tuple in fetch_all:
        if count.has_key(each_tuple[3]):
            count[each_tuple[3]] += 1
        else:
            count[each_tuple[3]] = 1
    # print 'city:', city, 'positionType:', positionType
    # print get_key_of_the_largest_value(count)
    return get_key_of_the_largest_value(count)


# 按大分类筛选，得到数量
def get_positionfirsttype_data():
    positionfirsttype_data = []
    for first_type in first_type_list:
        this_firsttype_data = {}
        # print first_type
        conn = sqlite3.connect('test.db')

        cmd = 'SELECT positionFirstType, sum(totalCount) as positionFirstTypeCount from totalcount where positionFirstType="' + first_type + '"'

        # print 'cmd:', cmd
        cursor = conn.execute(cmd)
        fetch_all = cursor.fetchall()
        # print fetch_all[0][0], fetch_all[0][1]
        this_firsttype_data['name'] = fetch_all[0][0]
        this_firsttype_data['value'] = fetch_all[0][1]
        # print this_firsttype_data['name'], this_firsttype_data['value']
        positionfirsttype_data.append(this_firsttype_data)
        cursor.close()
        conn.close()

    all_data['position_pie_chart_data']['positionfirsttype_data'] = positionfirsttype_data
    # 到时候前端画图时可用allData['position_pie_chart_data']["positionfirsttype_data"]来获得大分类


# 按细分分类筛选，得到数量
def get_specifictype_data():
    specifictype_data = []
    for specific_type in specific_type_list:
        this_specifictype_data = {}

        conn = sqlite3.connect('test.db')
        cmd = 'SELECT positionType, sum(totalCount) as positionTypeCount from totalcount where positionType="' + specific_type + '"'
        # print 'cmd:', cmd
        cursor = conn.execute(cmd)
        fetch_all = cursor.fetchall()
        # print fetch_all[0][0], fetch_all[0][1]
        this_specifictype_data['name'] = fetch_all[0][0]
        this_specifictype_data['value'] = fetch_all[0][1]
        # print this_specifictype_data['name'], this_specifictype_data['value']
        specifictype_data.append(this_specifictype_data)
        cursor.close()
        conn.close()

    all_data['position_pie_chart_data']['specifictype_data'] = specifictype_data
    # 到时候在画图时可用allData['position_pie_chart_data']["specifictype_data"]来获得细分分类


# 按大分类和城市获取总计数
def getdata_with_firsttype_and_city():
    data = []
    # print first_type_list
    for first_type in first_type_list:
        this_firsttype_data = {}
        this_firsttype_data['name'] = first_type
        this_firsttype_data['data'] = []
        this_firsttype_data['type'] = 'bar'
        this_firsttype_data['stack'] = '总量'
        this_firsttype_data['label'] = {}
        this_firsttype_data['label']['normal'] = {}
        # 后来发现在自己图里有数值显示并不好看，所以去掉了
        # this_firsttype_data['label']['normal']['show'] = 'true'
        this_firsttype_data['label']['normal']['position'] = 'insideRight'
        conn = sqlite3.connect('test.db')
        for city in all_city_list:
            cmd = 'SELECT positionFirstType, city, sum(totalCount) as count from totalcount where (positionFirstType="' + first_type + '" and city="' + city + '")'
            # print '>>> cmd:', cmd
            cursor = conn.execute(cmd)
            fetch_all = cursor.fetchall()
            
            # print fetch_all[0][0], fetch_all[0][1], fetch_all[0][2]
            this_firsttype_data['data'].append(fetch_all[0][2])
        cursor.close()
        conn.close()
        data.append(this_firsttype_data)
    all_data['totalcount_in_every_city_bar_chart_data']['seriesData'] = data


# 只有一个条件，得到总计数。为了后面画扇形图
def getdata_with_one_condition(condition, order_list, name):
    # print ','.join(order_list)
    data = []
    fetchresult_dict = {}
    conn = sqlite3.connect('test.db')
    cmd = 'select ' + condition + ' , count(*) as ' + condition + 'Count from lagou group by ' + condition
    # print '>>> cmd:', cmd
    cursor = conn.execute(cmd)
    fetch_all = cursor.fetchall()
    for row in fetch_all:
        size = row[0]
        count = row[1]
        fetchresult_dict[size] = count
    cursor.close()
    conn.close()
    # print fetchresult_dict
    for size_type in order_list:
        tmp_dict = {}
        tmp_dict['name'] = size_type
        # print size_type
        tmp_dict['value'] = fetchresult_dict[size_type.decode('utf-8')]
        data.append(tmp_dict)
    # print data
    all_data[name]['seriesData'] = data


# 为了后面画punch card的图。
# x_series_list是横轴从左到右的列表，y_series_list是纵轴从上往下的列表
# name是为了存储出来数据给字典的键命名
# y_series是纵轴那些数据是什么，这里要填写在数据库里那一列的名称
# 由于x轴在这里都是salary，因为后面所有此类图是探究y轴的那个东西与薪资的关系。所以没有设计x_series了
def getdata_for_punchcard(x_series_list, y_series_list, name, y_series):
    data = []
    x_series_len = len(x_series_list)
    y_series_len = len(y_series_list)
    conn = sqlite3.connect('test.db')
    for i in range(x_series_len):
        for j in range(y_series_len):
            cmd = 'SELECT cleanedSalary, ' + y_series + ' ,count(*) as cleanedSalaryCount from lagou where (cleanedSalary="' + x_series_list[i] + '" and ' + y_series + '="' + y_series_list[j] + '")'
            print '>>> cmd:', cmd
            cursor = conn.execute(cmd)
            fetch_all = cursor.fetchall()
            tmp_list = [i, j, fetch_all[0][2]]
            data.append(tmp_list)
            print tmp_list
    # print data
    cursor.close()
    conn.close()
    all_data[name]['data'] = data


def draw03_company_size_pie_chart(condition):
    all_data['company_size_pie_chart_data'] = {}
    all_data['company_size_pie_chart_data']['legend'] = companysize_list
    getdata_with_one_condition(condition, companysize_list, 'company_size_pie_chart_data')


def draw04_finance_stage_pie_chart(condition):
    all_data['finance_stage_pie_chart_data'] = {}
    all_data['finance_stage_pie_chart_data']['legend'] = financestage_list
    getdata_with_one_condition(condition, financestage_list, 'finance_stage_pie_chart_data')


def draw10_education_pie_chart(condition):
    all_data['education_pie_chart_data'] = {}
    all_data['education_pie_chart_data']['legend'] = education_list
    getdata_with_one_condition(condition, education_list, 'education_pie_chart_data')   



def draw01_position_pie_chart():
    all_data['position_pie_chart_data'] = {}
    # 图例
    all_data['position_pie_chart_data']['legend'] = first_type_list
    # 大分类
    get_positionfirsttype_data()
    # 细分分类
    get_specifictype_data()
    # print all_data



def draw02_totalcount_in_every_city_bar_chart():
    all_data['totalcount_in_every_city_bar_chart_data'] = {}
    all_data['totalcount_in_every_city_bar_chart_data']['legend'] = first_type_list
    all_data['totalcount_in_every_city_bar_chart_data']['all_city_list'] = all_city_list
    getdata_with_firsttype_and_city()





def draw05_city_and_salary_punchcard():
    all_data['city_and_salary_punchcard_data'] = {}
    all_data['city_and_salary_punchcard_data']['x_series'] = salary_list
    all_data['city_and_salary_punchcard_data']['y_series'] = ['北京', '上海', '杭州', '深圳', '杭州', '广州', '成都']
    all_data['city_and_salary_punchcard_data']['y_series'].reverse()

    x_series_list = all_data['city_and_salary_punchcard_data']['x_series']
    y_series_list = all_data['city_and_salary_punchcard_data']['y_series']

    getdata_for_punchcard(x_series_list, y_series_list, 'city_and_salary_punchcard_data', 'city')


def draw06_positiontype_and_salary_punchcard():
    all_data['positiontype_and_salary_punchcard_data'] = {}
    all_data['positiontype_and_salary_punchcard_data']['x_series'] = salary_list
    all_data['positiontype_and_salary_punchcard_data']['y_series'] = first_type_list
    all_data['positiontype_and_salary_punchcard_data']['y_series'].reverse()

    x_series_list = all_data['positiontype_and_salary_punchcard_data']['x_series']
    y_series_list = all_data['positiontype_and_salary_punchcard_data']['y_series']

    getdata_for_punchcard(x_series_list, y_series_list, 'positiontype_and_salary_punchcard_data', 'positionFirstType')


def draw07_education_and_salary_punchcard():
    all_data['education_and_salary_punchcard_data'] = {}
    all_data['education_and_salary_punchcard_data']['x_series'] = salary_list
    all_data['education_and_salary_punchcard_data']['y_series'] = education_list
    all_data['education_and_salary_punchcard_data']['y_series'].reverse()

    x_series_list = all_data['education_and_salary_punchcard_data']['x_series']
    y_series_list = all_data['education_and_salary_punchcard_data']['y_series']

    getdata_for_punchcard(x_series_list, y_series_list, 'education_and_salary_punchcard_data', 'education')


def draw08_workyear_and_salary_punchcard():
    all_data['workyear_and_salary_punchcard_data'] = {}
    all_data['workyear_and_salary_punchcard_data']['x_series'] = salary_list
    all_data['workyear_and_salary_punchcard_data']['y_series'] = workyear_list
    all_data['workyear_and_salary_punchcard_data']['y_series'].reverse()

    x_series_list = all_data['workyear_and_salary_punchcard_data']['x_series']
    y_series_list = all_data['workyear_and_salary_punchcard_data']['y_series']

    getdata_for_punchcard(x_series_list, y_series_list, 'workyear_and_salary_punchcard_data', 'workYear')


def draw09_developmentstage_and_salary_punchcard():
    all_data['developmentstage_and_salary_punchcard_data'] = {}
    all_data['developmentstage_and_salary_punchcard_data']['x_series'] = salary_list
    all_data['developmentstage_and_salary_punchcard_data']['y_series'] = developmentstage_list
    all_data['developmentstage_and_salary_punchcard_data']['y_series'].reverse()

    x_series_list = all_data['developmentstage_and_salary_punchcard_data']['x_series']
    y_series_list = all_data['developmentstage_and_salary_punchcard_data']['y_series']

    getdata_for_punchcard(x_series_list, y_series_list, 'developmentstage_and_salary_punchcard_data', 'developmentStage')







def analyse():

    # 新建表"totalcount"
    newDB()
    # 在表"lagou"中增加一列
    add_column_developmentStage()


    draw03_company_size_pie_chart('companySize')
    draw04_finance_stage_pie_chart('financeStage')    
    draw10_education_pie_chart('education')
    
    draw01_position_pie_chart()
    draw02_totalcount_in_every_city_bar_chart()

    draw05_city_and_salary_punchcard()
    draw06_positiontype_and_salary_punchcard()
    draw07_education_and_salary_punchcard()
    draw08_workyear_and_salary_punchcard()
    draw09_developmentstage_and_salary_punchcard()

    # 之后这个这个JS文件会被当做全局变量引入HTML中
    with open('results_dict.js', 'a+') as f:
        f.write('var allData = ')
        f.write(json.dumps(all_data))
        f.write(';\n')
    


if __name__ == '__main__':
    analyse()


