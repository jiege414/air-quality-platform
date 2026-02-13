# 空气质量数据可视化分析平台

## 项目简介

本项目是一个基于B/S架构的空气质量数据可视化分析平台，旨在通过自动化采集多源数据，构建一个集中、直观的空气质量信息中心，为环境感知与健康出行提供数据支持。

## 技术栈

### 前端
- **Vue.js 2.x** - 前端框架
- **Element UI** - UI组件库
- **ECharts 5.x** - 数据可视化图表库
- **Axios** - HTTP请求库

### 后端
- **SpringBoot 2.7.x** - 后端框架
- **MyBatis-Plus** - ORM框架
- **Quartz** - 定时任务调度
- **MySQL 8.0** - 关系型数据库
- **Redis** - 缓存数据库

### 数据采集
- **Python 3.x** - 爬虫开发
- **Requests** - HTTP请求
- **BeautifulSoup4** - HTML解析
- **Pandas/NumPy** - 数据处理
- **Statsmodels** - ARIMA时间序列预测

## 环境要求

### 必需软件
| 软件 | 版本 | 下载地址 |
|------|------|----------|
| Java JDK | 1.8+ | https://adoptium.net/zh-CN/temurin/releases/?version=8 |
| MySQL | 8.0+ | https://dev.mysql.com/downloads/installer/ |
| Node.js | 18.x+ | https://nodejs.org/ |
| Python | 3.8+ | https://www.python.org/downloads/ |
| Maven | 3.6+（可选，项目已包含Maven Wrapper） |

### 推荐配置
- **操作系统**：Windows 10/11 或 Linux/macOS
- **内存**：8GB+
- **磁盘空间**：10GB+

## 项目结构

```
Air quality/
├── backend/                    # SpringBoot后端项目
│   ├── src/main/java/com/cugb/
│   │   ├── AirQualityApplication.java
│   │   ├── common/            # 通用类
│   │   ├── config/            # 配置类
│   │   ├── controller/        # 控制器
│   │   ├── entity/            # 实体类
│   │   ├── mapper/            # MyBatis映射器
│   │   └── service/           # 业务逻辑
│   ├── src/main/resources/
│   │   └── application.yml    # 配置文件
│   └── pom.xml                # Maven配置
├── frontend/                   # Vue.js前端项目
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── router/            # 路由配置
│   │   ├── store/             # Vuex状态管理
│   │   └── App.vue            # 根组件
│   └── package.json
├── spider/                     # Python爬虫项目
│   ├── air_quality_spider.py  # 空气质量爬虫
│   ├── prediction.py          # ARIMA预测模块
│   ├── scheduler.py           # 定时任务调度
│   ├── database.py            # 数据库连接
│   └── config.py              # 配置文件
└── database/
    ├── init.sql               # 数据库初始化脚本（表结构+数据）
    ├── tables.sql             # 仅表结构
    └── data.sql               # 仅数据
```

## 首次运行详细步骤

### 第一步：数据库初始化

1. **安装 MySQL 8.0**
   - 下载 MySQL Installer：https://dev.mysql.com/downloads/installer/
   - 选择 "Server only" 安装类型
   - 设置 root 密码（记住密码，后续需要用到）
   - 完成安装

2. **执行初始化脚本**

   **方式一：使用 MySQL 命令行（推荐）**
   ```bash
   # 进入 MySQL（需要输入密码）
   "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
   
   # 在 MySQL 命令行中执行
   source C:/Users/chuanjie.song/Desktop/空气质量数据可视化分析平台/Air quality/database/init.sql
   ```

   **方式二：使用 MySQL Workbench**
   - 打开 MySQL Workbench
   - 连接到本地 MySQL 服务器
   - 打开 `database/init.sql` 文件
   - 执行脚本

3. **验证数据库**
   ```sql
   USE air_quality;
   SHOW TABLES;
   SELECT * FROM city;
   ```
   预期输出：4 张表（city, air_quality, air_quality_realtime, warning_record）和 20 个城市记录

### 第二步：启动后端服务

1. **安装 Java JDK 8**
   - 下载 Eclipse Temurin JDK 8：https://adoptium.net/zh-CN/temurin/releases/?version=8
   - 下载 `.msi` 安装包并安装
   - 记住安装路径（如：`C:\Program Files\Eclipse Adoptium\jdk-8.xxx`）

2. **启动 SpringBoot 服务**

   **方式一：使用 Maven Wrapper（推荐，无需单独安装 Maven）**
   ```bash
   cd backend
   
   # Windows PowerShell
   $env:JAVA_HOME="C:\Users\你的用户名\AppData\Local\Programs\Eclipse Adoptium\jdk-8.xxx-hotspot"
   $env:Path="$env:JAVA_HOME\bin;$env:Path"
   .\mvnw.cmd spring-boot:run
   
   # CMD
   set JAVA_HOME=C:\Users\你的用户名\AppData\Local\Programs\Eclipse Adoptium\jdk-8.xxx-hotspot
   set PATH=%JAVA_HOME%\bin;%PATH%
   mvnw.cmd spring-boot:run
   ```

   **方式二：使用已安装的 Maven**
   ```bash
   cd backend
   mvn spring-boot:run
   ```

3. **验证后端启动**
   - 访问 http://localhost:8080
   - 预期输出：Whitelabel Error Page（表示服务已启动，但没有默认页面）
   - 访问 http://localhost:8080/api/city/list
   - 预期输出：JSON 格式的城市列表数据

### 第三步：启动前端服务

1. **安装 Node.js 18+**
   - 下载：https://nodejs.org/dist/v18.19.0/node-v18.19.0-x64.msi
   - 双击安装，保持默认选项
   - 安装完成后重启终端

2. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```
   注意：首次安装可能需要 2-5 分钟，请耐心等待

3. **启动前端开发服务器**
   ```bash
   npm run serve
   ```

4. **验证前端启动**
   - 访问 http://localhost:3000
   - 预期输出：空气质量数据可视化分析平台首页

### 第四步：运行 Python 爬虫（可选）

1. **安装 Python 依赖**
   ```bash
   cd spider
   pip install -r requirements.txt
   ```

2. **运行爬虫**
   ```bash
   # 一次性爬取数据
   python air_quality_spider.py
   
   # 启动定时调度器（每小时自动爬取）
   python scheduler.py
   ```

## 常见问题及解决方案

### 问题 1：MySQL 命令无法识别
**错误信息**：
```
mysql : 无法将"mysql"项识别为 cmdlet、函数、脚本文件或可运行程序的名称
```

**解决方案**：
使用 MySQL 的完整路径：
```bash
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

### 问题 2：数据库字符编码错误
**错误信息**：
```
ERROR 1366 (HY000): Incorrect string value: '\xE5\x8C\x97\xE4\xBA\xAC' for column 'city_name'
```

**解决方案**：
1. 确保使用 `utf8mb4` 字符集
2. 使用项目提供的分离脚本：
   - 先执行 `database/tables.sql` 创建表结构
   - 再执行 `database/data.sql` 插入数据（使用英文城市名避免编码问题）

### 问题 3：Java 环境变量未配置
**错误信息**：
```
Error: JAVA_HOME not found in your environment
```

**解决方案**：
在 PowerShell 中临时设置：
```bash
$env:JAVA_HOME="C:\Users\你的用户名\AppData\Local\Programs\Eclipse Adoptium\jdk-8.xxx-hotspot"
$env:Path="$env:JAVA_HOME\bin;$env:Path"
```

永久设置（推荐）：
1. 右键 "此电脑" → "属性" → "高级系统设置"
2. 点击 "环境变量"
3. 新建系统变量 `JAVA_HOME`，值为 JDK 安装路径
4. 编辑 `Path` 变量，添加 `%JAVA_HOME%\bin`

### 问题 4：Maven 命令无法识别
**错误信息**：
```
mvn : 无法将"mvn"项识别为 cmdlet
```

**解决方案**：
使用项目自带的 Maven Wrapper：
```bash
.\mvnw.cmd spring-boot:run
```

### 问题 5：依赖下载失败
**错误信息**：
```
Could not find artifact com.alibaba:fastjson2:jar:2.0.40
```

**解决方案**：
已修复，项目使用正确的 groupId：`com.alibaba.fastjson2`

### 问题 6：npm install 权限错误
**错误信息**：
```
npm ERR! code EPERM
npm ERR! syscall rmdir
```

**解决方案**：
```bash
# 清除缓存后重新安装
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install --ignore-scripts
```

### 问题 7：yorkie 安装失败
**错误信息**：
```
npm ERR! command failed: node bin/install.js
```

**解决方案**：
已在 `package.json` 中添加 `"gitHooks": {}` 跳过 git hooks 安装

## 预期输出结果

### 后端启动成功
```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::               (v2.7.14)

2026-02-13 16:05:16.967  INFO 41972 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2026-02-13 16:05:17.790  INFO 41972 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port(s): 8080 (http) with context path ''
2026-02-13 16:05:17.795  INFO 41972 --- [           main] com.cugb.AirQualityApplication           : Started AirQualityApplication in 1.736 seconds (JVM running for 1.936)
```

### 前端启动成功
```
 DONE  Compiled successfully in 3492ms

  App running at:
  - Local:   http://localhost:3000/
  - Network: unavailable

  Note that the development build is not optimized.
  To create a production build, run npm run build.
```

## 功能模块说明

### 1. 数据概览（Dashboard）
- **功能**：展示关键统计数据和实时排名
- **图表**：
  - AQI 最差 TOP10 城市条形图
  - AQI 最优 TOP10 城市条形图
- **统计卡片**：监测城市数、平均 AQI、预警数量等

### 2. 城市排名（Ranking）
- **功能**：全国城市 AQI 实时排名
- **操作**：
  - 切换查看最差/最优排名
  - 查看详细数据表格
- **数据**：AQI、PM2.5、PM10、SO2、NO2、CO、O3

### 3. 历史查询（History）
- **功能**：查询城市历史空气质量数据
- **操作**：
  - 选择城市和日期范围
  - 生成 AQI 变化趋势折线图
  - 查看污染物浓度变化
- **时间范围**：近一周、近一月、近一年

### 4. 数据对比（Compare）
- **功能**：多城市空气质量对比分析
- **操作**：
  - 选择 2-5 个城市进行对比
  - 多城市 AQI 对比折线图
  - 对比统计分析

### 5. 预警信息（Warning）
- **功能**：空气质量预警管理
- **算法**：ARIMA 时间序列预测
- **操作**：
  - 查看未处理预警
  - 手动运行预测
  - 处理预警记录
- **预警等级**：
  - 🟢 优 (0-50)
  - 🟡 良 (51-100)
  - 🟠 轻度污染 (101-150)
  - 🔴 中度污染 (151-200)
  - 🟣 重度污染 (201-300)
  - ⚫ 严重污染 (>300)

## API 接口文档

### 城市相关接口
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/city/list` | 获取所有城市列表 |
| GET | `/api/city/{cityCode}` | 获取指定城市信息 |

### 空气质量数据接口
| 方法 | 接口 | 参数 | 说明 |
|------|------|------|------|
| GET | `/api/air-quality/history` | cityCode, startDate, endDate | 获取历史数据 |
| GET | `/api/air-quality/ranking` | type(worst/best), limit | 获取城市排名 |
| POST | `/api/air-quality/compare` | cityCodes, startDate, endDate | 对比多个城市 |

### 实时数据接口
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/air-quality-realtime/ranking` | 获取实时排名 |
| GET | `/api/air-quality-realtime/list` | 获取所有实时数据 |

### 预警接口
| 方法 | 接口 | 参数 | 说明 |
|------|------|------|------|
| GET | `/api/warning/unhandled` | - | 获取未处理预警 |
| POST | `/api/warning/predict` | - | 运行预测 |
| POST | `/api/warning/handle/{warningId}` | - | 处理预警 |

## 日常启动指南（已配置环境后）

当你已经完成首次环境配置后，日常使用只需以下步骤：

### 1. 启动 MySQL 服务（如未开机自启）

**Windows PowerShell：**
```powershell
# 检查 MySQL 服务状态
Get-Service MySQL80

# 启动服务（如果未运行）
Start-Service MySQL80

# 停止服务
Stop-Service MySQL80
```

**验证 MySQL 连接：**
```powershell
mysql -u root -p123456
```

### 2. 启动后端服务（SpringBoot）

**方式一：使用 Maven Wrapper（推荐）**
```powershell
cd backend
.\mvnw.cmd spring-boot:run
```

**方式二：使用已安装的 Maven**
```powershell
cd backend
mvn spring-boot:run
```

**预期输出：**
```
Tomcat started on port(s): 8080 (http)
Started AirQualityApplication in x.x seconds
```

**后端访问地址：**
- 首页：http://localhost:8080
- API 测试：http://localhost:8080/api/city/list

### 3. 启动前端服务（Vue.js）

```powershell
cd frontend
npm run serve
```

**预期输出：**
```
DONE  Compiled successfully in xxxxms

App running at:
- Local:   http://localhost:3000/
- Network: unavailable
```

**前端访问地址：** http://localhost:3000

### 4. 启动 Python 爬虫（可选）

如果你需要获取实时空气质量数据：

```powershell
# 进入项目根目录，激活虚拟环境
.\venv\Scripts\activate

# 进入爬虫目录
cd spider

# 运行爬虫调度器（自动定时爬取）
python scheduler.py

# 或运行一次性爬虫
python air_quality_spider.py
```

---

## 服务访问汇总

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端页面 | http://localhost:3000/ | 数据可视化界面 |
| 后端 API | http://localhost:8080/ | RESTful API 服务 |
| 城市列表 API | http://localhost:8080/api/city/list | 获取所有城市 |
| MySQL | localhost:3306 | 数据库服务 |

---

## 快速验证项目运行状态

### 验证后端服务
在浏览器中访问：http://localhost:8080/api/city/list

**预期返回：**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {"cityCode": "110000", "cityName": "北京", "province": "北京市"},
    {"cityCode": "310000", "cityName": "上海", "province": "上海市"},
    ...
  ]
}
```

### 验证前端页面
在浏览器中访问：http://localhost:3000

**预期看到：**
- 顶部导航栏（数据概览、城市排名、历史查询、数据对比、预警信息）
- 数据概览页面，包含统计卡片和图表

---

## 停止服务

### 停止前端服务
在运行前端服务的终端中按 `Ctrl + C`，然后输入 `Y` 确认。

### 停止后端服务
在运行后端服务的终端中按 `Ctrl + C`。

### 停止 Python 爬虫
在运行爬虫的终端中按 `Ctrl + C`。

---

## 常见问题快速解决

### 问题 1：端口被占用

**错误信息：**
```
Port 8080 was already in use
```

**解决方案：**
```powershell
# 查找占用 8080 端口的进程
netstat -ano | findstr :8080

# 结束进程（将 <PID> 替换为实际进程 ID）
taskkill /PID <PID> /F
```

### 问题 2：后端无法连接数据库

**错误信息：**
```
Communications link failure
```

**解决方案：**
1. 确认 MySQL 服务已启动
2. 检查 `backend/src/main/resources/application.yml` 中的数据库密码是否正确
3. 确认数据库 `air_quality` 已创建

### 问题 3：前端无法连接后端

**错误信息：**
```
Proxy error: Could not proxy request
```

**解决方案：**
1. 确认后端服务已启动（http://localhost:8080 可访问）
2. 检查 `frontend/vue.config.js` 中的代理配置
3. 尝试直接访问后端 API 测试

### 问题 4：Python 爬虫依赖缺失

**错误信息：**
```
ModuleNotFoundError: No module named 'requests'
```

**解决方案：**
```powershell
# 激活虚拟环境
.\venv\Scripts\activate

# 重新安装依赖
pip install -r spider/requirements.txt
```

---

## 数据更新和维护

### 自动数据更新
爬虫调度器已配置定时任务：
- **每 2 小时**：获取实时空气质量数据
- **每天 02:00**：获取历史数据
- **每天 06:00**：运行 ARIMA 预测并生成预警

### 手动数据更新
```powershell
# 激活虚拟环境
.\venv\Scripts\activate

cd spider

# 手动运行爬虫
python air_quality_spider.py

# 手动运行预测
python prediction.py
```

### 查看数据库数据
```sql
-- 查看城市列表
SELECT * FROM city;

-- 查看实时数据
SELECT * FROM air_quality_realtime ORDER BY aqi DESC;

-- 查看历史数据（最近7天）
SELECT * FROM air_quality 
WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
ORDER BY date DESC, aqi DESC;

-- 查看预警记录
SELECT * FROM warning_record WHERE is_handled = 0;
```

---

## 生产环境部署

### 后端打包部署
```powershell
cd backend

# 打包
mvn clean package

# 运行打包后的 jar 包
java -jar target/air-quality-platform-1.0.0.jar
```

### 前端打包部署
```powershell
cd frontend

# 打包（生成 dist 目录）
npm run build

# 将 dist 目录部署到 Nginx 或 Apache
```

### 注意事项
- 爬虫每小时自动采集最新数据
- 手动运行爬虫：`python spider/air_quality_spider.py`
- 手动运行预测：`python spider/prediction.py`

### 生产环境部署
1. **后端打包**：
   ```bash
   cd backend
   mvn clean package
   java -jar target/air-quality-platform-1.0.0.jar
   ```

2. **前端打包**：
   ```bash
   cd frontend
   npm run build
   ```
   将 `dist` 目录部署到 Nginx 或 Apache

### 注意事项
- 首次启动需要下载大量依赖，请确保网络畅通
- 数据库字符集使用 `utf8mb4` 以支持中文
- 爬虫需要连接互联网才能获取数据
- 预测功能需要至少 7 天的历史数据

## 开发团队

- **学校**：中国地质大学（北京）
- **专业**：软件工程
- **作者**：宋传杰
- **学号**：1004226121
- **导师**：曾姗


## 更新日志

### 2026-02-13
- ✅ 完成项目初始化
- ✅ 修复 fastjson2 依赖问题
- ✅ 修复数据库字符编码问题
- ✅ 完善 README 文档
- ✅ 添加常见问题解决方案
