window.onload = function() {
    function draw01_position_pie_chart(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var legendData = allData['position_pie_chart_data']['legend'];
        var firsttypeCount = allData['position_pie_chart_data']['positionfirsttype_data'];
        var specifictypeCount = allData['position_pie_chart_data']['specifictype_data'];

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw01')[0]);

    /* 如果需要延迟显示可以这么写
        myChart.showLoading({
            text: '正在努力的读取数据中...'
        });
    */

        // console.log(legendData);
        // console.log(firsttypeCount);
        // console.log(specifictypeCount);

        // 指定图表的配置项和数据
        function optionConfig(legendData, firsttypeCount, specifictypeCount) {
            var option = {
                title : {
                    text: '互联网公司职位需求',
                    x:'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b}: {c} ({d}%)"
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    data: legendData
                },
                series: [
                    {
                        name:'职位需求',
                        type:'pie',
                        selectedMode: 'single',
                        radius: [0, '31%'],
                        center: ['50%', '55%'],
                        label: {
                            normal: {
                                position: 'inner'
                            }
                        },
                        labelLine: {
                            normal: {
                                show: false
                            }
                        },
                        data: firsttypeCount
                    },
                    {
                        name:'职位分类',
                        type:'pie',
                        radius: ['34%', '68%'],
                        center: ['50%', '55%'],
                        data: specifictypeCount
                    }
                ]
            };
            return option;
        }


    /* 如果需要延迟显示可以这么写，或者配成其他函数的回调函数
        setTimeout(function() {
            myChart.hideLoading();
            myChart.setOption(optionConfig(legendData, firsttypeCount, specifictypeCount));
        }, 1000)
    */

        // 使用刚指定的配置项和数据显示图表。
        // myChart.setOption(option);
        myChart.setOption(optionConfig(legendData, firsttypeCount, specifictypeCount));
    }


    function draw02_totalcount_in_every_city_bar_chart(allData) {
        var legendData = allData['totalcount_in_every_city_bar_chart_data']['legend'];
        var cityList = allData['totalcount_in_every_city_bar_chart_data']['all_city_list'];
        var seriesData = allData['totalcount_in_every_city_bar_chart_data']['seriesData'];
        // json会把布尔值转成字符串。但是不要显示数字了
        // for (var i = 0, len = seriesData.length; i < len; i++){
        //     seriesData[i]['label']['normal']['show'] = true;
        // }

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw02')[0]);

        function optionConfig(legendData, cityList, seriesData) {
            var option = {
                title : {
                    text: '互联网公司地域分布',
                    x:'center'
                },
                tooltip : {
                    trigger: 'axis',
                    axisPointer : {            // 坐标轴指示器，坐标轴触发有效
                        type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                legend: {
                    x: 'center',
                    y: 'bottom',
                    data: legendData
                },
                // grid: {
                //     left: '3%',
                //     right: '4%',
                //     bottom: '3%',
                //     containLabel: true
                // },
                yAxis:  {
                    type: 'value'
                },
                xAxis: {
                    type: 'category',
                    data: cityList
                },
                series: seriesData
            };
            return option;
        }

        myChart.setOption(optionConfig(legendData, cityList, seriesData));
    }

    function draw03_company_size_pie_chart(allData) {
        var legendData = allData['company_size_pie_chart_data']['legend'];
        var seriesData = allData['company_size_pie_chart_data']['seriesData'];
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw03')[0]);

        function optionConfig(legendData, seriesData) {
            var option = {
                title : {
                    text: '互联网公司人数分布',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x : 'left',
                    data: legendData
                },
                toolbox: {
                    feature : {
                        magicType : {
                            type: ['pie', 'funnel']
                        },
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        type:'pie',
                        radius : [35, 180],
                        roseType : 'radius',
                        data: seriesData
                    }
                ]
            };

            return option;
        }

        myChart.setOption(optionConfig(legendData, seriesData));
    }

    function draw04_finance_stage_pie_chart(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var legendData = allData['finance_stage_pie_chart_data']['legend'];
        var seriesData = allData['finance_stage_pie_chart_data']['seriesData'];
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw04')[0]);

        function optionConfig(legendData, seriesData) {
            var option = {
                title : {
                    text: '互联网公司融资情况',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x: 'left',
                    data: legendData
                },
                toolbox: {
                    feature : {
                        magicType : {
                            type: ['pie', 'funnel']
                        },
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        type:'pie',
                        radius : [35, 180],
                        roseType : 'radius',
                        center: ['55%', '50%'], 
                        data: seriesData
                    }
                ]
            };
            return option;
        }

        myChart.setOption(optionConfig(legendData, seriesData));
    }


    function draw05_city_and_salary_punchcard(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var xSeries = allData['city_and_salary_punchcard_data']['x_series'];
        var ySeries = allData['city_and_salary_punchcard_data']['y_series'];
        var seriesData = allData['city_and_salary_punchcard_data']['data']

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw05')[0]);

        function optionConfig(xSeries, ySeries, seriesData) {
            var option = {
                title: {
                    text: '互联网发展前六强城市工资整体分布比例',
                    x: 'center'
                },
                legend: {
                    data: ['计数'],
                    left: 'left'
                },
                tooltip: {
                    position: 'top',
                    formatter: function (params) {
                        return params.value[2];
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                grid: {
                    left: 60,
                    bottom: 10,
                    right: 60,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: xSeries,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'category',
                    data: ySeries,
                    axisLine: {
                        show: false
                    }
                },
                series: [{
                    name: '计数',
                    type: 'scatter',
                    symbolSize: function (val) {
                        return val[2] * 0.02;
                    },
                    data: seriesData,
                    animationDelay: function (idx) {
                        return idx * 5;
                    }
                }]
            };
            return option;
        }

        myChart.setOption(optionConfig(xSeries, ySeries, seriesData));
    }


    function draw06_positiontype_and_salary_punchcard(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var xSeries = allData['positiontype_and_salary_punchcard_data']['x_series'];
        var ySeries = allData['positiontype_and_salary_punchcard_data']['y_series'];
        var seriesData = allData['positiontype_and_salary_punchcard_data']['data']

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw06')[0]);

        function optionConfig(xSeries, ySeries, seriesData) {
            var option = {
                title: {
                    text: '职位与工资分布',
                    x: 'center'
                },
                legend: {
                    data: ['计数'],
                    left: 'left'
                },
                tooltip: {
                    position: 'top',
                    formatter: function (params) {
                        return params.value[2];
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                grid: {
                    left: 60,
                    bottom: 10,
                    right: 60,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: xSeries,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'category',
                    data: ySeries,
                    axisLine: {
                        show: false
                    }
                },
                series: [{
                    name: '计数',
                    type: 'scatter',
                    symbolSize: function (val) {
                        return val[2] * 0.01;
                    },
                    data: seriesData,
                    animationDelay: function (idx) {
                        return idx * 5;
                    }
                }]
            };
            return option;
        }

        myChart.setOption(optionConfig(xSeries, ySeries, seriesData));
    }


    function draw07_education_and_salary_punchcard(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var xSeries = allData['education_and_salary_punchcard_data']['x_series'];
        var ySeries = allData['education_and_salary_punchcard_data']['y_series'];
        var seriesData = allData['education_and_salary_punchcard_data']['data']

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw07')[0]);

        function optionConfig(xSeries, ySeries, seriesData) {
            var option = {
                title: {
                    text: '学历与工资分布',
                    x: 'center'
                },
                legend: {
                    data: ['计数'],
                    left: 'left'
                },
                tooltip: {
                    position: 'top',
                    formatter: function (params) {
                        return params.value[2];
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                grid: {
                    left: 60,
                    bottom: 10,
                    right: 60,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: xSeries,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'category',
                    data: ySeries,
                    axisLine: {
                        show: false
                    }
                },
                series: [{
                    name: '计数',
                    type: 'scatter',
                    symbolSize: function (val) {
                        return val[2] * 0.0085;
                    },
                    data: seriesData,
                    animationDelay: function (idx) {
                        return idx * 5;
                    }
                }]
            };
            return option;
        }

        myChart.setOption(optionConfig(xSeries, ySeries, seriesData));
    }


    function draw08_workyear_and_salary_punchcard(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var xSeries = allData['workyear_and_salary_punchcard_data']['x_series'];
        var ySeries = allData['workyear_and_salary_punchcard_data']['y_series'];
        var seriesData = allData['workyear_and_salary_punchcard_data']['data']

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw08')[0]);

        function optionConfig(xSeries, ySeries, seriesData) {
            var option = {
                title: {
                    text: '工作经验与工资分布',
                    x: 'center'
                },
                legend: {
                    data: ['计数'],
                    left: 'left'
                },
                tooltip: {
                    position: 'top',
                    formatter: function (params) {
                        return params.value[2];
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                grid: {
                    left: 60,
                    bottom: 10,
                    right: 60,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: xSeries,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'category',
                    data: ySeries,
                    axisLine: {
                        show: false
                    }
                },
                series: [{
                    name: '计数',
                    type: 'scatter',
                    symbolSize: function (val) {
                        return val[2] * 0.0085;
                    },
                    data: seriesData,
                    animationDelay: function (idx) {
                        return idx * 5;
                    }
                }]
            };
            return option;
        }

        myChart.setOption(optionConfig(xSeries, ySeries, seriesData));
    }


    function draw09_developmentstage_and_salary_punchcard(allData) {
        // 图例所需要数组即为所有大分类和细分分类
        var xSeries = allData['developmentstage_and_salary_punchcard_data']['x_series'];
        var ySeries = allData['developmentstage_and_salary_punchcard_data']['y_series'];
        var seriesData = allData['developmentstage_and_salary_punchcard_data']['data']

        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw09')[0]);

        function optionConfig(xSeries, ySeries, seriesData) {
            var option = {
                title: {
                    text: '公司发展阶段与工资分布',
                    x: 'center'
                },
                legend: {
                    data: ['计数'],
                    left: 'left'
                },
                tooltip: {
                    position: 'top',
                    formatter: function (params) {
                        return params.value[2];
                    }
                },
                toolbox: {
                    feature : {
                        saveAsImage : {show: true}
                    }
                },
                grid: {
                    left: 60,
                    bottom: 10,
                    right: 60,
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: xSeries,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                            type: 'dashed'
                        }
                    },
                    axisLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'category',
                    data: ySeries,
                    axisLine: {
                        show: false
                    }
                },
                series: [{
                    name: '计数',
                    type: 'scatter',
                    symbolSize: function (val) {
                        return val[2] * 0.01;
                    },
                    data: seriesData,
                    animationDelay: function (idx) {
                        return idx * 5;
                    }
                }]
            };
            return option;
        }

        myChart.setOption(optionConfig(xSeries, ySeries, seriesData));
    }


    function draw10_education_pie_chart(allData) {
        var legendData = allData['education_pie_chart_data']['legend'];
        var seriesData = allData['education_pie_chart_data']['seriesData'];
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementsByClassName('draw10')[0]);

        function optionConfig(legendData, seriesData) {
            var option = {
                title : {
                    text: '职位学历要求',
                    x:'center'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: "{b} : {c} ({d}%)"
                },
                legend: {
                    orient: 'vertical',
                    x : 'left',
                    data: legendData
                },
                toolbox: {
                    feature : {
                        magicType : {
                            type: ['pie', 'funnel']
                        },
                        saveAsImage : {show: true}
                    }
                },
                calculable : true,
                series : [
                    {
                        type:'pie',
                        radius : [35, 180],
                        roseType : 'radius',
                        data: seriesData
                    }
                ]
            };

            return option;
        }

        myChart.setOption(optionConfig(legendData, seriesData));
    }


    // 一页上加载多个图表
    function drawAllCharts(allData) {
        draw03_company_size_pie_chart(allData);
        draw04_finance_stage_pie_chart(allData);
        draw02_totalcount_in_every_city_bar_chart(allData);
        draw05_city_and_salary_punchcard(allData);
        draw01_position_pie_chart(allData);
        draw06_positiontype_and_salary_punchcard(allData);
        draw10_education_pie_chart(allData);
        draw07_education_and_salary_punchcard(allData);
        draw08_workyear_and_salary_punchcard(allData);
        draw09_developmentstage_and_salary_punchcard(allData);
    }
    drawAllCharts(allData);
}