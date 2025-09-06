# 电影票房预测平台

这是一个基于真实数据的电影票房预测平台，使用机器学习技术来预测电影票房表现。

## 功能特点

### 🎬 真实数据支持
- 使用真实的电影数据库
- 支持CSV数据导入
- 基于历史电影数据的智能预测

### 🤖 智能预测
- 机器学习模型预测票房
- 多维度特征分析
- 置信度和成功概率评估

### 📊 数据可视化
- 实时统计仪表板
- 票房趋势图表
- 电影类型分布分析

### 🔍 数据管理
- 电影信息CRUD操作
- 高级搜索功能
- 分页显示

## 技术栈

### 后端
- **Django 4.x** - Web框架
- **Django REST Framework** - API框架
- **scikit-learn** - 机器学习库
- **pandas** - 数据处理
- **joblib** - 模型序列化

### 前端
- **Vue 3** - 前端框架
- **Element Plus** - UI组件库
- **Chart.js** - 图表库
- **Vite** - 构建工具

## 快速开始

### 1. 环境准备

确保您已安装：
- Python 3.8+
- Node.js 16+
- 数据库（SQLite/PostgreSQL/MySQL）

### 2. 后端设置

```bash
# 进入后端目录
cd movie_prediction_backend

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 导入数据（如果有CSV文件）
python import_data.py

# 训练预测模型
python train_model.py

# 启动开发服务器
python manage.py runserver
```

### 3. 前端设置

```bash
# 进入前端目录
cd movie-prediction-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- 前端应用: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/api/

## 数据导入

### 方法1: 使用CSV文件

如果您有电影数据的CSV文件，将其命名为 `movie_data.csv` 并放在项目根目录，然后运行：

```bash
cd movie_prediction_backend
python import_data.py
```

### 方法2: 手动添加数据

通过前端界面手动添加电影数据，或使用Django管理界面。

### 方法3: 使用示例数据

如果没有CSV文件，系统会自动创建示例数据。

## API接口

### 电影管理
- `GET /api/movies/` - 获取电影列表
- `POST /api/movies/` - 创建新电影
- `GET /api/movies/{id}/` - 获取单个电影
- `PUT /api/movies/{id}/` - 更新电影
- `DELETE /api/movies/{id}/` - 删除电影
- `GET /api/movies/search/?q={query}` - 搜索电影
- `GET /api/movies/statistics/` - 获取统计数据

### 票房预测
- `POST /api/predict/` - 预测电影票房

## 预测模型

### 特征工程
- 年份 (Year)
- 时长 (Duration)
- 评分 (Rating)
- 投票数 (Votes)
- 获奖数 (Num_Awards)
- 评论数 (Critic_Reviews)
- 衍生特征 (评分投票比、获奖评论比等)

### 算法
- **随机森林回归** - 主要预测算法
- **特征标准化** - 数据预处理
- **交叉验证** - 模型评估

### 预测输出
- 预测票房 (Predicted Box Office)
- 置信度 (Confidence)
- 投资回报率 (ROI)
- 成功概率 (Success Probability)

## 项目结构

```
movie-prediction-platform/
├── movie_prediction_backend/          # Django后端
│   ├── manage.py
│   ├── movie_prediction_backend/      # Django设置
│   │   ├── models.py                  # 数据模型
│   │   ├── views.py                   # API视图
│   │   ├── serializers.py             # 序列化器
│   │   └── urls.py                    # URL配置
│   ├── train_model.py                 # 模型训练脚本
│   ├── import_data.py                 # 数据导入脚本
│   └── requirements.txt               # Python依赖
├── movie-prediction-frontend/         # Vue前端
│   ├── src/
│   │   ├── components/                # Vue组件
│   │   │   ├── Dashboard.vue          # 仪表板
│   │   │   ├── MovieList.vue          # 电影列表
│   │   │   └── MoviePrediction.vue    # 预测界面
│   │   ├── router/                    # 路由配置
│   │   └── main.js                    # 应用入口
│   ├── package.json                   # Node.js依赖
│   └── vite.config.js                 # Vite配置
├── movie_data.csv                     # 电影数据文件
├── movie_prediction_model.pkl         # 训练好的模型
└── README.md                          # 项目说明
```

## 使用指南

### 1. 查看电影数据
- 访问电影列表页面
- 使用搜索功能查找特定电影
- 查看电影详细信息

### 2. 添加新电影
- 点击"新增电影"按钮
- 填写电影信息
- 保存到数据库

### 3. 预测票房
- 进入预测页面
- 输入电影参数
- 点击"预测票房"获取结果
- 查看预测图表和详细分析

### 4. 查看统计
- 访问仪表板查看总体统计
- 分析票房趋势
- 查看电影类型分布

## 模型训练

### 自动训练
系统会在首次启动时自动训练模型，使用数据库中的真实数据。

### 手动训练
```bash
cd movie_prediction_backend
python train_model.py
```

### 模型评估
训练完成后会显示：
- 均方误差 (MSE)
- 决定系数 (R²)
- 平均绝对误差
- 特征重要性排序

## 配置说明

### 数据库配置
在 `movie_prediction_backend/settings.py` 中配置数据库连接。

### API配置
- 默认端口: 8000
- CORS设置: 允许前端跨域访问
- 分页设置: 每页20条记录

### 模型配置
- 算法: RandomForestRegressor
- 树数量: 200
- 最大深度: 15
- 随机种子: 42

## 故障排除

### 常见问题

1. **模型文件不存在**
   - 运行 `python train_model.py` 训练模型

2. **数据库连接失败**
   - 检查数据库配置
   - 运行 `python manage.py migrate`

3. **前端无法连接后端**
   - 检查后端服务是否启动
   - 确认CORS设置正确

4. **预测结果不准确**
   - 检查训练数据质量
   - 重新训练模型
   - 调整特征工程

### 日志查看
```bash
# 查看Django日志
python manage.py runserver --verbosity=2

# 查看模型训练日志
python train_model.py
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或联系开发团队。 "# movie-prediction-platform" 
