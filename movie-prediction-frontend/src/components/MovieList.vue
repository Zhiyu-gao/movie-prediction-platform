<template>
    <div class="movie-list">
      <el-card shadow="hover">
        <template #header>
          <div class="clearfix">
            <span>电影管理</span>
            <el-button style="float: right" type="primary" @click="handleCreate">
              <el-icon><Plus /></el-icon>新增电影
            </el-button>
          </div>
        </template>
        
        <el-input v-model="searchQuery" placeholder="搜索电影标题" clearable @clear="fetchMovies">
          <template #suffix>
            <el-button @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
        
        <el-table :data="movies" stripe border style="width: 100%; margin-top: 20px">
          <el-table-column prop="title" label="标题" width="150"></el-table-column>
          <el-table-column prop="year" label="年份" width="80"></el-table-column>
          <el-table-column prop="director" label="导演" width="120"></el-table-column>
          <el-table-column prop="duration" label="时长" width="80"></el-table-column>
          <el-table-column prop="votes" label="投票数量" width="120"></el-table-column>
          <el-table-column prop="description" label="描述" width="120"></el-table-column>
          <el-table-column prop="language" label="语言" width="120"></el-table-column>
          <el-table-column prop="country" label="国家" width="120"></el-table-column>
          <el-table-column prop="budget_usd" label="预算" width="120"></el-table-column>
          <el-table-column prop="genre" label="类别" width="120"></el-table-column>
          <el-table-column prop="production_company" label="制作公司" width="120"></el-table-column>
          <el-table-column prop="content_rating" label="内容分级" width="120"></el-table-column>
          <el-table-column prop="lead_actor" label="主演" width="120"></el-table-column>
          <el-table-column prop="num_awards" label="获奖数" width="120"></el-table-column>
          <el-table-column prop="critic_reviews" label="评论数" width="120"></el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button size="small" type="primary" @click="handleEdit(scope.row)">
                <el-icon><Edit /></el-icon>编辑
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">
                <el-icon><Delete /></el-icon>删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 30, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </el-card>
      
      <!-- 新增/编辑电影对话框 -->
      <el-dialog v-model="dialogVisible" title="电影信息">
        <template #default>
          <el-form :model="movieForm" :rules="rules" ref="formRef" label-width="120px">
            <el-form-item label="标题" prop="title">
              <el-input v-model="movieForm.title"></el-input>
            </el-form-item>
            <el-form-item label="年份" prop="year">
              <el-input-number v-model="movieForm.year" :min="1900" :max="new Date().getFullYear()"></el-input-number>
            </el-form-item>
            <el-form-item label="导演" prop="director">
              <el-input v-model="movieForm.director"></el-input>
            </el-form-item>
            <el-form-item label="时长(分钟)" prop="duration">
              <el-input-number v-model="movieForm.duration" :min="1"></el-input-number>
            </el-form-item>
            <el-form-item label="评分" prop="rating">
              <el-rate v-model="movieForm.rating" show-text></el-rate>
            </el-form-item>
            <el-form-item label="票数" prop="votes">
              <el-input-number v-model="movieForm.votes" :min="0"></el-input-number>
            </el-form-item>
            <el-form-item label="描述" prop="description">
              <el-input type="textarea" v-model="movieForm.description" :rows="4"></el-input>
            </el-form-item>
            <el-form-item label="语言" prop="language">
              <el-input v-model="movieForm.language"></el-input>
            </el-form-item>
            <el-form-item label="国家" prop="country">
              <el-input v-model="movieForm.country"></el-input>
            </el-form-item>
            <el-form-item label="预算(美元)" prop="budget_usd">
              <el-input-number v-model="movieForm.budget_usd" :min="0"></el-input-number>
            </el-form-item>
            <el-form-item label="票房(美元)" prop="boxOffice">
              <el-input-number v-model="movieForm.boxOffice" :min="0"></el-input-number>
            </el-form-item>
            <el-form-item label="类型" prop="genre">
              <el-input v-model="movieForm.genre"></el-input>
            </el-form-item>
            <el-form-item label="制作公司" prop="production_company">
              <el-input v-model="movieForm.production_company"></el-input>
            </el-form-item>
            <el-form-item label="内容分级" prop="content_rating">
              <el-input v-model="movieForm.content_rating"></el-input>
            </el-form-item>
            <el-form-item label="主演" prop="lead_actor">
              <el-input v-model="movieForm.lead_actor"></el-input>
            </el-form-item>
            <el-form-item label="获奖数" prop="num_awards">
              <el-input-number v-model="movieForm.num_awards" :min="0"></el-input-number>
            </el-form-item>
            <el-form-item label="评论数" prop="critic_reviews">
              <el-input-number v-model="movieForm.critic_reviews" :min="0"></el-input-number>
            </el-form-item>
          </el-form>
        </template>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </template>
      </el-dialog>
      
      <!-- 删除确认对话框 -->
      <el-dialog
        title="确认删除"
        v-model="deleteDialogVisible"
        width="30%">
        <template #default>
          <p>确定要删除电影 "{{ deleteMovieTitle }}" 吗？</p>
        </template>
        <template #footer>
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete">确定</el-button>
        </template>
      </el-dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, toRefs } from 'vue'
  import { Plus, Edit, Delete, Search} from '@element-plus/icons-vue'
  import { ElNotification } from 'element-plus'; // 通知组件

  const loading = ref(false);
  
  const state = reactive({
    movies: [],
    currentPage: 1,
    pageSize: 10,
    total: 0,
    searchQuery: '',
    dialogVisible: false,
    deleteDialogVisible: false,
    loadingDelete: false, // 删除操作的加载状态
    movieForm: {
      id: null,
      title: '',
      year: null,
      director: '',
      duration: null,
      rating: 0,
      votes: 0,
      description: '',
      language: '',
      country: '',
      budget_usd: 0,
      boxOffice: 0,
      genre: '',
      production_company: '',
      content_rating: '',
      lead_actor: '',
      num_awards: 0,
      critic_reviews: 0
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
      rating: [
        { required: true, message: '请输入评分', trigger: 'blur' }
      ]
    },
    formRef: null,
    deleteMovieId: null,
    deleteMovieTitle: ''
  })
  
  const {
    movies,
    currentPage,
    pageSize,
    total,
    searchQuery,
    dialogVisible,
    deleteDialogVisible,
    movieForm,
    rules,
    formRef,
    deleteMovieId,
    deleteMovieTitle
  } = toRefs(state)
  
  onMounted(() => {
    fetchMovies()
  })
  
  const fetchMovies = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/movies/?page=${currentPage.value}&page_size=${pageSize.value}`)
      if (response.ok) {
        const data = await response.json()
        movies.value = data.results || data
        total.value = data.count || data.length
      } else {
        console.error('获取电影列表失败')
        // 如果API失败，使用备用数据
        useBackupData()
      }
    } catch (error) {
      console.error('API调用错误:', error)
      useBackupData()
    }
  }
  
  const useBackupData = () => {
    // 备用数据，基于真实电影信息
    const backupMovies = [
      {
        id: 1,
        title: '阿凡达',
        year: 2009,
        director: '詹姆斯·卡梅隆',
        duration: 162,
        rating: 7.8,
        votes: 1200000,
        description: '潘多拉星球上的科幻冒险',
        language: '英语',
        country: '美国',
        budget_usd: 237000000,
        boxoffice_usd: 2847246203,
        genre: '科幻',
        production_company: '20世纪福克斯',
        content_rating: 'PG-13',
        lead_actor: '萨姆·沃辛顿',
        num_awards: 3,
        critic_reviews: 350
      },
      {
        id: 2,
        title: '泰坦尼克号',
        year: 1997,
        director: '詹姆斯·卡梅隆',
        duration: 194,
        rating: 7.9,
        votes: 1100000,
        description: '1912年泰坦尼克号沉船的爱情故事',
        language: '英语',
        country: '美国',
        budget_usd: 200000000,
        boxoffice_usd: 2201647264,
        genre: '爱情',
        production_company: '派拉蒙影业',
        content_rating: 'PG-13',
        lead_actor: '莱昂纳多·迪卡普里奥',
        num_awards: 11,
        critic_reviews: 280
      },
      {
        id: 3,
        title: '复仇者联盟4：终局之战',
        year: 2019,
        director: '安东尼·罗素',
        duration: 181,
        rating: 8.4,
        votes: 1000000,
        description: '漫威超级英雄的终极集结',
        language: '英语',
        country: '美国',
        budget_usd: 356000000,
        boxoffice_usd: 2797501328,
        genre: '动作',
        production_company: '漫威影业',
        content_rating: 'PG-13',
        lead_actor: '小罗伯特·唐尼',
        num_awards: 1,
        critic_reviews: 450
      }
    ]
    
    movies.value = backupMovies
    total.value = backupMovies.length
  }
  
  const handleSizeChange = (newSize) => {
    pageSize.value = newSize
    fetchMovies()
  }
  
  const handleCurrentChange = (newPage) => {
    currentPage.value = newPage
    fetchMovies()
  }
  
  const handleSearch = async () => {
    if (searchQuery.value.trim()) {
      try {
        const response = await fetch(`http://localhost:8000/api/movies/search/?q=${encodeURIComponent(searchQuery.value)}`)
        if (response.ok) {
          const data = await response.json()
          movies.value = data.results || data
          total.value = data.count || data.length
        } else {
          console.error('搜索失败')
          fetchMovies()
        }
      } catch (error) {
        console.error('搜索API错误:', error)
        fetchMovies()
      }
    } else {
      fetchMovies()
    }
  }
  
  const handleCreate = () => {
    // 重置表单
    for (const key in movieForm.value) {
      if (key !== 'id') {
        movieForm.value[key] = ''
      }
    }
    movieForm.value.id = null
    dialogVisible.value = true
  }
  
  const handleEdit = (row) => {
    // 填充表单数据
    for (const key in movieForm.value) {
      movieForm.value[key] = row[key]
    }
    dialogVisible.value = true
  }
  
  const handleDelete = (row) => {
    deleteMovieId.value = row.id
    deleteMovieTitle.value = row.title
    deleteDialogVisible.value = true
  }
  
  const submitForm = async () => {
    try {
      loading.value = true;

      const url = movieForm.value.id 
        ? `http://localhost:8000/api/movies/${movieForm.value.id}/`
        : 'http://localhost:8000/api/movies/';
        
      const method = movieForm.value.id ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(movieForm.value)
      });
      
      if (response.ok) {
        // 保存成功通知
        ElNotification({
          title: '成功',
          message: '电影信息保存成功',
          type: 'success',
          duration: 3000, // 3秒后自动关闭
        });
        dialogVisible.value = false;
        fetchMovies();
      } else {
        // 保存失败通知
        const errorData = await response.json();
        ElNotification({
          title: '失败',
          message: `保存失败 (${response.status}): ${errorData.detail || '请检查输入内容'}`,
          type: 'error',
          duration: 5000, // 5秒后自动关闭
        });
      }
    } catch (error) {
      // 网络错误通知
      ElNotification({
        title: '错误',
        message: '网络错误，请重试',
        type: 'error',
        duration: 5000,
      });
      console.error('保存API错误:', error);
    } finally {
      loading.value = false;
    }
  };
  
  const confirmDelete = async () => {
    try {
      loading.value = true; // 添加加载状态
      const response = await fetch(`http://localhost:8000/api/movies/${deleteMovieId.value}/`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        // 删除成功通知
        ElNotification({
          title: '成功',
          message: '电影删除成功',
          type: 'success',
          duration: 3000,
        });
        deleteDialogVisible.value = false;
        fetchMovies();
      } else {
        // 删除失败通知
        let errorMsg = `删除失败 (${response.status})`;
        try {
          const errorData = await response.json();
          errorMsg += `: ${errorData.detail || '删除操作失败'}`;
        } catch {
          errorMsg += ': 服务器返回错误';
        }
        
        ElNotification({
          title: '失败',
          message: errorMsg,
          type: 'error',
          duration: 5000,
        });
      }
    } catch (error) {
      // 网络错误通知
      ElNotification({
        title: '错误',
        message: '网络错误，请重试',
        type: 'error',
        duration: 5000,
      });
      console.error('删除API错误:', error);
    } finally {
      loading.value = false; // 重置加载状态
    }
  };
  </script>
  
  <style scoped>
  .movie-list {
    padding: 20px;
  }
  </style>    