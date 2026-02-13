<template>
  <div class="compare">
    <h2 class="page-title">城市数据对比</h2>
    
    <div class="card-container">
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="选择城市">
          <el-select
            v-model="queryForm.cityCodes"
            multiple
            collapse-tags
            placeholder="请选择要对比的城市（至少2个）"
            style="width: 350px;"
          >
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
          <el-button type="primary" @click="handleQuery" icon="el-icon-search">开始对比</el-button>
          <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="chartData.length > 0">
      <div class="card-container">
        <h3>AQI对比趋势图</h3>
        <div ref="compareChart" style="height: 450px;"></div>
      </div>

      <div class="card-container" style="margin-top: 20px;">
        <h3>对比统计</h3>
        <el-row :gutter="20">
          <el-col :span="8" v-for="(stat, index) in statistics" :key="index">
            <div class="stat-card">
              <div class="stat-title">{{ stat.cityName }}</div>
              <div class="stat-row">
                <span class="stat-label">平均AQI:</span>
                <span class="stat-value" :style="{ color: getAqiColor(stat.avgAqi) }">{{ stat.avgAqi }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">最高AQI:</span>
                <span class="stat-value">{{ stat.maxAqi }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">最低AQI:</span>
                <span class="stat-value">{{ stat.minAqi }}</span>
              </div>
              <div class="stat-row">
                <span class="stat-label">优良天数:</span>
                <span class="stat-value">{{ stat.goodDays }}天</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="card-container" style="margin-top: 20px;">
        <h3>详细对比数据</h3>
        <el-table :data="tableData" stripe style="width: 100%">
          <el-table-column prop="date" label="日期" align="center" width="120" fixed></el-table-column>
          <el-table-column v-for="city in selectedCities" :key="city.cityCode" :label="city.cityName" align="center">
            <template slot-scope="scope">
              <el-tag :type="getAqiType(scope.row[city.cityCode])" size="small">
                {{ scope.row[city.cityCode] }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <div v-if="!hasData && hasQueried" class="card-container no-data">
      <i class="el-icon-warning-outline"></i>
      <p>暂无对比数据，请选择至少2个城市进行查询</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Compare',
  data() {
    return {
      queryForm: {
        cityCodes: [],
        dateRange: []
      },
      cities: [],
      chartData: [],
      tableData: [],
      statistics: [],
      selectedCities: [],
      hasQueried: false,
      compareChart: null,
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
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.compareChart) this.compareChart.dispose()
  },
  methods: {
    async fetchCities() {
      try {
        const response = await this.$axios.get('/city/list')
        if (response.data.code === 200) {
          this.cities = response.data.data
        }
      } catch (error) {
        console.error('获取城市列表失败:', error)
        this.cities = [
          { cityCode: '110000', cityName: '北京' },
          { cityCode: '310000', cityName: '上海' },
          { cityCode: '440100', cityName: '广州' },
          { cityCode: '440300', cityName: '深圳' },
          { cityCode: '330100', cityName: '杭州' },
          { cityCode: '320100', cityName: '南京' }
        ]
      }
    },
    async handleQuery() {
      if (this.queryForm.cityCodes.length < 2) {
        this.$message.warning('请至少选择2个城市进行对比')
        return
      }
      if (!this.queryForm.dateRange || this.queryForm.dateRange.length !== 2) {
        this.$message.warning('请选择时间范围')
        return
      }

      this.hasQueried = true
      this.selectedCities = this.cities.filter(c => this.queryForm.cityCodes.includes(c.cityCode))

      try {
        const response = await this.$axios.post('/air-quality/compare', {
          cityCodes: this.queryForm.cityCodes,
          startDate: this.queryForm.dateRange[0],
          endDate: this.queryForm.dateRange[1]
        })

        if (response.data.code === 200) {
          this.processData(response.data.data)
          this.$nextTick(() => {
            this.renderChart()
          })
        }
      } catch (error) {
        console.error('对比查询失败:', error)
        this.$message.error('查询失败，请稍后重试')
        this.processMockData()
        this.$nextTick(() => {
          this.renderChart()
        })
      }
    },
    handleReset() {
      this.queryForm.cityCodes = []
      this.queryForm.dateRange = []
      this.chartData = []
      this.tableData = []
      this.statistics = []
      this.selectedCities = []
      this.hasQueried = false
    },
    processData(data) {
      const dates = data.dates
      const cityData = data.cityData
      
      this.chartData = dates.map((date, index) => {
        const row = { date }
        this.queryForm.cityCodes.forEach(cityCode => {
          row[cityCode] = cityData[cityCode][index] || 0
        })
        return row
      })

      this.tableData = this.chartData

      this.statistics = this.queryForm.cityCodes.map(cityCode => {
        const values = cityData[cityCode]
        const city = this.cities.find(c => c.cityCode === cityCode)
        const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length)
        const max = Math.max(...values)
        const min = Math.min(...values)
        const goodDays = values.filter(v => v <= 100).length
        
        return {
          cityName: city ? city.cityName : cityCode,
          avgAqi: avg,
          maxAqi: max,
          minAqi: min,
          goodDays: goodDays
        }
      })
    },
    processMockData() {
      const startDate = new Date(this.queryForm.dateRange[0])
      const endDate = new Date(this.queryForm.dateRange[1])
      const dates = []
      
      for (let d = new Date(startDate); d <= endDate; d.setDate(d.getDate() + 1)) {
        dates.push(d.toISOString().split('T')[0])
      }

      this.chartData = dates.map(date => {
        const row = { date }
        this.queryForm.cityCodes.forEach((cityCode, index) => {
          const baseAqi = 50 + index * 20 + Math.random() * 50
          row[cityCode] = Math.round(baseAqi + Math.sin(new Date(date).getTime() / 86400000) * 20)
        })
        return row
      })

      this.tableData = this.chartData

      this.statistics = this.queryForm.cityCodes.map((cityCode, index) => {
        const city = this.cities.find(c => c.cityCode === cityCode)
        const values = this.chartData.map(row => row[cityCode])
        const avg = Math.round(values.reduce((a, b) => a + b, 0) / values.length)
        const max = Math.max(...values)
        const min = Math.min(...values)
        const goodDays = values.filter(v => v <= 100).length
        
        return {
          cityName: city ? city.cityName : cityCode,
          avgAqi: avg,
          maxAqi: max,
          minAqi: min,
          goodDays: goodDays
        }
      })
    },
    renderChart() {
      if (!this.compareChart) {
        this.compareChart = this.$echarts.init(this.$refs.compareChart)
      }

      const dates = this.chartData.map(item => item.date)
      const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#C45656']
      
      const series = this.queryForm.cityCodes.map((cityCode, index) => {
        const city = this.cities.find(c => c.cityCode === cityCode)
        return {
          name: city ? city.cityName : cityCode,
          type: 'line',
          data: this.chartData.map(item => item[cityCode]),
          smooth: true,
          symbol: 'circle',
          symbolSize: 6,
          lineStyle: {
            width: 2
          },
          itemStyle: {
            color: colors[index % colors.length]
          }
        }
      })

      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: series.map(s => s.name),
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
          name: 'AQI',
          min: 0
        },
        series: series
      }

      this.compareChart.setOption(option, true)
    },
    getAqiType(aqi) {
      if (aqi <= 50) return 'success'
      if (aqi <= 100) return ''
      if (aqi <= 150) return 'warning'
      return 'danger'
    },
    getAqiColor(aqi) {
      if (aqi <= 50) return '#67C23A'
      if (aqi <= 100) return '#909399'
      if (aqi <= 150) return '#E6A23C'
      if (aqi <= 200) return '#F56C6C'
      return '#C45656'
    },
    handleResize() {
      if (this.compareChart) this.compareChart.resize()
    }
  }
}
</script>

<style scoped>
.query-form {
  padding: 10px 0;
}

.stat-card {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 15px;
}

.stat-title {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409EFF;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
}

.stat-label {
  color: #606266;
}

.stat-value {
  font-weight: bold;
  color: #303133;
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
