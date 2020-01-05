import pandas as pd
import plotly as py
import plotly.offline as py
import cufflinks as cf
from pyecharts import options as opts
from pyecharts.charts import Geo,Line,Funnel, Page,Bar, Pie, Timeline
from pyecharts.globals import ChartType, SymbolType
cf.set_config_file(offline=True, theme='ggplot')


from flask import Flask,render_template,request,escape
import csv

app = Flask(__name__)

#人均消费支出与平均薪资
df2 = pd.read_csv("consumption.csv",encoding='gbk')

def line_smooth() -> Line:
    line = (
        Line()
        .add_xaxis(list(df2.地区))
        .add_yaxis("人均消费支出（元）", list(df2.居民人均消费支出))
        .add_yaxis("平均工资（元）", list(df2.平均薪资))
        .set_global_opts(title_opts=opts.TitleOpts(title="平均工资和消费支出的关系"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return line

line_smooth().render('消费.html')

def chazhi() -> Bar:
    c = (
        Bar()
        .add_xaxis(list(df2.地区))
        .add_yaxis("差值", list(df2.差值))
        .set_global_opts(title_opts=opts.TitleOpts(title="差值", subtitle="平均工资-人均消费支出"),
                        datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],)
    )
    return c
chazhi().render('差值.html')

@app.route('/consumption',methods=['GET','POST'])
def consumption() -> 'html':
    data_str = df2.to_html()
    with open("消费.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all1 = "".join(f.readlines())
    with open("差值.html", encoding="utf8", mode="r") as f:
        plot_all2 = "".join(f.readlines())
    title = ('36个主要城市的人均消费支出与平均薪资')
    return render_template('consumption.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all1 = plot_all1,
                           the_plot_all2=plot_all2,
                           )

#人口密度
df = pd.read_csv("population_density.csv",encoding='gbk')

def geo_base() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china",itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"))
        .add("人/平方千米", zip(list(df.地区),list(df.人口密度)))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="2018年36个主要城市的人口密度情况"),
            visualmap_opts=opts.VisualMapOpts(max_=2306.6,min_=18.7,is_piecewise=True,
                                             pieces=[{'min':924,'max':2306.593060},{'min':602,'max':923.156006},{'min':362,'max':600.689035},{'min':18.781760,'max':361.142947}]))
    )
    return c
geo_base().render('人口密度.html')

@app.route('/density',methods=['GET','POST'])
def density() -> 'html':
    data_str = df.to_html()
    with open("人口密度.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的人口密度')
    return render_template('density.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#失业率
df4 = pd.read_csv("unemployment.csv",encoding='gbk')

def timeline2() -> Timeline:
    x = list(df4.地区)
    tl = Timeline()
    for i in range(2014, 2019):
        bar = (
            Bar()
            .add_xaxis(x)
            .add_yaxis("失业率", list(df4["{}年".format(i)]))
            .set_global_opts(title_opts=opts.TitleOpts("{}年各城市失业率".format(i)),
                             datazoom_opts=(opts.DataZoomOpts(type_="inside")),
                             visualmap_opts=opts.VisualMapOpts(max_=4.5,min_=0),
                            yaxis_opts=opts.AxisOpts(max_=4.5,min_=0)))
        tl.add(bar, "{}年".format(i),)
    return tl

timeline2().render('失业率.html')

@app.route('/unemployment',methods=['GET','POST'])
def unemployment() -> 'html':
    data_str = df4.to_html()
    with open("失业率.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的失业率')
    return render_template('unemployment.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#房价
df3 = pd.read_csv("house_prices.csv",encoding='gbk')

#2009-2011
def line_smooth2() -> Line:
    line = (
        Bar()
        .add_xaxis(list(df2.地区))
        .add_yaxis("2009年", list(df3['2009年']))
        .add_yaxis("2010年", list(df3['2010年']))
        .add_yaxis("2011年", list(df3['2011年']))
        .set_global_opts(title_opts=opts.TitleOpts(title="2009-2011年各城市住宅商品房平均房价变化"),
                         legend_opts=opts.LegendOpts(pos_left=380),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return line
line_smooth2().render('房价1.html')


@app.route('/house_prices1',methods=['GET','POST'])
def house_prices1() -> 'html':
    data = df3.loc[:, ['地区', '2009年', '2010年', '2011年']]
    data_str = data.to_html()
    with open("房价1.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的住宅商品房平均房价(2009-2011)')
    return render_template('house_prices1.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#2012-2014
def line_smooth3() -> Line:
    line = (
        Bar()
        .add_xaxis(list(df2.地区))
        .add_yaxis("2012年", list(df3['2012年']))
        .add_yaxis("2013年", list(df3['2013年']))
        .add_yaxis("2014年", list(df3['2014年']))
        .set_global_opts(title_opts=opts.TitleOpts(title="2012-2014年各城市住宅商品房平均房价变化"),
                         legend_opts=opts.LegendOpts(pos_left=380),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return line
line_smooth3().render('房价2.html')

@app.route('/house_prices2',methods=['GET','POST'])
def house_prices2() -> 'html':
    data = df3.loc[:, ['地区', '2012年', '2013年', '2014年']]
    data_str = data.to_html()
    with open("房价2.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的住宅商品房平均房价(2012-2014)')
    return render_template('house_prices2.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#2015-2018
def line_smooth4() -> Line:
    line = (
        Bar()
        .add_xaxis(list(df2.地区))
        .add_yaxis("2015年", list(df3['2015年']))
        .add_yaxis("2016年", list(df3['2016年']))
        .add_yaxis("2017年", list(df3['2017年']))
        .add_yaxis("2018年", list(df3['2018年']))
        .set_global_opts(title_opts=opts.TitleOpts(title="2015-2018年各城市住宅商品房平均房价变化"),
                         legend_opts=opts.LegendOpts(pos_left=380),
                         datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )
    return line
line_smooth4().render('房价3.html')

@app.route('/house_prices3',methods=['GET','POST'])
def house_prices3() -> 'html':
    data = df3.loc[:, ['地区', '2015年', '2016年', '2017年','2018年']]
    data_str = data.to_html()
    with open("房价3.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的住宅商品房平均房价(2015-2018)')
    return render_template('house_prices3.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#2009-2019
def timeline2() -> Timeline:
    x = list(df3.地区)
    t2 = Timeline()
    for i in range(2009, 2019):
        c = (
            Line()
                .add_xaxis(x)
                .add_yaxis("住宅商品房平均房价", list(df3["{}年".format(i)]))
                .set_global_opts(title_opts=opts.TitleOpts("{}年各城市住宅商品房平均房价".format(i)),
                                 datazoom_opts=opts.DataZoomOpts(type_="inside"),
                                 visualmap_opts=opts.VisualMapOpts(max_=56000, min_=2811),
                                 yaxis_opts=opts.AxisOpts(max_=56000, min_=2811))
        )
        t2.add(c, "{}年".format(i), )
    return t2

timeline2().render('房价.html')

@app.route('/house_prices',methods=['GET','POST'])
def house_prices() -> 'html':
    data_str = df3.to_html()
    with open("房价.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的住宅商品房平均房价(2009-2019)')
    return render_template('house_prices.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

#总结
df5 = pd.read_csv("pressure.csv",encoding='gbk')

def funnel_label_inside() -> Funnel:
    c = (
        Funnel()
        .add(
            "排名总和",
            [list(z) for z in zip(df5['地区'], df5['排名总和'])],
            label_opts=opts.LabelOpts(position="inside"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="36个主要城市六个维度排名总和"),
                        legend_opts=opts.LegendOpts(type_='scroll',pos_top=25)
                        )
    )
    return c
funnel_label_inside().render('首页.html')

@app.route('/')
@app.route('/entry')
def conclusion() -> 'html':
    data_str = df5.to_html()
    with open("首页.html", encoding="utf8", mode="r") as f:                     # 把"成果.html"當文字檔讀入成字符串
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的生活压力对比分析')
    return render_template('entry.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )

if __name__ == '__main__':
    app.run(debug=True)
