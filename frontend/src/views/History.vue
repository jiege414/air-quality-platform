<template>
  <div class="history">
    <h2 class="page-title">历史数据查询</h2>
    
    <div class="card-container">
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="选择城市">
          <el-select
            v-model="queryForm.cityCode"
            filterable
            remote
            reserve-keyword
            clearable
            placeholder="请输入城市名搜索"
            :remote-method="searchCities"
            :loading="cityLoading"
            @focus="handleCityFocus"
            style="width: 200px;"
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
          <el-button type="primary" @click="handleQuery" icon="el-icon-search">查询</el-button>
          <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 数据缺失提示 -->
    <div v-if="missingDataCount > 0" class="card-container warning-tip">
      <i class="el-icon-warning"></i>
      <span>提示：查询范围内有 {{ missingDataCount }} 天数据缺失（已用虚线标记）</span>
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
        <el-table-column label="数据状态" align="center" width="100">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.hasData" type="success" size="small">有数据</el-tag>
            <el-tag v-else type="info" size="small">无数据</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="aqi" label="AQI" align="center" width="100">
          <template slot-scope="scope">
            <span v-if="scope.row.hasData">
              <el-tag :type="getAqiType(scope.row.aqi)" size="small">
                {{ scope.row.aqi }}
              </el-tag>
            </span>
            <span v-else style="color: #C0C4CC;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="quality" label="空气质量" align="center" width="100">
          <template slot-scope="scope">
            <span v-if="scope.row.hasData" :style="{ color: getQualityColor(scope.row.quality) }">
              {{ scope.row.quality }}
            </span>
            <span v-else style="color: #C0C4CC;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm25" label="PM2.5" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.hasData">{{ scope.row.pm25 }} <span style="color: #909399; font-size: 12px;">μg/m³</span></span>
            <span v-else style="color: #C0C4CC;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="pm10" label="PM10" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.hasData">{{ scope.row.pm10 }} <span style="color: #909399; font-size: 12px;">μg/m³</span></span>
            <span v-else style="color: #C0C4CC;">-</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-if="!hasData && hasQueried" class="card-container no-data">
      <i class="el-icon-warning-outline"></i>
      <p>暂无数据，请调整查询条件</p>
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
  name: 'History',
  data() {
    return {
      queryForm: {
        cityCode: '',
        startDate: '',
        endDate: ''
      },
      cities: [],
      cityLoading: false,
      chartData: [],
      tableData: [],
      hasQueried: false,
      trendChart: null,
      pollutantChart: null,
      missingDataCount: 0,
      // 数据最早日期：2026-02-13
      minDate: new Date(2026, 1, 13), // 月份从0开始，1表示2月
      // 数据最晚日期：明年12月31日
      maxDate: new Date(2027, 11, 31),
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
    this.initCharts()
    window.addEventListener('resize', this.handleResize)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.trendChart) this.trendChart.dispose()
    if (this.pollutantChart) this.pollutantChart.dispose()
  },
  methods: {
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
    // 城市选择框获得焦点时加载数据
    handleCityFocus() {
      if (this.cities.length === 0) {
        this.fetchCities()
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
      if (!this.queryForm.startDate || !this.queryForm.endDate) {
        this.$message.warning('请选择开始日期和结束日期')
        return
      }

      this.hasQueried = true
      try {
        // 使用新的 API，包含缺失数据标记
        const response = await this.$axios.get('/air-quality/history-with-missing', {
          params: {
            cityCode: this.queryForm.cityCode,
            startDate: this.queryForm.startDate,
            endDate: this.queryForm.endDate
          }
        })

        if (response.data.code === 200) {
          this.chartData = response.data.data
          this.tableData = response.data.data
          // 统计缺失数据天数
          this.missingDataCount = this.chartData.filter(item => !item.hasData).length
          this.$nextTick(() => {
            this.renderCharts()
          })
        }
      } catch (error) {
        console.error('查询历史数据失败:', error)
        this.$message.error('查询失败，请稍后重试')
        this.chartData = []
        this.tableData = []
        this.missingDataCount = 0
      }
    },
    // 重置：清空选择，图表保持原样
    handleReset() {
      this.queryForm.cityCode = ''
      this.queryForm.startDate = ''
      this.queryForm.endDate = ''
      // 注意：不清空 chartData 和 tableData，保持图表原样
      this.hasQueried = false
      this.missingDataCount = 0
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
      const aqiValues = this.chartData.map(item => item.hasData ? item.aqi : null)
      
      // 标记哪些数据点是缺失的
      const dataWithSymbol = this.chartData.map(item => {
        if (item.hasData) {
          return {
            value: item.aqi,
            symbol: 'circle',
            symbolSize: 8
          }
        } else {
          return {
            value: null,
            symbol: 'none'
          }
        }
      })
      
      const option = {
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            const dataIndex = params[0].dataIndex
            const item = this.chartData[dataIndex]
            if (item.hasData) {
              return `${item.date}<br/>AQI: ${item.aqi}<br/>空气质量: ${item.quality}`
            } else {
              return `${item.date}<br/><span style="color: #909399;">数据缺失</span>`
            }
          }
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
          data: dataWithSymbol,
          smooth: true,
          connectNulls: false, // 不连接空值，显示断点
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
      this.trendChart.setOption(option, true)
    },
    renderPollutantChart() {
      const dates = this.chartData.map(item => item.date)
      const pm25Values = this.chartData.map(item => item.hasData ? item.pm25 : null)
      const pm10Values = this.chartData.map(item => item.hasData ? item.pm10 : null)
      
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['PM2.5', 'PM10'],
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
            connectNulls: false,
            itemStyle: { color: '#F56C6C' }
          },
          {
            name: 'PM10',
            type: 'line',
            data: pm10Values,
            smooth: true,
            connectNulls: false,
            itemStyle: { color: '#E6A23C' }
          }
        ]
      }
      this.pollutantChart.setOption(option, true)
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

.warning-tip {
  background-color: #fdf6ec;
  border: 1px solid #f5dab1;
  color: #e6a23c;
  padding: 12px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
}

.warning-tip i {
  margin-right: 8px;
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
</style>
