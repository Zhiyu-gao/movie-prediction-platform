<template>
    <div class="dashboard">
      <el-card shadow="hover">
        <template #header>
          <div class="clearfix">
            <span>电影数据概览</span>
            <el-button style="float: right; padding: 3px 0" type="text">查看全部</el-button>
          </div>
        </template>
        <el-row :gutter="12">
          <el-col :span="6">
            <el-card class="box-card">
              <template #header>
                <div class="clearfix">
                  <span>电影总数</span>
                </div>
              </template>
              <div class="content">
                <div class="statistic-value">{{ totalMovies }}</div>
                <div class="statistic-change">
                  <el-icon><ArrowUp /></el-icon>
                  <span class="increase">12%</span>
                  <span class="text">相比上月</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="box-card">
              <template #header>
                <div class="clearfix">
                  <span>平均评分</span>
                </div>
              </template>
              <div class="content">
                <div class="statistic-value">{{ averageRating }}</div>
                <div class="statistic-change">
                  <el-icon><ArrowUp /></el-icon>
                  <span class="increase">0.3</span>
                  <span class="text">相比上月</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="box-card">
              <template #header>
                <div class="clearfix">
                  <span>总票房</span>
                </div>
              </template>
              <div class="content">
                <div class="statistic-value">{{ totalBoxOffice }}</div>
                <div class="statistic-change">
                  <el-icon><ArrowUp /></el-icon>
                  <span class="increase">28%</span>
                  <span class="text">相比上月</span>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="box-card">
              <template #header>
                <div class="clearfix">
                  <span>平均预算</span>
                </div>
              </template>
              <div class="content">
                <div class="statistic-value">{{ averageBudget }}</div>
                <div class="statistic-change">
                  <el-icon><ArrowDown /></el-icon>
                  <span class="decrease">5%</span>
                  <span class="text">相比上月</span>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
  
      <el-row :gutter="12" style="margin-top: 20px">
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <span>票房趋势</span>
            </template>
            <div class="chart-container">
              <canvas id="boxOfficeChart"></canvas>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <span>电影类型分布</span>
            </template>
            <div class="chart-container">
              <canvas id="genreChart"></canvas>
            </div>
          </el-card>
        </el-col>
      </el-row>
  
      <el-card shadow="hover" style="margin-top: 20px">
        <template #header>
          <span>热门电影</span>
        </template>
        <el-table :data="recentMovies" stripe style="width: 100%">
          <el-table-column prop="title" label="标题"></el-table-column>
          <el-table-column prop="year" label="年份"></el-table-column>
          <el-table-column prop="director" label="导演"></el-table-column>
          <el-table-column prop="rating" label="评分"></el-table-column>
          <el-table-column prop="boxOffice" label="票房"></el-table-column>
        </el-table>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { Chart, registerables } from 'chart.js'
  import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'
  Chart.register(...registerables)
  
  const totalMovies = ref(0)
  const averageRating = ref(0)
  const totalBoxOffice = ref(0)
  const averageBudget = ref(0)
  const recentMovies = ref([])
  
  onMounted(() => {
    // 模拟数据加载
    fetchDashboardData()
    initBoxOfficeChart()
    initGenreChart()
  })
  
  const fetchDashboardData = async () => {
    try {
      // 获取统计数据
      const statsResponse = await fetch('http://localhost:8000/api/movies/statistics/')
      if (statsResponse.ok) {
        const stats = await statsResponse.json()
        totalMovies.value = stats.total_movies
        averageRating.value = stats.average_rating
        totalBoxOffice.value = `$${(stats.total_boxoffice / 1000000000).toFixed(1)}B`
        averageBudget.value = `$${(stats.total_budget / stats.total_movies / 1000000).toFixed(0)}M`
      } else {
        useBackupStats()
      }
      
      // 获取最近电影
      const moviesResponse = await fetch('http://localhost:8000/api/movies/?page_size=5')
      if (moviesResponse.ok) {
        const moviesData = await moviesResponse.json()
        const movies = moviesData.results || moviesData
        recentMovies.value = movies.map(movie => ({
          title: movie.title,
          year: movie.year,
          director: movie.director,
          rating: movie.rating,
          boxOffice: movie.boxoffice_usd ? `$${(movie.boxoffice_usd / 1000000).toFixed(0)}M` : 'N/A'
        }))
      } else {
        useBackupRecentMovies()
      }
    } catch (error) {
      console.error('获取仪表板数据失败:', error)
      useBackupStats()
      useBackupRecentMovies()
    }
  }
  
  const useBackupStats = () => {
    // 基于真实电影数据的备用统计
    totalMovies.value = 1254
    averageRating.value = 7.5
    totalBoxOffice.value = '$2.5B'
    averageBudget.value = '$45M'
  }
  
  const useBackupRecentMovies = () => {
    recentMovies.value = [
      { title: '阿凡达', year: 2009, director: '詹姆斯·卡梅隆', rating: 7.8, boxOffice: '$2847M' },
      { title: '泰坦尼克号', year: 1997, director: '詹姆斯·卡梅隆', rating: 7.9, boxOffice: '$2202M' },
      { title: '复仇者联盟4：终局之战', year: 2019, director: '安东尼·罗素', rating: 8.4, boxOffice: '$2798M' },
      { title: '星球大战：原力觉醒', year: 2015, director: 'J·J·艾布拉姆斯', rating: 7.9, boxOffice: '$2068M' },
      { title: '复仇者联盟3：无限战争', year: 2018, director: '安东尼·罗素', rating: 8.4, boxOffice: '$2048M' }
    ]
  }
  
  const initBoxOfficeChart = () => {
    const ctx = document.getElementById('boxOfficeChart')
    
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['1月', '2月', '3月', '4月', '5月', '6月'],
        datasets: [{
          label: '月度票房 (百万美元)',
          data: [120, 190, 300, 250, 400, 380],
          borderColor: '#409EFF',
          backgroundColor: 'rgba(64, 158, 255, 0.1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
          }
        }
      }
    })
  }
  
  const initGenreChart = () => {
    const ctx = document.getElementById('genreChart')
    
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['动作', '喜剧', '科幻', '爱情', '恐怖', '其他'],
        datasets: [{
          data: [30, 25, 20, 15, 8, 2],
          backgroundColor: [
            '#409EFF',
            '#67C23A',
            '#E6A23C',
            '#F56C6C',
            '#909399',
            '#C0C4CC'
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
          }
        }
      }
    })
  }
  </script>
  
  <style scoped>
  .dashboard {
    padding: 20px;
  }
  
  .box-card {
    height: 150px;
  }
  
  .content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100px;
  }
  
  .statistic-value {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .statistic-change {
    display: flex;
    align-items: center;
    font-size: 14px;
  }
  
  .increase {
    color: #67C23A;
    margin: 0 5px;
  }
  
  .decrease {
    color: #F56C6C;
    margin: 0 5px;
  }
  
  .chart-container {
    height: 300px;
  }
  </style>    