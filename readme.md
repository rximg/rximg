# RxImg

RxImg是以响应式数据流为主的一个图像处理工具，可以在一个低代码可视化的界面上搭建图像处理流程。由于引入了响应式的数据流，相对于以往类似的工具RxImg有如下优势。

* 支持更复杂的图像数据流，比如多分枝的，循环的，带条件的。

* 流程可视化

* 低代码

* 可以利用python生态中的各种图像处理，深度学习资源


## pipeline

![image](https://github.com/rximg/rximgimagebed/blob/master/firstdemo.gif?raw=true)

## Quick Start

install python > 3.9

```
pip install rximg
python -m rximg.app
```
open 127.0.0.1:5000 in browser

## 教程
[【RxImg】基于响应式数据流的图像处理新范式](https://zhuanlan.zhihu.com/p/496054199])

[【RxImg】基础概念 快速开始一个最简单的例子](https://zhuanlan.zhihu.com/p/497466246)

[【RxImg】各个模块介绍](https://zhuanlan.zhihu.com/p/498125496)

[【RxImg】低代码玩转PaddleHub的360+深度学习模型](https://zhuanlan.zhihu.com/p/517834251)

## Develop 

install python > 3.9

download release
```
pip install -r requirements.txt
python app.py
```
open another terminal

```
cd frontend
npm run serve
```
open 127.0.0.1:8080 in browser