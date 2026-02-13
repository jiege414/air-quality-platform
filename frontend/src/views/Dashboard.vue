<template>
  <div class="dashboard">
    <h2 class="page-title">数据概览</h2>
    
    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #67C23A;">
            <i class="el-icon-s-data"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.totalCities || 20 }}</div>
            <div class="stat-label">监测城市</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #409EFF;">
            <i class="el-icon-s-marketing"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.avgAqi || '-' }}</div>
            <div class="stat-label">平均AQI</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #E6A23C;">
            <i class="el-icon-warning"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.warningCount || 0 }}</div>
            <div class="stat-label">预警数量</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon" style="background: #F56C6C;">
            <i class="el-icon-s-flag"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ statistics.worstCity || '-' }}</div>
            <div class="stat-label">污染最严重</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <div class="card-container">
          <h3>实时AQI排名（最差TOP10）</h3>
          <div ref="worstRankingChart" style="height: 400px;"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="card-container">
          <h3>实时AQI排名（最优TOP10）</h3>
          <div ref="bestRankingChart" style="height: 400px;"></div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <div class="card-container">
          <h3>全国城市空气质量分布</h3>
          <div ref="mapChart" style="height: 500px;"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      statistics: {
        totalCities: 20,
        avgAqi: 85,
        warningCount: 3,
        worstCity: '北京'
      },
      worstRankingChart: null,
      bestRankingChart: null,
      mapChart: null
    }
  },
  mounted() {
    this.initCharts()
    this.fetchData()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.worstRankingChart) this.worstRankingChart.dispose()
    if (this.bestRankingChart) this.bestRankingChart.dispose()
    if (this.mapChart) this.mapChart.dispose()
  },
  methods: {
    initCharts() {
      this.worstRankingChart = this.$echarts.init(this.$refs.worstRankingChart)
      this.bestRankingChart = this.$echarts.init(this.$refs.bestRankingChart)
      this.mapChart = this.$echarts.init(this.$refs.mapChart)
    },
    async fetchData() {
      await this.fetchWorstRanking()
      await this.fetchBestRanking()
      await this.fetchRealtimeData()
    },
    async fetchWorstRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=10')
        if (response.data.code === 200) {
          const data = response.data.data
          this.renderRankingChart(this.worstRankingChart, data, 'worst')
        }
      } catch (error) {
        console.error('获取最差排名失败:', error)
        this.renderMockRankingChart(this.worstRankingChart, 'worst')
      }
    },
    async fetchBestRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=10')
        if (response.data.code === 200) {
          const data = response.data.data
          this.renderRankingChart(this.bestRankingChart, data, 'best')
        }
      } catch (error) {
        console.error('获取最优排名失败:', error)
        this.renderMockRankingChart(this.bestRankingChart, 'best')
      }
    },
    async fetchRealtimeData() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/list')
        if (response.data.code === 200) {
          const data = response.data.data
          this.updateStatistics(data)
        }
      } catch (error) {
        console.error('获取实时数据失败:', error)
      }
    },
    renderRankingChart(chart, data, type) {
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: 'AQI'
        },
        yAxis: {
          type: 'category',
          data: data.cityNames.reverse(),
          axisLabel: {
            fontSize: 12
          }
        },
        series: [{
          name: 'AQI',
          type: 'bar',
          data: data.aqiValues.reverse(),
          itemStyle: {
            color: type === 'worst' ? '#F56C6C' : '#67C23A',
            borderRadius: [0, 4, 4, 0]
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}'
          }
        }]
      }
      chart.setOption(option)
    },
    renderMockRankingChart(chart, type) {
      const mockData = type === 'worst' 
        ? { cityNames: ['北京', '天津', '石家庄', '郑州', '济南', '西安', '沈阳', '太原', '乌鲁木齐', '兰州'], aqiValues: [180, 165, 158, 145, 138, 132, 128, 125, 122, 118] }
        : { cityNames: ['三亚', '海口', '拉萨', '深圳', '珠海', '厦门', '昆明', '福州', '广州', '贵阳'], aqiValues: [25, 32, 38, 42, 45, 48, 52, 55, 58, 62] }
      this.renderRankingChart(chart, mockData, type)
    },
    updateStatistics(data) {
      if (data && data.length > 0) {
        this.statistics.totalCities = data.length
        const totalAqi = data.reduce((sum, item) => sum + item.aqi, 0)
        this.statistics.avgAqi = Math.round(totalAqi / data.length)
        const worst = data.reduce((max, item) => item.aqi > max.aqi ? item : max, data[0])
        this.statistics.worstCity = worst.cityName
      }
    },
    handleResize() {
      if (this.worstRankingChart) this.worstRankingChart.resize()
      if (this.bestRankingChart) this.bestRankingChart.resize()
      if (this.mapChart) this.mapChart.resize()
    }
  }
}
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-icon i {
  font-size: 30px;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

h3 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
}
</style>
