<template>
  <div class="history">
    <h2 class="page-title">历史数据查询</h2>
    
    <div class="card-container">
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="选择城市">
          <el-select v-model="queryForm.cityCode" placeholder="请选择城市" style="width: 180px;">
            <el-option
              v-for="city in cities"
              :key="city.cityCode"
              :label="city.cityName"
              :value="city.cityCode"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker
            v-model="queryForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            :picker-options="pickerOptions"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery" icon="el-icon-search">查询</el-button>
          <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card-container" v-if="chartData.length > 0">
      <h3>AQI变化趋势</h3>
      <div ref="trendChart" style="height: 400px;"></div>
    </div>

    <div class="card-container" v-if="chartData.length > 0" style="margin-top: 20px;">
      <h3>污染物浓度变化</h3>
      <div ref="pollutantChart" style="height: 400px;"></div>
    </div>

    <div class="card-container" v-if="tableData.length > 0" style="margin-top: 20px;">
      <h3>详细数据</h3>
      <el-table :data="tableData" stripe style="width: 100%" max-height="500">
        <el-table-column prop="date" label="日期" align="center" width="120"></el-table-column>
        <el-table-column prop="aqi" label="AQI" align="center" width="100">
          <template slot-scope="scope">
            <el-tag :type="getAqiType(scope.row.aqi)" size="small">
              {{ scope.row.aqi }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quality" label="空气质量" align="center" width="100">
          <template slot-scope="scope">
            <span :style="{ color: getQualityColor(scope.row.quality) }">{{ scope.row.quality }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm25" label="PM2.5" align="center">
          <template slot-scope="scope">{{ scope.row.pm25 }} μg/m³</template>
        </el-table-column>
        <el-table-column prop="pm10" label="PM10" align="center">
          <template slot-scope="scope">{{ scope.row.pm10 }} μg/m³</template>
        </el-table-column>
        <el-table-column prop="so2" label="SO₂" align="center">
          <template slot-scope="scope">{{ scope.row.so2 }} μg/m³</template>
        </el-table-column>
        <el-table-column prop="no2" label="NO₂" align="center">
          <template slot-scope="scope">{{ scope.row.no2 }} μg/m³</template>
        </el-table-column>
        <el-table-column prop="co" label="CO" align="center">
          <template slot-scope="scope">{{ scope.row.co }} mg/m³</template>
        </el-table-column>
        <el-table-column prop="o3" label="O₃" align="center">
          <template slot-scope="scope">{{ scope.row.o3 }} μg/m³</template>
        </el-table-column>
      </el-table>
    </div>

    <div v-if="!hasData && hasQueried" class="card-container no-data">
      <i class="el-icon-warning-outline"></i>
      <p>暂无数据，请调整查询条件</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History',
  data() {
    return {
      queryForm: {
        cityCode: '',
        dateRange: []
      },
      cities: [],
      chartData: [],
      tableData: [],
      hasQueried: false,
      trendChart: null,
      pollutantChart: null,
      pickerOptions: {
        shortcuts: [
          {
            text: '最近一周',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      }
    }
  },
  computed: {
    hasData() {
      return this.chartData.length > 0
    }
  },
  mounted() {
    this.fetchCities()
    this.initCharts()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.trendChart) this.trendChart.dispose()
    if (this.pollutantChart) this.pollutantChart.dispose()
  },
  methods: {
    async fetchCities() {
      try {
        const response = await this.$axios.get('/city/list')
        if (response.data.code === 200) {
          this.cities = response.data.data
          if (this.cities.length > 0) {
            this.queryForm.cityCode = this.cities[0].cityCode
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
        this.queryForm.cityCode = '110000'
      }
    },
    initCharts() {
      this.$nextTick(() => {
        if (this.$refs.trendChart) {
          this.trendChart = this.$echarts.init(this.$refs.trendChart)
        }
        if (this.$refs.pollutantChart) {
          this.pollutantChart = this.$echarts.init(this.$refs.pollutantChart)
        }
      })
    },
    async handleQuery() {
      if (!this.queryForm.cityCode) {
        this.$message.warning('请选择城市')
        return
      }
      if (!this.queryForm.dateRange || this.queryForm.dateRange.length !== 2) {
        this.$message.warning('请选择时间范围')
        return
      }

      this.hasQueried = true
      try {
        const response = await this.$axios.get('/air-quality/history', {
          params: {
            cityCode: this.queryForm.cityCode,
            startDate: this.queryForm.dateRange[0],
            endDate: this.queryForm.dateRange[1]
          }
        })

        if (response.data.code === 200) {
          this.chartData = response.data.data
          this.tableData = response.data.data
          this.$nextTick(() => {
            this.renderCharts()
          })
        }
      } catch (error) {
        console.error('查询历史数据失败:', error)
        this.$message.error('查询失败，请稍后重试')
        this.chartData = this.getMockData()
        this.tableData = this.chartData
        this.$nextTick(() => {
          this.renderCharts()
        })
      }
    },
    handleReset() {
      this.queryForm.cityCode = this.cities.length > 0 ? this.cities[0].cityCode : ''
      this.queryForm.dateRange = []
      this.chartData = []
      this.tableData = []
      this.hasQueried = false
    },
    getMockData() {
      const data = []
      const cityName = this.cities.find(c => c.cityCode === this.queryForm.cityCode)?.cityName || '北京'
      const startDate = new Date(this.queryForm.dateRange[0])
      const endDate = new Date(this.queryForm.dateRange[1])
      
      for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        const dateStr = d.toISOString().split('T')[0]
        const baseAqi = 50 + Math.random() * 100
        const aqi = Math.round(baseAqi + Math.sin(d.getTime() / 86400000) * 30)
        
        let quality
        if (aqi <= 50) quality = '优'
        else if (aqi <= 100) quality = '良'
        else if (aqi <= 150) quality = '轻度污染'
        else if (aqi <= 200) quality = '中度污染'
        else quality = '重度污染'
        
        data.push({
          date: dateStr,
          cityName: cityName,
          aqi: Math.max(20, Math.min(300, aqi)),
          quality: quality,
          pm25: Math.round(aqi * 0.6),
          pm10: Math.round(aqi * 0.8),
          so2: Math.round(10 + Math.random() * 40),
          no2: Math.round(15 + Math.random() * 50),
          co: (0.5 + Math.random() * 1.5).toFixed(2),
          o3: Math.round(30 + Math.random() * 100)
        })
      }
      return data
    },
    renderCharts() {
      if (!this.trendChart) {
        this.trendChart = this.$echarts.init(this.$refs.trendChart)
      }
      if (!this.pollutantChart) {
        this.pollutantChart = this.$echarts.init(this.$refs.pollutantChart)
      }
      
      this.renderTrendChart()
      this.renderPollutantChart()
    },
    renderTrendChart() {
      const dates = this.chartData.map(item => item.date)
      const aqiValues = this.chartData.map(item => item.aqi)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: function(params) {
            const dataIndex = params[0].dataIndex
            const item = this.chartData[dataIndex]
            return `${item.date}<br/>AQI: ${item.aqi}<br/>空气质量: ${item.quality}`
          }.bind(this)
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dates,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: 'AQI',
          min: 0
        },
        series: [{
          name: 'AQI',
          type: 'line',
          data: aqiValues,
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          lineStyle: {
            width: 3,
            color: '#409EFF'
          },
          itemStyle: {
            color: '#409EFF'
          },
          areaStyle: {
            color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
            ])
          },
          markLine: {
            data: [
              { yAxis: 50, name: '优', lineStyle: { color: '#67C23A' } },
              { yAxis: 100, name: '良', lineStyle: { color: '#E6A23C' } },
              { yAxis: 150, name: '轻度', lineStyle: { color: '#F56C6C' } }
            ]
          }
        }]
      }
      this.trendChart.setOption(option)
    },
    renderPollutantChart() {
      const dates = this.chartData.map(item => item.date)
      const pm25Values = this.chartData.map(item => item.pm25)
      const pm10Values = this.chartData.map(item => item.pm10)
      const so2Values = this.chartData.map(item => item.so2)
      const no2Values = this.chartData.map(item => item.no2)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['PM2.5', 'PM10', 'SO₂', 'NO₂'],
          top: 10
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: dates,
          axisLabel: {
            rotate: 45
          }
        },
        yAxis: {
          type: 'value',
          name: '浓度 (μg/m³)'
        },
        series: [
          {
            name: 'PM2.5',
            type: 'line',
            data: pm25Values,
            smooth: true,
            itemStyle: { color: '#F56C6C' }
          },
          {
            name: 'PM10',
            type: 'line',
            data: pm10Values,
            smooth: true,
            itemStyle: { color: '#E6A23C' }
          },
          {
            name: 'SO₂',
            type: 'line',
            data: so2Values,
            smooth: true,
            itemStyle: { color: '#67C23A' }
          },
          {
            name: 'NO₂',
            type: 'line',
            data: no2Values,
            smooth: true,
            itemStyle: { color: '#409EFF' }
          }
        ]
      }
      this.pollutantChart.setOption(option)
    },
    getAqiType(aqi) {
      if (aqi <= 50) return 'success'
      if (aqi <= 100) return ''
      if (aqi <= 150) return 'warning'
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
      if (this.trendChart) this.trendChart.resize()
      if (this.pollutantChart) this.pollutantChart.resize()
    }
  }
}
</script>

<style scoped>
.query-form {
  padding: 10px 0;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #909399;
}

.no-data i {
  font-size: 48px;
  margin-bottom: 15px;
}

.no-data p {
  font-size: 14px;
}

h3 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 16px;
}
</style>
