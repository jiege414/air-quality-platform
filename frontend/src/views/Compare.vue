<template>
  <div class="compare">
    <h2 class="page-title">城市数据对比</h2>
    
    <div class="card-container">
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="选择城市">
          <el-select
            v-model="queryForm.cityCodes"
            multiple
            :collapse-tags="false"
            filterable
            remote
            reserve-keyword
            placeholder="请输入城市名搜索（至少选择2个）"
            :remote-method="searchCities"
            :loading="cityLoading"
            @change="handleCityChange"
            style="width: 450px;"
            ref="citySelect"
          >
            <el-option
              v-for="city in cities"
              :key="city.cityCode"
              :label="city.cityName"
              :value="city.cityCode"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期">
          <el-date-picker
            v-model="queryForm.startDate"
            type="date"
            placeholder="选择开始日期"
            value-format="yyyy-MM-dd"
            :picker-options="startPickerOptions"
            :default-value="defaultPickerDate"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker
            v-model="queryForm.endDate"
            type="date"
            placeholder="选择结束日期"
            value-format="yyyy-MM-dd"
            :picker-options="endPickerOptions"
            :default-value="defaultPickerDate"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery" icon="el-icon-search">开始对比</el-button>
          <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据缺失提示 -->
    <div v-if="missingDataCount > 0" class="card-container warning-tip">
      <i class="el-icon-warning"></i>
      <span>提示：查询范围内有 {{ missingDataCount }} 天数据缺失</span>
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

    <!-- 数据说明 -->
    <div class="data-note">
      <i class="el-icon-info"></i>
      <span>数据说明：本系统采用每天凌晨 2:00 的监测数据作为当日空气质量代表值</span>
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
        startDate: '',
        endDate: ''
      },
      cities: [],
      selectedCitiesMap: {}, // 存储所有已选择的城市信息
      cityLoading: false,
      chartData: [],
      tableData: [],
      statistics: [],
      selectedCities: [],
      hasQueried: false,
      missingDataCount: 0,
      compareChart: null,
      // 日期选择器默认显示2026年3月
      defaultPickerDate: new Date(2026, 2, 1),
      // 开始日期选择器配置
      startPickerOptions: {
        disabledDate: (time) => {
          const year = time.getFullYear()
          const month = time.getMonth()
          const date = time.getDate()

          // 限制年份必须在 2026-2027 之间
          if (year < 2026 || year > 2027) {
            return true
          }

          // 2026年2月13日之前不可选
          if (year === 2026 && (month < 1 || (month === 1 && date < 13))) {
            return true
          }

          // 2027年12月31日之后不可选
          if (year === 2027 && (month > 11 || (month === 11 && date > 31))) {
            return true
          }

          // 不能晚于结束日期
          if (this.queryForm.endDate) {
            const endDate = new Date(this.queryForm.endDate)
            return time.getTime() > endDate.getTime()
          }

          return false
        }
      },
      // 结束日期选择器配置
      endPickerOptions: {
        disabledDate: (time) => {
          const year = time.getFullYear()
          const month = time.getMonth()
          const date = time.getDate()

          // 限制年份必须在 2026-2027 之间
          if (year < 2026 || year > 2027) {
            return true
          }

          // 2026年2月13日之前不可选
          if (year === 2026 && (month < 1 || (month === 1 && date < 13))) {
            return true
          }

          // 2027年12月31日之后不可选
          if (year === 2027 && (month > 11 || (month === 11 && date > 31))) {
            return true
          }

          // 不能晚于今天
          const today = new Date()
          today.setHours(0, 0, 0, 0)
          if (time.getTime() > today.getTime()) {
            return true
          }

          // 不能早于开始日期
          if (this.queryForm.startDate) {
            const startDate = new Date(this.queryForm.startDate)
            return time.getTime() < startDate.getTime()
          }

          return false
        }
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
    // 获取城市列表（初始加载）
    async fetchCities() {
      try {
        const response = await this.$axios.get('/city/page', {
          params: {
            page: 1,
            size: 20
          }
        })
        if (response.data.code === 200) {
          this.cities = response.data.data.records
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
    // 搜索城市（支持模糊搜索）
    async searchCities(query) {
      this.cityLoading = true
      try {
        const response = await this.$axios.get('/city/page', {
          params: {
            page: 1,
            size: 20,
            keyword: query || ''
          }
        })
        if (response.data.code === 200) {
          this.cities = response.data.data.records
        }
      } catch (error) {
        console.error('搜索城市失败:', error)
      } finally {
        this.cityLoading = false
      }
    },
    // 处理城市选择变化
    handleCityChange(selectedCodes) {
      // 将当前搜索到的城市信息保存到 selectedCitiesMap
      this.cities.forEach(city => {
        if (selectedCodes.includes(city.cityCode)) {
          this.$set(this.selectedCitiesMap, city.cityCode, city)
        }
      })
      // 清空搜索文本
      this.$nextTick(() => {
        if (this.$refs.citySelect) {
          this.$refs.citySelect.query = ''
          this.$refs.citySelect.previousQuery = ''
        }
      })
    },
    async handleQuery() {
      if (this.queryForm.cityCodes.length < 2) {
        this.$message.warning('请至少选择2个城市进行对比')
        return
      }
      if (!this.queryForm.startDate || !this.queryForm.endDate) {
        this.$message.warning('请选择开始日期和结束日期')
        return
      }

      this.hasQueried = true
      // 从 selectedCitiesMap 获取已选择的城市信息
      this.selectedCities = this.queryForm.cityCodes.map(code => {
        return this.selectedCitiesMap[code] || { cityCode: code, cityName: code }
      })

      try {
        const response = await this.$axios.post('/air-quality/compare', {
          cityCodes: this.queryForm.cityCodes,
          startDate: this.queryForm.startDate,
          endDate: this.queryForm.endDate
        })

        if (response.data.code === 200) {
          this.processData(response.data.data)
          // 设置缺失数据计数
          this.missingDataCount = response.data.data.missingDataCount || 0
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
      this.queryForm.startDate = ''
      this.queryForm.endDate = ''
      this.selectedCitiesMap = {}
      this.chartData = []
      this.tableData = []
      this.statistics = []
      this.selectedCities = []
      this.hasQueried = false
      this.missingDataCount = 0
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
        // 从 selectedCitiesMap 获取城市名称
        const city = this.selectedCitiesMap[cityCode]
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
      const startDate = new Date(this.queryForm.startDate)
      const endDate = new Date(this.queryForm.endDate)
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
        // 从 selectedCitiesMap 获取城市名称
        const city = this.selectedCitiesMap[cityCode]
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
        // 从 selectedCitiesMap 获取城市名称
        const city = this.selectedCitiesMap[cityCode]
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

.data-note {
  text-align: center;
  padding: 15px;
  margin-top: 20px;
  color: #909399;
  font-size: 12px;
}

.data-note i {
  margin-right: 5px;
}

.warning-tip {
  background-color: #fdf6ec;
  border: 1px solid #f5dab1;
  color: #e6a23c;
  padding: 12px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
}

.warning-tip i {
  margin-right: 8px;
  font-size: 16px;
}
</style>
