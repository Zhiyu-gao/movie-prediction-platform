<template>
    <div class="movie-prediction">
      <el-card shadow="hover">
        <template #header>
          <span>电影票房预测</span>
        </template>
        
        <el-form :model="predictionForm" :rules="rules" ref="predictionFormRef" label-width="120px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="电影标题" prop="title">
                <el-input v-model="predictionForm.title"></el-input>
              </el-form-item>
              <el-form-item label="年份" prop="year">
                <el-input-number v-model="predictionForm.year" :min="2020" :max="new Date().getFullYear() + 5"></el-input-number>
              </el-form-item>
              <el-form-item label="导演" prop="director">
                <el-input v-model="predictionForm.director"></el-input>
              </el-form-item>
              <el-form-item label="时长(分钟)" prop="duration">
                <el-input-number v-model="predictionForm.duration" :min="60" :max="300"></el-input-number>
              </el-form-item>
              <el-form-item label="类型" prop="genre">
                <el-select v-model="predictionForm.genre" placeholder="请选择电影类型">
                  <el-option v-for="genre in genres" :key="genre" :label="genre" :value="genre"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="内容分级" prop="contentRating">
                <el-select v-model="predictionForm.contentRating" placeholder="请选择内容分级">
                  <el-option v-for="rating in contentRatings" :key="rating" :label="rating" :value="rating"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="主演" prop="leadActor">
                <el-input v-model="predictionForm.leadActor"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="预算(美元)" prop="budget">
                <el-input-number v-model="predictionForm.budget" :min="1000000" :max="500000000"></el-input-number>
              </el-form-item>
              <el-form-item label="预期评分" prop="rating">
                <el-rate v-model="predictionForm.rating" show-text></el-rate>
              </el-form-item>
              <el-form-item label="预期票数" prop="votes">
                <el-input-number v-model="predictionForm.votes" :min="1000" :max="1000000"></el-input-number>
              </el-form-item>
              <el-form-item label="语言" prop="language">
                <el-input v-model="predictionForm.language"></el-input>
              </el-form-item>
              <el-form-item label="国家" prop="country">
                <el-input v-model="predictionForm.country"></el-input>
              </el-form-item>
              <el-form-item label="制作公司" prop="productionCompany">
                <el-input v-model="predictionForm.productionCompany"></el-input>
              </el-form-item>
              <el-form-item label="预期获奖数" prop="numAwards">
                <el-input-number v-model="predictionForm.numAwards" :min="0" :max="50"></el-input-number>
              </el-form-item>
              <el-form-item label="影评数" prop="criticReviews">
                <el-input-number v-model="predictionForm.criticReviews" :min="0" :max="10000"></el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-form-item>
            <el-button type="primary" @click="predictBoxOffice">预测票房</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 预测结果卡片 -->
      <el-card v-if="predictionResult" shadow="hover" style="margin-top: 20px">
        <template #header>
          <span>预测结果</span>
        </template>
        
        <div class="result-container">
          <div class="prediction-value">
            <div class="label">预测票房:</div>
            <div class="value">${{ predictionResult.predicted_boxoffice.toLocaleString('en-US') }}</div>
          </div>
          
          <div class="prediction-details">
            <div class="detail-item">
              <div class="detail-label">置信度:</div>
              <div class="detail-value">{{ predictionResult.confidence.toFixed(2) }}%</div>
            </div>
            <div class="detail-item">
              <div class="detail-label">投资回报率(ROI):</div>
              <div class="detail-value">{{ predictionResult.roi.toFixed(2) }}%</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, toRefs } from 'vue'
  import { Chart, registerables } from 'chart.js'
  Chart.register(...registerables)
  
  const state = reactive({
    predictionForm: {
      title: '',
      year: new Date().getFullYear(),
      director: '',
      duration: 120,
      genre: 'Action',
      contentRating: 'PG-13',
      leadActor: '',
      budget: 100000000,
      rating: 7.5,
      votes: 500000,
      language: 'English',
      country: 'USA',
      productionCompany: '',
      numAwards: 0,
      criticReviews: 100
    },
    rules: {
      title: [
        { required: true, message: '请输入电影标题', trigger: 'blur' }
      ],
      year: [
        { required: true, message: '请输入电影年份', trigger: 'blur' },
        { type: 'number', message: '年份必须为数字值', trigger: 'blur' }
      ],
      director: [
        { required: true, message: '请输入导演', trigger: 'blur' }
      ],
      genre: [
        { required: true, message: '请选择电影类型', trigger: 'change' }
      ],
      budget: [
        { required: true, message: '请输入预算', trigger: 'blur' },
        { type: 'number', message: '预算必须为数字值', trigger: 'blur' }
      ],
      criticReviews: [
        { required: true, message: '请输入影评数', trigger: 'blur' },
        { type: 'number', message: '影评数必须为数字值', trigger: 'blur' }
      ]
    },
    predictionFormRef: null,
    genres: ['Action', 'Comedy', 'Drama', 'Romance', 'Thriller', 'Horror', 'Fantasy'],
    contentRatings: ['G', 'PG', 'PG-13', 'R', 'NC-17', 'TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA'],
    predictionResult: null
  })
  
  const {
    predictionForm,
    rules,
    predictionFormRef,
    genres,
    contentRatings,
    predictionResult
  } = toRefs(state)
  
  const predictBoxOffice = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: predictionForm.value.title,
          year: predictionForm.value.year,
          director: predictionForm.value.director,
          duration: predictionForm.value.duration,
          genre: predictionForm.value.genre,
          content_rating: predictionForm.value.contentRating,
          lead_actor: predictionForm.value.leadActor,
          budget: predictionForm.value.budget ? predictionForm.value.budget.toFixed(2) : '0.00',
          rating: predictionForm.value.rating,
          votes: predictionForm.value.votes,
          language: predictionForm.value.language,
          country: predictionForm.value.country,
          production_company: predictionForm.value.productionCompany,
          num_awards: predictionForm.value.numAwards,
          critic_reviews: predictionForm.value.criticReviews
        })
      })
      
      if (response.ok) {
        const result = await response.json()
        predictionResult.value = {
          predicted_boxoffice: result.predicted_boxoffice,
          confidence: result.confidence,
          roi: result.roi
        }
        console.log(predictionResult)
      } else {
        predictionResult.value = null
      }
    } catch (error) {
      predictionResult.value = null
    }
  }
  
  const resetForm = () => {
    // 重置表单
    predictionForm.value = {
      title: '',
      year: new Date().getFullYear(),
      director: '',
      duration: 120,
      genre: 'Action',
      contentRating: 'PG-13',
      leadActor: '',
      budget: 100000000,
      rating: 7.5,
      votes: 500000,
      language: 'English',
      country: 'USA',
      productionCompany: '',
      numAwards: 0,
      criticReviews: 100
    }
    
    predictionResult.value = null
  }
  
  const createPredictionChart = () => {
    const ctx = document.getElementById('predictionChart')
    
    // 销毁现有图表
    if (window.predictionChartInstance) {
      window.predictionChartInstance.destroy()
    }
    
    // 创建新图表
    window.predictionChartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['预算', '预测票房', '高估计', '低估计'],
        datasets: [{
          label: '金额 (美元)',
          data: [
            predictionForm.value.budget,
            predictionResult.value.boxOffice,
            Math.floor(predictionResult.value.boxOffice * 1.3),
            Math.floor(predictionResult.value.boxOffice * 0.7)
          ],
          backgroundColor: [
            '#909399',  // 预算 - 灰色
            '#409EFF',  // 预测票房 - 蓝色
            '#67C23A',  // 高估计 - 绿色
            '#F56C6C'   // 低估计 - 红色
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return '$' + context.raw.toLocaleString('en-US')
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + value.toLocaleString('en-US');
              }
            }
          }
        }
      }
    })
  }
  </script>
  
  <style scoped>
  .movie-prediction {
    padding: 20px;
  }
  
  .result-container {
    padding: 20px;
  }
  
  .prediction-value {
    text-align: center;
    margin-bottom: 30px;
  }
  
  .value {
    font-size: 36px;
    font-weight: bold;
    color: #409EFF;
  }
  
  .prediction-details {
    display: flex;
    justify-content: space-around;
    margin-bottom: 30px;
  }
  
  .detail-item {
    text-align: center;
  }
  
  .detail-label {
    font-size: 14px;
    color: #909399;
  }
  
  .detail-value {
    font-size: 24px;
    font-weight: bold;
    margin-top: 5px;
  }
  
  .prediction-chart {
    height: 300px;
  }
  </style>    