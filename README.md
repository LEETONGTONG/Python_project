# Python期末项目说明
* [Pythonanywhere](http://leetong.pythonanywhere.com/)

## 各个HTML页面简要介绍
### 此项目网站主题为“36个主要城市的生活压力对比分析”，主要是通过数据表格、数据可视化图表、数据交互更直观、灵活地呈现数据。其共包括9个URL，分别是：
* [entry页面](http://leetong.pythonanywhere.com/)
#### 此页面通过漏斗图、文字说明、数据表格讲述了“36个主要城市的生活压力对比分析”的主题，并设置了一个**下拉选择框**，用户可通过此下拉选择框跳转到具体的各个页面（人均消费支出与平均薪资/人口密度/失业率/住宅商品房平均房价/总结）以查看具体的数据情况。
* [36个主要城市的人均消费支出与平均薪资](http://leetong.pythonanywhere.com/consumption)
#### 此页面通过数据折线图、条形图、数据表格和数据说明展示了36个主要城市的人均消费支出与平均薪资数据情况。(旁边设有按钮跳转到其它页面）
* [36个主要城市的人口密度](http://leetong.pythonanywhere.com/density)
#### 此页面通过数据地图、数据表格和数据说明展示了36个主要城市的人口密度数据情况。(旁边设有按钮跳转到其它页面）
* [36个主要城市的失业率](http://leetong.pythonanywhere.com/unemployment)
#### 此页面通过条形图、数据表格和数据说明展示了36个主要城市的失业率数据情况。(旁边设有按钮跳转到其它页面）
* [36个主要城市的住宅商品房平均房价](http://leetong.pythonanywhere.com/house_prices)
#### 此页面设置了**四个按钮控件**，用户可通过点击这些按钮跳转到不同的页面查看不同年份（2009-2019/2009-2011/2012-2014/2015-2018）对应的数据可视化图、数据表格具体数据情况,默认页面为36个主要城市的住宅商品房平均房价(2009-2019)。(旁边设有按钮跳转到其它页面）

  * [36个主要城市的住宅商品房平均房价(2009-2019)](http://leetong.pythonanywhere.com/house_prices)
  #### 此页面通过折线图（可点击或播放呈现每一年的折线可视化图）、数据表格和数据说明展示了36个主要城市的住宅商品房平均房价(2009-2019)数据情况。
  * [36个主要城市的住宅商品房平均房价(2009-2011)](http://leetong.pythonanywhere.com/house_prices1)
  #### 此页面通过条形图、数据表格和数据说明展示了36个主要城市的住宅商品房平均房价(2009-2011)数据情况。
  * [36个主要城市的住宅商品房平均房价(2012-2014)](http://leetong.pythonanywhere.com/house_prices2)
  #### 此页面通过条形图、数据表格和数据说明展示了36个主要城市的住宅商品房平均房价(2012-2014)数据情况。
  * [36个主要城市的住宅商品房平均房价(2015-2018)](http://leetong.pythonanywhere.com/house_prices3)
  #### 此页面通过条形图、数据表格和数据说明展示了36个主要城市的住宅商品房平均房价(2015-2018)数据情况。

## 数据传递描述
### app.py
#### 引用了pandas/plotly/cufflinks/pyecharts模块
```
import pandas as pd
import plotly as py
import plotly.offline as py
import cufflinks as cf
from pyecharts import options as opts
from pyecharts.charts import Geo,Line,Funnel, Page,Bar, Pie, Timeline
from pyecharts.globals import ChartType, SymbolType
```

#### 读入数据，放上数据图表代码，并实现将其呈现在html页面中。
```df = pd.read_csv("population_density.csv",encoding='gbk')

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
```

#### 前端与后端的相互传值。将csv数据表格生成表单html，读取数据图表的值，返回html/title/数据图表/数据表格。
```
@app.route('/density',methods=['GET','POST'])
def density() -> 'html':
    data_str = df.to_html()
    with open("人口密度.html", encoding="utf8", mode="r") as f:                     
        plot_all = "".join(f.readlines())
    title = ('36个主要城市的人口密度')
    return render_template('density.html',
                           the_title = title,
                           the_res = data_str,
                           the_plot_all = plot_all,
                           )
```

#### 在“36个主要城市的住宅商品房平均房价”页面中，对数据年份进行了分类筛选，使不同页面呈现所对应的年份数据情况。
```
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
```
