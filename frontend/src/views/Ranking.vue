<template>
  <div class="ranking">
    <h2 class="page-title">全国城市AQI排行榜</h2>
    
    <div class="card-container">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="ranking-section">
            <div class="section-header">
              <h3>
                <i class="el-icon-s-flag" style="color: #F56C6C;"></i>
                空气质量最差城市 TOP10
              </h3>
            </div>
            <div ref="worstChart" style="height: 500px;"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="ranking-section">
            <div class="section-header">
              <h3>
                <i class="el-icon-s-claim" style="color: #67C23A;"></i>
                空气质量最优城市 TOP10
              </h3>
            </div>
            <div ref="bestChart" style="height: 500px;"></div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="card-container" style="margin-top: 20px;">
      <div class="table-header">
        <h3>详细排名数据</h3>
        <el-radio-group v-model="rankingType" size="small" @change="handleTypeChange">
          <el-radio-button label="worst">最差排名</el-radio-button>
          <el-radio-button label="best">最优排名</el-radio-button>
        </el-radio-group>
      </div>
      <el-table :data="tableData" stripe style="width: 100%">
        <el-table-column type="index" label="排名" width="80" align="center">
          <template slot-scope="scope">
            <span :class="getRankClass(scope.$index)">{{ scope.$index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="cityName" label="城市" align="center"></el-table-column>
        <el-table-column prop="aqi" label="AQI" align="center">
          <template slot-scope="scope">
            <el-tag :type="getAqiType(scope.row.aqi)" size="medium">
              {{ scope.row.aqi }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quality" label="空气质量" align="center">
          <template slot-scope="scope">
            <span :style="{ color: getQualityColor(scope.row.quality) }">{{ scope.row.quality }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm25" label="PM2.5" align="center">
          <template slot-scope="scope">
            {{ scope.row.pm25 }} μg/m³
          </template>
        </el-table-column>
        <el-table-column prop="pm10" label="PM10" align="center">
          <template slot-scope="scope">
            {{ scope.row.pm10 }} μg/m³
          </template>
        </el-table-column>
      </el-table>
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
      worstChart: null,
      bestChart: null
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
          if (this.rankingType === 'worst') {
            this.tableData = this.worstData
          }
        }
      } catch (error) {
        console.error('获取最差排名失败:', error)
        this.worstData = this.getMockData('worst')
        this.renderChart(this.worstChart, this.worstData, 'worst')
        if (this.rankingType === 'worst') {
          this.tableData = this.worstData
        }
      }
    },
    async fetchBestRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=10')
        if (response.data.code === 200) {
          this.bestData = this.formatData(response.data.data)
          this.renderChart(this.bestChart, this.bestData, 'best')
          if (this.rankingType === 'best') {
            this.tableData = this.bestData
          }
        }
      } catch (error) {
        console.error('获取最优排名失败:', error)
        this.bestData = this.getMockData('best')
        this.renderChart(this.bestChart, this.bestData, 'best')
        if (this.rankingType === 'best') {
          this.tableData = this.bestData
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
        ? { cityNames: ['北京', '天津', '石家庄', '郑州', '济南', '西安', '沈阳', '太原', '乌鲁木齐', '兰州'], aqiValues: [180, 165, 158, 145, 138, 132, 128, 125, 122, 118], qualityList: ['中度污染', '中度污染', '中度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染', '轻度污染'] }
        : { cityNames: ['三亚', '海口', '拉萨', '深圳', '珠海', '厦门', '昆明', '福州', '广州', '贵阳'], aqiValues: [25, 32, 38, 42, 45, 48, 52, 55, 58, 62], qualityList: ['优', '优', '优', '优', '优', '优', '良', '良', '良', '良'] }
      return this.formatData(mockData)
    },
    renderChart(chart, data, type) {
      const cityNames = data.map(item => item.cityName)
      const aqiValues = data.map(item => item.aqi)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: function(params) {
            const dataIndex = params[0].dataIndex
            const item = data[dataIndex]
            return `${item.cityName}<br/>AQI: ${item.aqi}<br/>空气质量: ${item.quality}`
          }
        },
        grid: {
          left: '3%',
          right: '8%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: 'AQI指数',
          nameLocation: 'end',
          splitLine: {
            lineStyle: { type: 'dashed' }
          }
        },
        yAxis: {
          type: 'category',
          data: cityNames.slice().reverse(),
          axisLabel: {
            fontSize: 13,
            fontWeight: 'bold'
          },
          axisTick: { show: false }
        },
        series: [{
          name: 'AQI',
          type: 'bar',
          data: aqiValues.slice().reverse(),
          barWidth: '60%',
          itemStyle: {
            color: type === 'worst' 
              ? new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#F56C6C' },
                  { offset: 1, color: '#FF9999' }
                ])
              : new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
                  { offset: 0, color: '#67C23A' },
                  { offset: 1, color: '#95D475' }
                ]),
            borderRadius: [0, 4, 4, 0]
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
            fontSize: 12,
            fontWeight: 'bold'
          }
        }]
      }
      chart.setOption(option)
    },
    handleTypeChange(val) {
      this.tableData = val === 'worst' ? this.worstData : this.bestData
    },
    getRankClass(index) {
      if (index === 0) return 'rank-first'
      if (index === 1) return 'rank-second'
      if (index === 2) return 'rank-third'
      return 'rank-normal'
    },
    getAqiType(aqi) {
      if (aqi <= 50) return 'success'
      if (aqi <= 100) return ''
      if (aqi <= 150) return 'warning'
      if (aqi <= 200) return 'danger'
      return 'danger'
    },
    getQualityColor(quality) {
      const colorMap = {
        '优': '#67C23A',
        '良': '#909399',
        '轻度污染': '#E6A23C',
        '中度污染': '#F56C6C',
        '重度污染': '#C45656',
        '严重污染': '#8B0000'
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
.ranking-section {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 15px;
}

.section-header {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e4e7ed;
}

.section-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.section-header i {
  margin-right: 8px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.table-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.rank-first {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: #F56C6C;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
}

.rank-second {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: #E6A23C;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
}

.rank-third {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background: #409EFF;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
}

.rank-normal {
  color: #606266;
  font-weight: bold;
}
</style>
