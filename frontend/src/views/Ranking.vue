<template>
  <div class="ranking">
    <h2 class="page-title">全国城市AQI排行榜</h2>
    
    <!-- 图表区域 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-header" style="background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);">
            <i class="el-icon-s-flag"></i>
            <span>空气质量最差城市 TOP10</span>
          </div>
          <div class="chart-body">
            <div ref="worstChart" style="height: 400px;"></div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="chart-header" style="background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);">
            <i class="el-icon-s-claim"></i>
            <span>空气质量最优城市 TOP10</span>
          </div>
          <div class="chart-body">
            <div ref="bestChart" style="height: 400px;"></div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 详细排名表格 -->
    <div class="table-card">
      <div class="table-header">
        <div class="header-left">
          <i class="el-icon-s-data"></i>
          <span>详细排名数据</span>
        </div>
        <div class="header-right">
          <el-radio-group v-model="rankingType" size="small" @change="handleTypeChange">
            <el-radio-button label="worst">最差排名</el-radio-button>
            <el-radio-button label="best">最优排名</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="table-body">
        <el-table 
          :data="paginatedTableData" 
          stripe 
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '500' }">
          <el-table-column label="排名" align="center">
            <template slot-scope="scope">
              <div :class="['rank-badge', getRankBadgeClass((currentPage - 1) * pageSize + scope.$index)]">
                {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="cityName" label="城市" align="center"></el-table-column>
          <el-table-column label="AQI" align="center">
            <template slot-scope="scope">
              <span :style="{ color: getAqiColor(scope.row.aqi), fontWeight: '500' }">{{ scope.row.aqi }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="quality" label="空气质量" align="center">
            <template slot-scope="scope">
              <span :style="{ color: getQualityColor(scope.row.quality) }">{{ scope.row.quality }}</span>
            </template>
          </el-table-column>
          <el-table-column label="PM2.5" align="center">
            <template slot-scope="scope">
              {{ scope.row.pm25 }} <span style="color: #909399; font-size: 12px;">μg/m³</span>
            </template>
          </el-table-column>
          <el-table-column label="PM10" align="center">
            <template slot-scope="scope">
              {{ scope.row.pm10 }} <span style="color: #909399; font-size: 12px;">μg/m³</span>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="tableData.length"
            background>
          </el-pagination>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Ranking',
  data() {
    return {
      rankingType: 'worst',
      worstData: [],
      bestData: [],
      tableData: [],
      allWorstData: [],
      allBestData: [],
      worstChart: null,
      bestChart: null,
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    paginatedTableData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.tableData.slice(start, end)
    }
  },
  mounted() {
    this.initCharts()
    this.fetchData()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.worstChart) this.worstChart.dispose()
    if (this.bestChart) this.bestChart.dispose()
  },
  methods: {
    initCharts() {
      this.worstChart = this.$echarts.init(this.$refs.worstChart)
      this.bestChart = this.$echarts.init(this.$refs.bestChart)
    },
    async fetchData() {
      await this.fetchWorstRanking()
      await this.fetchBestRanking()
    },
    async fetchWorstRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=10')
        if (response.data.code === 200) {
          this.worstData = this.formatData(response.data.data)
          this.renderChart(this.worstChart, this.worstData, 'worst')
        }
      } catch (error) {
        console.error('获取最差排名失败:', error)
        this.worstData = this.getMockData('worst')
        this.renderChart(this.worstChart, this.worstData, 'worst')
      }
      
      // 获取全量数据用于表格分页
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=1000')
        if (response.data.code === 200) {
          this.allWorstData = this.formatData(response.data.data)
          if (this.rankingType === 'worst') {
            this.tableData = this.allWorstData
          }
        }
      } catch (error) {
        console.error('获取最差排名全量数据失败:', error)
        this.allWorstData = this.getMockData('worst')
        if (this.rankingType === 'worst') {
          this.tableData = this.allWorstData
        }
      }
    },
    async fetchBestRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=10')
        if (response.data.code === 200) {
          this.bestData = this.formatData(response.data.data)
          this.renderChart(this.bestChart, this.bestData, 'best')
        }
      } catch (error) {
        console.error('获取最优排名失败:', error)
        this.bestData = this.getMockData('best')
        this.renderChart(this.bestChart, this.bestData, 'best')
      }
      
      // 获取全量数据用于表格分页
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=1000')
        if (response.data.code === 200) {
          this.allBestData = this.formatData(response.data.data)
          if (this.rankingType === 'best') {
            this.tableData = this.allBestData
          }
        }
      } catch (error) {
        console.error('获取最优排名全量数据失败:', error)
        this.allBestData = this.getMockData('best')
        if (this.rankingType === 'best') {
          this.tableData = this.allBestData
        }
      }
    },
    formatData(data) {
      const result = []
      for (let i = 0; i < data.cityNames.length; i++) {
        result.push({
          cityName: data.cityNames[i],
          aqi: data.aqiValues[i],
          quality: data.qualityList[i],
          pm25: Math.round(data.aqiValues[i] * 0.6),
          pm10: Math.round(data.aqiValues[i] * 0.8)
        })
      }
      return result
    },
    getMockData(type) {
      const mockData = type === 'worst' 
        ? { cityNames: ['北京', '天津', '石家庄', '郑州', '济南', '西安', '沈阳', '太原', '乌鲁木齐', '兰州', '成都', '武汉', '长沙', '合肥', '南京', '杭州', '上海', '广州', '深圳', '重庆'], aqiValues: [180, 165, 158, 145, 138, 132, 128, 125, 122, 118, 115, 112, 108, 105, 102, 98, 95, 92, 88, 85], qualityList: ['中度污染', '中度污染', '中度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '良', '良', '良', '良', '良'] }
        : { cityNames: ['三亚', '海口', '拉萨', '深圳', '珠海', '厦门', '昆明', '福州', '广州', '贵阳', '南宁', '南昌', '长春', '哈尔滨', '呼和浩特', '乌鲁木齐', '银川', '西宁', '兰州', '西安'], aqiValues: [25, 32, 38, 42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82, 85, 88, 92, 95], qualityList: ['优', '优', '优', '优', '优', '优', '良', '良', '良', '良', '良', '良', '良', '良', '良', '良', '良', '良', '良', '良'] }
      return this.formatData(mockData)
    },
    renderChart(chart, data, type) {
      const cityNames = data.map(item => item.cityName)
      const aqiValues = data.map(item => item.aqi)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#ddd',
          borderWidth: 1,
          textStyle: { color: '#333' },
          formatter: (params) => {
            const dataIndex = params[0].dataIndex
            const item = data[dataIndex]
            return `
              <div style="padding: 10px;">
                <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px;">${item.cityName}</div>
                <div style="color: ${type === 'worst' ? '#ff6b6b' : '#67c23a'}; font-size: 16px; font-weight: bold;">AQI: ${item.aqi}</div>
                <div style="color: #666; margin-top: 5px; font-size: 12px;">空气质量: ${item.quality}</div>
              </div>
            `
          }
        },
        grid: {
          left: '3%',
          right: '8%',
          bottom: '3%',
          top: '5%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: 'AQI指数',
          nameLocation: 'end',
          nameTextStyle: {
            color: '#909399',
            fontSize: 11
          },
          splitLine: {
            lineStyle: { 
              type: 'dashed',
              color: '#ebeef5'
            }
          },
          axisLabel: {
            color: '#909399',
            fontSize: 11
          }
        },
        yAxis: {
          type: 'category',
          data: cityNames.slice().reverse(),
          axisLabel: {
            fontSize: 12,
            color: '#606266'
          },
          axisTick: { show: false },
          axisLine: {
            lineStyle: {
              color: '#ebeef5'
            }
          }
        },
        series: [{
          name: 'AQI',
          type: 'bar',
          data: aqiValues.slice().reverse(),
          barWidth: '50%',
          itemStyle: {
            color: type === 'worst' 
              ? new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#ff9a9a' },
                  { offset: 1, color: '#ff6b6b' }
                ])
              : new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#95d475' },
                  { offset: 1, color: '#67c23a' }
                ]),
            borderRadius: [0, 4, 4, 0]
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
            fontSize: 11,
            color: '#606266'
          }
        }]
      }
      chart.setOption(option)
    },
    handleTypeChange(val) {
      this.currentPage = 1
      this.tableData = val === 'worst' ? this.allWorstData : this.allBestData
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    getRankBadgeClass(index) {
      if (index === 0) return 'rank-1'
      if (index === 1) return 'rank-2'
      if (index === 2) return 'rank-3'
      return 'rank-normal'
    },
    getAqiColor(aqi) {
      if (aqi <= 50) return '#67c23a'
      if (aqi <= 100) return '#e6a23c'
      if (aqi <= 150) return '#f56c6c'
      if (aqi <= 200) return '#c45656'
      return '#8b0000'
    },
    getQualityColor(quality) {
      const colorMap = {
        '优': '#67c23a',
        '良': '#e6a23c',
        '轻度污染': '#f56c6c',
        '中度污染': '#c45656',
        '重度污染': '#8b0000',
        '严重污染': '#4d0000'
      }
      return colorMap[quality] || '#909399'
    },
    handleResize() {
      if (this.worstChart) this.worstChart.resize()
      if (this.bestChart) this.bestChart.resize()
    }
  }
}
</script>

<style scoped>
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  padding-left: 10px;
  border-left: 4px solid #409eff;
}

.chart-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chart-header {
  padding: 12px 16px;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  align-items: center;
}

.chart-header i {
  margin-right: 8px;
  font-size: 16px;
}

.chart-body {
  padding: 16px;
}

.table-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  overflow: hidden;
}

.table-header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.header-left {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
}

.header-left i {
  margin-right: 8px;
  font-size: 16px;
}

.header-right >>> .el-radio-button__inner {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.5);
  color: #606266;
}

.header-right >>> .el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background: #fff;
  border-color: #fff;
  color: #409eff;
  box-shadow: -1px 0 0 0 #fff;
}

.table-body {
  padding: 16px;
}

.rank-badge {
  width: 24px;
  height: 24px;
  line-height: 24px;
  border-radius: 50%;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  margin: 0 auto;
}

.rank-1 {
  background: #ff6b6b;
  color: #fff;
}

.rank-2 {
  background: #ffa94d;
  color: #fff;
}

.rank-3 {
  background: #4dabf7;
  color: #fff;
}

.rank-normal {
  background: #e9ecef;
  color: #868e96;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
}
</style>
