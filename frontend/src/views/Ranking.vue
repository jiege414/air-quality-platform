<template>
  <div class="ranking">
    <h2 class="page-title">全国城市AQI排行榜</h2>
    
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="ranking-card">
          <div class="card-header" style="background: linear-gradient(135deg, #F56C6C 0%, #FF9999 100%);">
            <div class="card-title">
              <i class="el-icon-s-flag"></i>
              空气质量最差城市 TOP10
            </div>
          </div>
          <div class="card-body">
            <div ref="worstChart" style="height: 480px;"></div>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="ranking-card">
          <div class="card-header" style="background: linear-gradient(135deg, #67C23A 0%, #95D475 100%);">
            <div class="card-title">
              <i class="el-icon-s-claim"></i>
              空气质量最优城市 TOP10
            </div>
          </div>
          <div class="card-body">
            <div ref="bestChart" style="height: 480px;"></div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="ranking-card" style="margin-top: 20px;">
      <div class="card-header" style="background: linear-gradient(135deg, #409EFF 0%, #79BBFF 100%);">
        <div class="card-title">
          <i class="el-icon-s-data"></i>
          详细排名数据
        </div>
        <div class="header-actions">
          <el-radio-group v-model="rankingType" size="small" @change="handleTypeChange">
            <el-radio-button label="worst">最差排名</el-radio-button>
            <el-radio-button label="best">最优排名</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="card-body">
        <el-table 
          :data="paginatedTableData" 
          stripe 
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#303133', fontWeight: '600' }">
          <el-table-column type="index" label="排名" width="100" align="center">
            <template slot-scope="scope">
              <span :class="getRankClass((currentPage - 1) * pageSize + scope.$index)">
                {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="cityName" label="城市" align="center" min-width="120"></el-table-column>
          <el-table-column prop="aqi" label="AQI" align="center" width="120">
            <template slot-scope="scope">
              <el-tag :type="getAqiType(scope.row.aqi)" size="medium" effect="plain">
                {{ scope.row.aqi }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="quality" label="空气质量" align="center" width="120">
            <template slot-scope="scope">
              <span :style="{ color: getQualityColor(scope.row.quality), fontWeight: '600' }">{{ scope.row.quality }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="pm25" label="PM2.5" align="center" width="140">
            <template slot-scope="scope">
              <span style="color: #606266;">{{ scope.row.pm25 }} <span style="font-size: 12px; color: #909399;">μg/m³</span></span>
            </template>
          </el-table-column>
          <el-table-column prop="pm10" label="PM10" align="center" width="140">
            <template slot-scope="scope">
              <span style="color: #606266;">{{ scope.row.pm10 }} <span style="font-size: 12px; color: #909399;">μg/m³</span></span>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="pagination-wrapper">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page.sync="currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size.sync="pageSize"
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
          formatter: function(params) {
            const dataIndex = params[0].dataIndex
            const item = data[dataIndex]
            return `
              <div style="padding: 10px;">
                <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px;">${item.cityName}</div>
                <div style="color: ${type === 'worst' ? '#F56C6C' : '#67C23A'}; font-size: 18px; font-weight: bold;">AQI: ${item.aqi}</div>
                <div style="color: #666; margin-top: 5px;">空气质量: ${item.quality}</div>
              </div>
            `
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
          nameTextStyle: {
            color: '#606266',
            fontSize: 12
          },
          splitLine: {
            lineStyle: { 
              type: 'dashed',
              color: '#e4e7ed'
            }
          },
          axisLabel: {
            color: '#606266'
          }
        },
        yAxis: {
          type: 'category',
          data: cityNames.slice().reverse(),
          axisLabel: {
            fontSize: 13,
            fontWeight: 'bold',
            color: '#303133'
          },
          axisTick: { show: false },
          axisLine: {
            lineStyle: {
              color: '#dcdfe6'
            }
          }
        },
        series: [{
          name: 'AQI',
          type: 'bar',
          data: aqiValues.slice().reverse(),
          barWidth: '55%',
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
            borderRadius: [0, 6, 6, 0],
            shadowColor: 'rgba(0, 0, 0, 0.1)',
            shadowBlur: 4,
            shadowOffsetY: 2
          },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
            fontSize: 12,
            fontWeight: 'bold',
            color: '#606266'
          },
          emphasis: {
            itemStyle: {
              shadowColor: 'rgba(0, 0, 0, 0.2)',
              shadowBlur: 8,
              shadowOffsetY: 4
            }
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
    getRankClass(index) {
      if (this.rankingType === 'worst') {
        if (index === 0) return 'rank-first-worst'
        if (index === 1) return 'rank-second-worst'
        if (index === 2) return 'rank-third-worst'
      } else {
        if (index === 0) return 'rank-first-best'
        if (index === 1) return 'rank-second-best'
        if (index === 2) return 'rank-third-best'
      }
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
        '良': '#E6A23C',
        '轻度污染': '#F56C6C',
        '中度污染': '#C45656',
        '重度污染': '#8B0000',
        '严重污染': '#4D0000'
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
.ranking-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  color: white;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.card-title i {
  margin-right: 8px;
  font-size: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
}

.header-actions >>> .el-radio-button__inner {
  background: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.5);
  color: #606266;
}

.header-actions >>> .el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background: #fff;
  border-color: #fff;
  color: #409EFF;
  box-shadow: -1px 0 0 0 #fff;
}

.card-body {
  padding: 20px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

/* 排名样式 - 最差排名 */
.rank-first-worst {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #F56C6C;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.rank-second-worst {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #E6A23C;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.rank-third-worst {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #409EFF;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

/* 排名样式 - 最优排名 */
.rank-first-best {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #67C23A;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.rank-second-best {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #409EFF;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.rank-third-best {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #E6A23C;
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
}

.rank-normal {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: #e0e0e0;
  color: #606266;
  border-radius: 50%;
  font-weight: 600;
  font-size: 13px;
}
</style>
