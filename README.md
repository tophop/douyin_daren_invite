##  抖音达人批量邀请工具(winddows版)
基本思路：基于python + mitmproxy，使用python调用mitmdump的同时打开浏览器，用户操作浏览器，获取实时 `_signature`,`cookies`,调用达人邀请接口，发送邀请数据
#### 功能(可选)
1. 输入：邀请数量，分类，筛选，排序，过滤，邀请内容
2. 获取邀请成功达人，聚合信息
#### 步骤
##### 1. python基础控制端(daren_script.py)
1. 自动安装mitmproxy证书
2. 启动mitmdump
3. 使用mitmdump proxy server打开浏览器
##### 2. 请求数据保存(daren_filter.py)
1. 基础数据：获取`url`,`_signature`,`cookies`(过滤请求持续获取最新`_signature`)
2. 达人列表接口，筛选key
3. 达人邀请接口
 ##### 3. 发送请求获取数据(daren_query.py)
 1. 达人邀请，包含邀请信息
 2. 获取邀请成功列表：信息整合(入库可选)
 3. 获取筛选达人列表：信息整合(入库可选)
##### 4. Qt界面(进行中)

### 用法(代码版)
1. 部署运行daren_script.py
2. 根据第一步打开的浏览器登录抖店，需要点击的页面：计划管理，达人广场,随意邀请一个达人
3. 在网页达人广场进行初步筛选
4. 执行daren_query.py内方法
    * get_product_list() ：获取计划管理中的产品promotion_id
    * get_author_list(start_page,end_page):获取达人列表
    * author_list_filter(filter, get_author_list),二次筛选
    * invite_post(uid):邀请达人
