<template>
  <div class="ranking">
    <h2 class="page-title">全国城市AQI排行榜</h2>
    
    <div class="card-container">
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="ranking-section worst-section">
            <div class="section-header">
              <div class="header-title">
                <i class="el-icon-s-flag"></i>
                <span>空气质量最差城市 TOP10</span>
              </div>
            </div>
            <div ref="worstChart" style="height: 500px;"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="ranking-section best-section">
            <div class="section-header">
              <div class="header-title">
                <i class="el-icon-s-claim"></i>
                <span>空气质量最优城市 TOP10</span>
              </div>
            </div>
            <div ref="bestChart" style="height: 500px;"></div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="card-container table-card" style="margin-top: 20px;">
      <div class="table-header">
        <div class="header-title">
          <i class="el-icon-s-data"></i>
          <span>详细排名数据</span>
        </div>
        <el-radio-group v-model="rankingType" size="small" @change="handleTypeChange">
          <el-radio-button label="worst">最差排名</el-radio-button>
          <el-radio-button label="best">最优排名</el-radio-button>
        </el-radio-group>
      </div>
      <el-table 
        :data="paginatedTableData" 
        stripe 
        style="width: 100%"
        v-loading="loading"
        element-loading-text="加载中...">
        <el-table-column type="index" label="排名" min-width="12%" align="center">
          <template slot-scope="scope">
            <span :class="getRankClass((currentPage - 1) * pageSize + scope.$index)">{{ (currentPage - 1) * pageSize + scope.$index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="cityName" label="城市" min-width="20%" align="center">
          <template slot-scope="scope">
            <span class="city-name">{{ scope.row.cityName }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="aqi" label="AQI" min-width="15%" align="center">
          <template slot-scope="scope">
            <div class="aqi-tag" :style="{ background: getAqiColor(scope.row.aqi) }">
              {{ scope.row.aqi }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="quality" label="空气质量" min-width="18%" align="center">
          <template slot-scope="scope">
            <span class="quality-text" :style="{ color: getQualityColor(scope.row.quality) }">{{ scope.row.quality }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm25" label="PM2.5" min-width="17%" align="center">
          <template slot-scope="scope">
            <span class="pollutant-value">{{ scope.row.pm25 }}</span>
            <span class="unit">μg/m³</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm10" label="PM10" min-width="18%" align="center">
          <template slot-scope="scope">
            <span class="pollutant-value">{{ scope.row.pm10 }}</span>
            <span class="unit">μg/m³</span>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页组件 -->
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="tableData.length">
        </el-pagination>
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
      allWorstData: [],
      allBestData: [],
      tableData: [],
      worstChart: null,
      bestChart: null,
      loading: false,
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
      this.loading = true
      await this.fetchWorstRanking()
      await this.fetchBestRanking()
      this.loading = false
    },
    async fetchWorstRanking() {
      try {
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=10')
        if (response.data.code === 200) {
          this.worstData = this.formatData(response.data.data)
          this.renderChart(this.worstChart, this.worstData, 'worst')
        }
        
        // 获取所有城市数据用于表格分页
        const allResponse = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=100')
        if (allResponse.data.code === 200) {
          this.allWorstData = this.formatData(allResponse.data.data)
          if (this.rankingType === 'worst') {
            this.tableData = this.allWorstData
          }
        }
      } catch (error) {
        console.error('获取最差排名失败:', error)
        this.worstData = this.getMockData('worst', 10)
        this.allWorstData = this.getMockData('worst', 50)
        this.renderChart(this.worstChart, this.worstData, 'worst')
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
        
        // 获取所有城市数据用于表格分页
        const allResponse = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=100')
        if (allResponse.data.code === 200) {
          this.allBestData = this.formatData(allResponse.data.data)
          if (this.rankingType === 'best') {
            this.tableData = this.allBestData
          }
        }
      } catch (error) {
        console.error('获取最优排名失败:', error)
        this.bestData = this.getMockData('best', 10)
        this.allBestData = this.getMockData('best', 50)
        this.renderChart(this.bestChart, this.bestData, 'best')
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
    getMockData(type, count) {
      const cities = type === 'worst' 
        ? ['北京', '天津', '石家庄', '郑州', '济南', '西安', '沈阳', '太原', '乌鲁木齐', '兰州', '保定', '唐山', '邯郸', '邢台', '衡水', '沧州', '廊坊', '张家口', '承德', '秦皇岛']
        : ['三亚', '海口', '拉萨', '深圳', '珠海', '厦门', '昆明', '福州', '广州', '贵阳', '南宁', '南昌', '长沙', '南京', '杭州', '上海', '成都', '重庆', '武汉', '合肥']
      
      const result = []
      for (let i = 0; i < Math.min(count, cities.length); i++) {
        const aqi = type === 'worst' 
          ? 180 - i * 8 + Math.floor(Math.random() * 10)
          : 25 + i * 5 + Math.floor(Math.random() * 5)
        
        let quality
        if (aqi <= 50) quality = '优'
        else if (aqi <= 100) quality = '良'
        else if (aqi <= 150) quality = '轻度污染'
        else if (aqi <= 200) quality = '中度污染'
        else quality = '重度污染'
        
        result.push({
          cityName: cities[i],
          aqi: aqi,
          quality: quality,
          pm25: Math.round(aqi * 0.6),
          pm10: Math.round(aqi * 0.8)
        })
      }
      return result
    },
    renderChart(chart, data, type) {
      const cityNames = data.map(item => item.cityName)
      const aqiValues = data.map(item => item.aqi)
      
      // 根据AQI值生成渐变色
      const getGradientColor = (aqi) => {
        if (type === 'worst') {
          if (aqi > 200) {
            return new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#7e0023' },
              { offset: 1, color: '#99004c' }
            ])
          } else if (aqi > 150) {
            return new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#99004c' },
              { offset: 1, color: '#ff0000' }
            ])
          } else {
            return new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#ff0000' },
              { offset: 1, color: '#ff7e00' }
            ])
          }
        } else {
          if (aqi <= 50) {
            return new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#00e400' },
              { offset: 1, color: '#67C23A' }
            ])
          } else {
            return new this.$echarts.graphic.LinearGradient(0, 0, 1, 0, [
              { offset: 0, color: '#67C23A' },
              { offset: 1, color: '#95D475' }
            ])
          }
        }
      }
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { 
            type: 'shadow',
            shadowStyle: {
              color: 'rgba(0, 0, 0, 0.1)'
            }
          },
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#e4e7ed',
          borderWidth: 1,
          textStyle: {
            color: '#303133'
          },
          formatter: function(params) {
            const dataIndex = params[0].dataIndex
            const item = data[dataIndex]
            return `
              <div style="padding: 10px;">
                <div style="font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #303133;">${item.cityName}</div>
                <div style="display: flex; align-items: center; margin-bottom: 5px;">
                  <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${type === 'worst' ? '#F56C6C' : '#67C23A'}; margin-right: 8px;"></span>
                  <span style="color: #606266;">AQI: </span>
                  <span style="font-weight: bold; color: ${type === 'worst' ? '#F56C6C' : '#67C23A'}; margin-left: 5px;">${item.aqi}</span>
                </div>
                <div style="display: flex; align-items: center;">
                  <span style="color: #606266;">空气质量: </span>
                  <span style="font-weight: bold; color: ${item.quality === '优' ? '#67C23A' : item.quality === '良' ? '#909399' : '#F56C6C'}; margin-left: 5px;">${item.quality}</span>
                </div>
              </div>
            `
          }
        },
        grid: {
          left: '3%',
          right: '12%',
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
            fontSize: 12
          },
          axisLine: {
            lineStyle: {
              color: '#e4e7ed'
            }
          },
          axisLabel: {
            color: '#606266'
          },
          splitLine: {
            lineStyle: { 
              type: 'dashed',
              color: '#e4e7ed'
            }
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
          axisLine: {
            lineStyle: {
              color: '#e4e7ed'
            }
          },
          axisTick: { show: false }
        },
        series: [{
          name: 'AQI',
          type: 'bar',
          data: aqiValues.slice().reverse().map((value, index) => ({
            value: value,
            itemStyle: {
              color: getGradientColor(value),
              borderRadius: [0, 8, 8, 0],
              shadowColor: 'rgba(0, 0, 0, 0.15)',
              shadowBlur: 8,
              shadowOffsetY: 3
            }
          })),
          barWidth: '55%',
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
            fontSize: 13,
            fontWeight: 'bold',
            color: '#303133',
            distance: 10
          },
          emphasis: {
            itemStyle: {
              shadowColor: 'rgba(0, 0, 0, 0.25)',
              shadowBlur: 12,
              shadowOffsetY: 5
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
    getAqiColor(aqi) {
      if (aqi <= 50) return '#00e400'
      if (aqi <= 100) return '#ffff00'
      if (aqi <= 150) return '#ff7e00'
      if (aqi <= 200) return '#ff0000'
      if (aqi <= 300) return '#99004c'
      return '#7e0023'
    },
    getQualityColor(quality) {
      const colorMap = {
        '优': '#67C23A',
        '良': '#E6A23C',
        '轻度污染': '#F56C6C',
        '中度污染': '#C45656',
        '重度污染': '#8B0000',
        '严重污染': '#4a0000'
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
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.ranking-section:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.worst-section {
  border-top: 4px solid #F56C6C;
}

.best-section {
  border-top: 4px solid #67C23A;
}

.section-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.header-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.header-title i {
  margin-right: 10px;
  font-size: 20px;
}

.worst-section .header-title i {
  color: #F56C6C;
}

.best-section .header-title i {
  color: #67C23A;
}

.table-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.table-header .header-title {
  font-size: 18px;
  font-weight: 600;
}

.table-header .header-title i {
  color: #409EFF;
  margin-right: 10px;
  font-size: 22px;
}

/* 表格样式优化 */
.city-name {
  font-weight: 500;
  color: #303133;
  font-size: 14px;
}

.aqi-tag {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  color: #fff;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.quality-text {
  font-weight: 600;
  font-size: 14px;
}

.pollutant-value {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
}

.unit {
  color: #909399;
  font-size: 12px;
  margin-left: 4px;
}

/* 排名样式 */
.rank-first {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #F56C6C 0%, #ff9999 100%);
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(245, 108, 108, 0.4);
}

.rank-second {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #E6A23C 0%, #f0c78a 100%);
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(230, 162, 60, 0.4);
}

.rank-third {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #409EFF 0%, #8cc5ff 100%);
  color: #fff;
  border-radius: 50%;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.4);
}

.rank-normal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: #f5f7fa;
  color: #606266;
  border-radius: 50%;
  font-weight: 600;
  font-size: 13px;
}

/* 分页样式 */
.pagination-container {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-pagination) {
  font-weight: 500;
}

:deep(.el-pagination .el-pagination__total) {
  color: #606266;
}

:deep(.el-pagination .el-pagination__sizes) {
  margin-right: 15px;
}

:deep(.el-pagination .el-pager li) {
  font-weight: 500;
  border-radius: 6px;
  margin: 0 3px;
}

:deep(.el-pagination .el-pager li.active) {
  background: #409EFF;
  color: #fff;
}

:deep(.el-pagination button) {
  border-radius: 6px;
}
</style>
