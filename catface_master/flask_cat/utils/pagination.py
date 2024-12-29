# -*- coding: utf-8 -*-
# Time : 2024/2/1 15:35
# Author : lirunsheng
# User : l'r's
# Software: PyCharm
# File : pagination.py.py
"""
自定义的分页组件，以后如果想要使用这个分页组件，你需要做如下几件事：

在视图函数中：
    def pretty_list(request):

        # 1.根据自己的情况去筛选自己的数据
        queryset = models.PrettyNum.objects.all()

        # 2.实例化分页对象
        page_object = Pagination(request, queryset)

        context = {
            "queryset": page_object.page_queryset,  # 分完页的数据
            "page_string": page_object.html()       # 生成页码
        }
        return render(request, 'pretty_list.html', context)

在HTML页面中

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        {{ page_string }}
    </ul>

"""
import math
from markupsafe import Markup
from flask import request, render_template_string

class Pagination(object):

    def __init__(self, request, queryset, page_size=3, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """

        import copy
        self.query_dict = request.args.to_dict()
        self.page_param = page_param # 获取分页的参数,在分页组件中是 "page"

        page = self.query_dict.get(page_param, "1")
        #默认值是字符串的1是为了能够支持更多可能的数据类型，
        #可能以后我们封装数据接口的时候不一定是数据类型，
        #所以要把转化为int的工作放在下面的代码中

        if page.isdecimal():
            page = int(page)#转化为int类型
        else:
            page = 1

        self.page = page
        self.page_size = page_size # 每一页记录个数

        self.start = (page - 1) * page_size # 记录开始的区间
        self.end = page * page_size # 记录结束的区间

        self.page_queryset = queryset[self.start:self.end] #获取当前页码的数据

        #total_count = models.PrettyNum.objects.all().count()  # 统计所有数据记录数
        try:
            total_count = queryset.count() # 统计所有数据记录数
        except Exception as e:
            total_count = len(queryset)

        # 页码

        self.plus = 5  # 当前页面 前后几页的数值
        self.total_page= math.ceil(total_count / 3)  # 总共页面数

    def html(self):
        page_str_list = []
        if self.total_page < 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page
        elif self.page < 1 + self.plus:
            start_page = 1
            end_page = self.page + self.plus
        elif self.page + self.plus > self.total_page:
            start_page = self.page - self.plus
            end_page = self.total_page
        else:
            start_page = self.page - self.plus
            end_page = self.page + self.plus

        # Generate page links
        self.query_dict[self.page_param] = "1"
        page_str_list.append(f'<li><a href="?{self._encode_query_dict()}">首页</a></li>')

        # Previous page link
        if self.page <= 1:
            self.query_dict[self.page_param] = "1"
            prev = f'<li><a href="?{self._encode_query_dict()}">上一页</a></li>'
        else:
            self.query_dict[self.page_param] = str(self.page - 1)
            prev = f'<li><a href="?{self._encode_query_dict()}">上一页</a></li>'
        page_str_list.append(prev)

        # Page numbers
        for i in range(start_page, end_page + 1):
            self.query_dict[self.page_param] = str(i)
            if i == self.page:
                ele = f'<li class="active"><a href="?{self._encode_query_dict()}">{i}</a></li>'
            else:
                ele = f'<li><a href="?{self._encode_query_dict()}">{i}</a></li>'
            page_str_list.append(ele)

        # Next page link
        if self.page < self.total_page:
            self.query_dict[self.page_param] = str(self.page + 1)
            next_page = f'<li><a href="?{self._encode_query_dict()}">下一页</a></li>'
        else:
            self.query_dict[self.page_param] = str(self.total_page)
            next_page = f'<li><a href="?{self._encode_query_dict()}">下一页</a></li>'
        page_str_list.append(next_page)

        # Last page link
        self.query_dict[self.page_param] = str(self.total_page)
        page_str_list.append(f'<li><a href="?{self._encode_query_dict()}">尾页</a></li>')

        # Search form for page input
        search_string = '''
            <form method="get">
                <div class="row">
                    <div class="col-md-8">
                        <input type="text" name="page" class="form-control" placeholder="页码">
                    </div>
                    <div class="col-md-4">
                        <button class="btn btn-default" type="submit" style="height: 40px;">跳转</button>
                    </div>
                </div>
            </form>
        '''
        page_str_list.append(search_string)
        page_string = "".join(page_str_list)

        return Markup(page_string)

    def _encode_query_dict(self):
        """Encode the query dictionary into a URL query string."""
        return "&".join([f"{key}={value}" for key, value in self.query_dict.items()])
