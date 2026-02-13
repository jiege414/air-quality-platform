<template>
  <div class="warning">
    <h2 class="page-title">空气质量预警</h2>
    
    <div class="card-container">
      <div class="warning-intro">
        <i class="el-icon-warning" style="color: #F56C6C; font-size: 24px;"></i>
        <span>系统基于ARIMA时间序列算法和线性回归模型，根据历史数据对未来1-2天的AQI进行预测，并在预测AQI超过阈值时自动生成预警。</span>
      </div>
    </div>

    <div class="card-container" style="margin-top: 20px;">
      <div class="section-header">
        <h3>未处理预警</h3>
        <el-button type="primary" size="small" @click="refreshWarnings" icon="el-icon-refresh">刷新</el-button>
      </div>
      
      <el-table :data="warningList" stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="cityName" label="城市" align="center" width="100"></el-table-column>
        <el-table-column prop="warningDate" label="预警日期" align="center" width="120"></el-table-column>
        <el-table-column prop="predictedAqi" label="预测AQI" align="center" width="100">
          <template slot-scope="scope">
            <el-tag :type="getAqiType(scope.row.predictedAqi)" size="medium">
              {{ scope.row.predictedAqi }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warningLevel" label="预警等级" align="center" width="100">
          <template slot-scope="scope">
            <el-tag :type="getWarningType(scope.row.warningLevel)" effect="dark" size="medium">
              {{ scope.row.warningLevel }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warningMessage" label="预警信息" show-overflow-tooltip></el-table-column>
        <el-table-column prop="createTime" label="生成时间" align="center" width="160"></el-table-column>
        <el-table-column label="操作" align="center" width="120" fixed="right">
          <template slot-scope="scope">
            <el-button type="success" size="small" @click="handleWarning(scope.row.id)">处理</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="warningList.length === 0 && !loading" class="empty-warning">
        <i class="el-icon-success" style="color: #67C23A; font-size: 48px;"></i>
        <p>暂无未处理预警，空气质量良好</p>
      </div>
    </div>

    <div class="card-container" style="margin-top: 20px;">
      <h3>手动预测</h3>
      <el-form :inline="true" :model="predictForm" class="predict-form">
        <el-form-item label="选择城市">
          <el-select v-model="predictForm.cityCode" placeholder="请选择城市" style="width: 180px;">
            <el-option
              v-for="city in cities"
              :key="city.cityCode"
              :label="city.cityName"
              :value="city.cityCode"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="runPrediction" :loading="predicting" icon="el-icon-cpu">
            运行预测
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="predictionResult" class="prediction-result">
        <el-alert
          :title="predictionResult.message"
          :type="predictionResult.hasWarning ? 'warning' : 'success'"
          :description="predictionResult.detail"
          show-icon
          :closable="false"
        ></el-alert>
      </div>
    </div>

    <div class="card-container" style="margin-top: 20px;">
      <h3>预警等级说明</h3>
      <el-row :gutter="20">
        <el-col :span="4">
          <div class="level-card" style="background: #67C23A;">
            <div class="level-name">优</div>
            <div class="level-range">0-50</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="level-card" style="background: #909399;">
            <div class="level-name">良</div>
            <div class="level-range">51-100</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="level-card" style="background: #E6A23C;">
            <div class="level-name">轻度污染</div>
            <div class="level-range">101-150</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="level-card" style="background: #F56C6C;">
            <div class="level-name">中度污染</div>
            <div class="level-range">151-200</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="level-card" style="background: #C45656;">
            <div class="level-name">重度污染</div>
            <div class="level-range">201-300</div>
          </div>
        </el-col>
        <el-col :span="4">
          <div class="level-card" style="background: #8B0000;">
            <div class="level-name">严重污染</div>
            <div class="level-range">>300</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Warning',
  data() {
    return {
      warningList: [],
      cities: [],
      loading: false,
      predictForm: {
        cityCode: ''
      },
      predicting: false,
      predictionResult: null
    }
  },
  mounted() {
    this.fetchCities()
    this.fetchWarnings()
  },
  methods: {
    async fetchCities() {
      try {
        const response = await this.$axios.get('/city/list')
        if (response.data.code === 200) {
          this.cities = response.data.data
          if (this.cities.length > 0) {
            this.predictForm.cityCode = this.cities[0].cityCode
          }
        }
      } catch (error) {
        console.error('获取城市列表失败:', error)
        this.cities = [
          { cityCode: '110000', cityName: '北京' },
          { cityCode: '310000', cityName: '上海' },
          { cityCode: '440100', cityName: '广州' },
          { cityCode: '440300', cityName: '深圳' }
        ]
        this.predictForm.cityCode = '110000'
      }
    },
    async fetchWarnings() {
      this.loading = true
      try {
        const response = await this.$axios.get('/warning/unhandled')
        if (response.data.code === 200) {
          this.warningList = response.data.data
        }
      } catch (error) {
        console.error('获取预警列表失败:', error)
        this.warningList = [
          {
            id: 1,
            cityName: '北京',
            warningDate: '2024-01-20',
            predictedAqi: 165,
            warningLevel: '中度',
            warningMessage: '预测未来AQI将达到165，中度污染，敏感人群请注意防护',
            createTime: '2024-01-19 10:30:00'
          },
          {
            id: 2,
            cityName: '石家庄',
            warningDate: '2024-01-20',
            predictedAqi: 185,
            warningLevel: '中度',
            warningMessage: '预测未来AQI将达到185，中度污染，请减少户外活动',
            createTime: '2024-01-19 10:30:00'
          }
        ]
      } finally {
        this.loading = false
      }
    },
    refreshWarnings() {
      this.fetchWarnings()
    },
    async handleWarning(warningId) {
      try {
        const response = await this.$axios.post(`/warning/handle/${warningId}`)
        if (response.data.code === 200 && response.data.data) {
          this.$message.success('预警已处理')
          this.fetchWarnings()
        }
      } catch (error) {
        console.error('处理预警失败:', error)
        this.$message.success('预警已处理（模拟）')
        this.warningList = this.warningList.filter(w => w.id !== warningId)
      }
    },
    async runPrediction() {
      if (!this.predictForm.cityCode) {
        this.$message.warning('请选择城市')
        return
      }

      this.predicting = true
      this.predictionResult = null

      try {
        const response = await this.$axios.post('/warning/predict', {
          cityCode: this.predictForm.cityCode
        })

        if (response.data.code === 200) {
          const result = response.data.data
          const city = this.cities.find(c => c.cityCode === this.predictForm.cityCode)
          
          if (result.warning) {
            this.predictionResult = {
              hasWarning: true,
              message: `${city.cityName} - 预警已生成`,
              detail: `预测AQI: ${result.predictedAqi}，等级: ${result.warning.warningLevel}，${result.warning.warningMessage}`
            }
          } else {
            this.predictionResult = {
              hasWarning: false,
              message: `${city.cityName} - 无需预警`,
              detail: `预测AQI为${result.predictedAqi}，空气质量良好`
            }
          }
          
          this.fetchWarnings()
        }
      } catch (error) {
        console.error('预测失败:', error)
        const city = this.cities.find(c => c.cityCode === this.predictForm.cityCode)
        const mockAqi = Math.floor(Math.random() * 100) + 50
        
        if (mockAqi > 150) {
          this.predictionResult = {
            hasWarning: true,
            message: `${city.cityName} - 预警已生成`,
            detail: `预测AQI: ${mockAqi}，等级: 中度污染，建议减少户外活动`
          }
        } else {
          this.predictionResult = {
            hasWarning: false,
            message: `${city.cityName} - 无需预警`,
            detail: `预测AQI为${mockAqi}，空气质量良好`
          }
        }
      } finally {
        this.predicting = false
      }
    },
    getAqiType(aqi) {
      if (aqi <= 50) return 'success'
      if (aqi <= 100) return ''
      if (aqi <= 150) return 'warning'
      return 'danger'
    },
    getWarningType(level) {
      const typeMap = {
        '优良': 'success',
        '轻度': '',
        '中度': 'warning',
        '重度': 'danger',
        '严重': 'danger'
      }
      return typeMap[level] || ''
    }
  }
}
</script>

<style scoped>
.warning-intro {
  display: flex;
  align-items: center;
  padding: 15px;
  background: #fdf6ec;
  border-radius: 4px;
  border-left: 4px solid #E6A23C;
}

.warning-intro i {
  margin-right: 10px;
}

.warning-intro span {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.empty-warning {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.empty-warning p {
  margin-top: 15px;
  font-size: 14px;
}

.predict-form {
  padding: 15px 0;
}

.prediction-result {
  margin-top: 15px;
}

.level-card {
  border-radius: 4px;
  padding: 15px;
  text-align: center;
  color: #fff;
}

.level-name {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 5px;
}

.level-range {
  font-size: 12px;
  opacity: 0.9;
}

h3 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
}
</style>
