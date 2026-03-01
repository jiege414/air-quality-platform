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
            <div class="stat-value">{{ statistics.goodCityPercent || '-' }}%</div>
            <div class="stat-label">优良城市占比</div>
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
      <el-col :span="16">
        <div class="map-container">
          <div class="map-header">
            <div class="map-title">
              <i class="el-icon-map-location"></i>
              全国城市空气质量分布
            </div>
            <div class="map-search">
              <el-autocomplete
                v-model="searchCity"
                :fetch-suggestions="querySearch"
                placeholder="搜索城市"
                prefix-icon="el-icon-search"
                @select="handleSelect"
                @keyup.enter.native="handleSearchEnter"
                clearable
                size="small"
                style="width: 200px">
              </el-autocomplete>
            </div>
          </div>
          <div ref="mapChart" style="height: 520px;"></div>
          <div class="map-legend">
            <div class="legend-title">城市AQI实时报</div>
            <div class="legend-time">{{ currentTime }} 发布</div>
            <div class="legend-items">
              <div class="legend-item">
                <span class="legend-color" style="background: #00e400;"></span>
                <span class="legend-text">优</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #ffff00;"></span>
                <span class="legend-text">良</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #ff7e00;"></span>
                <span class="legend-text">轻度</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #ff0000;"></span>
                <span class="legend-text">中度</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #99004c;"></span>
                <span class="legend-text">重度</span>
              </div>
              <div class="legend-item">
                <span class="legend-color" style="background: #7e0023;"></span>
                <span class="legend-text">严重</span>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="side-panel">
          <div class="panel-title">
            <i class="el-icon-s-data"></i>
            重点城市监测
          </div>
          <div class="city-list">
            <div v-for="(city, index) in displayedCities" :key="index" 
                 class="city-item" 
                 @click="focusCity(city)">
              <div class="city-rank">{{ index + 1 }}</div>
              <div class="city-info">
                <div class="city-name">{{ city.name }}</div>
                <div class="city-aqi">
                  <span class="aqi-num" :style="{ color: getAqiColor(city.aqi) }">{{ city.aqi }}</span>
                  <span class="aqi-level" :style="{ background: getAqiColor(city.aqi) }">{{ city.quality }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 城市详情弹窗 -->
    <el-dialog
      :title="selectedCity ? selectedCity.name + ' 空气质量详情' : '城市详情'"
      :visible.sync="cityDialogVisible"
      width="400px"
      center>
      <div v-if="selectedCity" class="city-detail">
        <div class="aqi-display">
          <div class="aqi-value" :style="{ color: getAqiColor(selectedCity.aqi) }">{{ selectedCity.aqi }}</div>
          <div class="aqi-badge" :style="{ background: getAqiColor(selectedCity.aqi) }">{{ selectedCity.quality }}</div>
        </div>
        
        <div class="detail-info">
          <div class="info-item">
            <span class="label">PM2.5：</span>
            <span class="value">{{ selectedCity.pm25 }} μg/m³</span>
          </div>
          <div class="info-item">
            <span class="label">PM10：</span>
            <span class="value">{{ selectedCity.pm10 }} μg/m³</span>
          </div>
          <div class="info-item">
            <span class="label">发布时间：</span>
            <span class="value">{{ new Date(selectedCity.dataTime).toLocaleString('zh-CN') }}</span>
          </div>
        </div>

        <div class="health-advice">
          <div class="advice-title">
            <i class="el-icon-info"></i> 健康指引
          </div>
          <div class="advice-content">{{ getHealthAdvice(selectedCity.aqi).guidance }}</div>
          <div class="advice-title" style="margin-top: 15px;">
            <i class="el-icon-warning"></i> 建议措施
          </div>
          <div class="advice-content">{{ getHealthAdvice(selectedCity.aqi).suggestion }}</div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getCityCoordinate } from '@/assets/cityCoordinates.js'

export default {
  name: 'Dashboard',
  data() {
    return {
      statistics: {
        totalCities: '-',
        goodCityPercent: '-',
        warningCount: '-',
        worstCity: '-'
      },
      mapChart: null,
      realtimeData: [],
      displayedCities: [],
      selectedCity: null,
      cityDialogVisible: false,
      searchCity: '',
      currentTime: new Date().toLocaleString('zh-CN')
    }
  },
  mounted() {
    this.initCharts()
    this.fetchData()
    window.addEventListener('resize', this.handleResize)
    // 更新时间
    setInterval(() => {
      this.currentTime = new Date().toLocaleString('zh-CN')
    }, 60000)
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize)
    if (this.mapChart) this.mapChart.dispose()
  },
  methods: {
    initCharts() {
      this.mapChart = this.$echarts.init(this.$refs.mapChart)
      
      // 添加地图点击事件
      this.mapChart.on('click', (params) => {
        if (params.componentType === 'series') {
          this.showCityDetail(params.data)
        }
      })
    },
    async fetchData() {
      await this.fetchRealtimeData()
    },
    async fetchWorstRanking() {
      try {
        console.log('正在获取最差排名数据...')
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=worst&limit=10')
        console.log('最差排名API响应:', response.data)
        if (response.data.code === 200) {
          const data = response.data.data
          console.log('最差排名数据:', data)
          this.renderRankingChart(this.worstRankingChart, data, 'worst')
        } else {
          console.error('API返回错误:', response.data.message)
          this.renderMockRankingChart(this.worstRankingChart, 'worst')
        }
      } catch (error) {
        console.error('获取最差排名失败:', error)
        this.renderMockRankingChart(this.worstRankingChart, 'worst')
      }
    },
    async fetchBestRanking() {
      try {
        console.log('正在获取最优排名数据...')
        const response = await this.$axios.get('/air-quality-realtime/ranking?type=best&limit=10')
        console.log('最优排名API响应:', response.data)
        if (response.data.code === 200) {
          const data = response.data.data
          console.log('最优排名数据:', data)
          this.renderRankingChart(this.bestRankingChart, data, 'best')
        } else {
          console.error('API返回错误:', response.data.message)
          this.renderMockRankingChart(this.bestRankingChart, 'best')
        }
      } catch (error) {
        console.error('获取最优排名失败:', error)
        this.renderMockRankingChart(this.bestRankingChart, 'best')
      }
    },
    async fetchRealtimeData() {
      try {
        console.log('正在获取实时数据...')
        const response = await this.$axios.get('/air-quality-realtime/list')
        console.log('实时数据API响应:', response.data)
        if (response.data.code === 200) {
          const data = response.data.data
          console.log('实时数据:', data)
          this.realtimeData = data
          this.updateStatistics(data)
          this.renderMap(data)
          // 更新重点城市列表（取AQI最高的15个城市）
          this.displayedCities = [...data]
            .sort((a, b) => b.aqi - a.aqi)
            .slice(0, 15)
            .map(item => ({
              name: item.cityName,
              aqi: item.aqi,
              quality: item.quality
            }))
        } else {
          console.error('API返回错误:', response.data.message)
        }
      } catch (error) {
        console.error('获取实时数据失败:', error)
      }
    },
    // 城市搜索功能
    querySearch(queryString, cb) {
      const cities = this.realtimeData.map(item => ({
        value: item.cityName,
        aqi: item.aqi,
        quality: item.quality
      }))
      const results = queryString
        ? cities.filter(city => city.value.toLowerCase().includes(queryString.toLowerCase()))
        : cities
      cb(results.slice(0, 10))
    },
    handleSelect(item) {
      this.focusCity(item)
    },
    handleSearchEnter() {
      // 回车键搜索
      if (this.searchCity) {
        const city = this.realtimeData.find(item => 
          item.cityName.toLowerCase().includes(this.searchCity.toLowerCase())
        )
        if (city) {
          this.focusCity({ value: city.cityName })
        } else {
          this.$message.warning(`未找到包含 "${this.searchCity}" 的城市`)
        }
      }
    },
    focusCity(city) {
      // 在地图上定位城市
      // 从搜索框返回的 item 中，城市名在 value 属性中
      const cityName = city.value || city.name
      const cityData = this.realtimeData.find(item => item.cityName === cityName)
      if (cityData) {
        const coord = getCityCoordinate(cityName)
        if (coord && this.mapChart) {
          this.mapChart.setOption({
            geo: {
              center: coord,
              zoom: 6
            }
          })
          // 显示城市详情
          this.showCityDetail({
            name: cityName,
            value: [...coord, cityData.aqi, cityData.quality, cityData.pm25, cityData.pm10, cityData.dataTime],
            itemStyle: { color: this.getAqiColor(cityData.aqi) }
          })
          this.$message.success(`已定位到 ${cityName}`)
        } else {
          this.$message.warning(`未找到 ${cityName} 的坐标信息`)
        }
      } else {
        this.$message.error(`未找到 ${cityName} 的数据`)
      }
    },
    renderMap(data) {
      // 准备地图数据
      const mapData = data.map(item => {
        const coord = getCityCoordinate(item.cityName)
        if (coord) {
          return {
            name: item.cityName,
            value: [...coord, item.aqi, item.quality, item.pm25, item.pm10, item.dataTime],
            itemStyle: {
              color: this.getAqiColor(item.aqi)
            }
          }
        }
        return null
      }).filter(item => item !== null)

      const option = {
        backgroundColor: '#f0f8ff',
        tooltip: {
          trigger: 'item',
          backgroundColor: 'rgba(255, 255, 255, 0.95)',
          borderColor: '#ddd',
          borderWidth: 1,
          textStyle: {
            color: '#333'
          },
          formatter: (params) => {
            if (params.componentType === 'series') {
              const data = params.data
              return `
                <div style="padding: 12px; min-width: 180px;">
                  <div style="font-weight: bold; font-size: 16px; margin-bottom: 10px; color: #333;">${data.name}</div>
                  <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 28px; font-weight: bold; margin-right: 10px; color: ${data.itemStyle.color};">${data.value[2]}</span>
                    <span style="background: ${data.itemStyle.color}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 13px;">${data.value[3]}</span>
                  </div>
                  <div style="color: #666; font-size: 13px; line-height: 1.8;">
                    <div>PM2.5: ${data.value[4]} μg/m³</div>
                    <div>PM10: ${data.value[5]} μg/m³</div>
                    <div style="margin-top: 8px; color: #999; font-size: 12px;">更新时间: ${new Date(data.value[6]).toLocaleString('zh-CN')}</div>
                  </div>
                </div>
              `
            }
            return params.name
          }
        },
        // 美化后的中国地图
        geo: {
          map: 'china',
          roam: true,
          zoom: 1.15,
          center: [105, 36],
          label: {
            show: false
          },
          itemStyle: {
            areaColor: '#e8f4f8',
            borderColor: '#a0c4d9',
            borderWidth: 1,
            shadowColor: 'rgba(0, 0, 0, 0.1)',
            shadowBlur: 5,
            shadowOffsetY: 3
          },
          emphasis: {
            itemStyle: {
              areaColor: '#d0e8f2'
            }
          }
        },
        series: [
          {
            name: 'AQI',
            type: 'scatter',
            coordinateSystem: 'geo',
            data: mapData,
            symbolSize: 14,
            emphasis: {
              scale: 1.8,
              label: {
                show: true,
                formatter: '{b}',
                position: 'top',
                fontSize: 13,
                fontWeight: 'bold',
                color: '#333',
                backgroundColor: 'rgba(255,255,255,0.8)',
                padding: [4, 8],
                borderRadius: 4
              }
            }
          }
        ]
      }

      // 加载中国地图数据并渲染
      this.loadChinaMap().then(() => {
        this.mapChart.setOption(option)
      })
    },
    async loadChinaMap() {
      // 从 CDN 加载中国地图数据
      try {
        const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
        const chinaJson = await response.json()
        this.$echarts.registerMap('china', chinaJson)
        return true
      } catch (error) {
        console.error('加载中国地图数据失败:', error)
        // 使用简化的轮廓作为备用
        const simplifiedChina = {
          "type": "FeatureCollection",
          "features": [{
            "type": "Feature",
            "properties": {"name": "中国"},
            "geometry": {
              "type": "Polygon",
              "coordinates": [[
                [73, 53], [135, 53], [135, 18], [73, 18], [73, 53]
              ]]
            }
          }]
        }
        this.$echarts.registerMap('china', simplifiedChina)
        return false
      }
    },
    getAqiColor(aqi) {
      if (aqi <= 50) return '#00e400'
      if (aqi <= 100) return '#ffff00'
      if (aqi <= 150) return '#ff7e00'
      if (aqi <= 200) return '#ff0000'
      if (aqi <= 300) return '#99004c'
      return '#7e0023'
    },
    showCityDetail(cityData) {
      this.selectedCity = {
        name: cityData.name,
        aqi: cityData.value[2],
        quality: cityData.value[3],
        pm25: cityData.value[4],
        pm10: cityData.value[5],
        dataTime: cityData.value[6]
      }
      this.cityDialogVisible = true
    },
    getHealthAdvice(aqi) {
      if (aqi <= 50) {
        return {
          guidance: '空气质量令人满意，基本无空气污染',
          suggestion: '各类人群可正常活动'
        }
      } else if (aqi <= 100) {
        return {
          guidance: '空气质量可接受，但某些污染物可能对极少数异常敏感人群健康有较弱影响',
          suggestion: '极少数异常敏感人群应减少户外活动'
        }
      } else if (aqi <= 150) {
        return {
          guidance: '易感人群症状有轻度加剧，健康人群出现刺激症状',
          suggestion: '儿童、老年人及心脏病、呼吸系统疾病患者应减少长时间、高强度的户外锻炼'
        }
      } else if (aqi <= 200) {
        return {
          guidance: '进一步加剧易感人群症状，可能对健康人群心脏、呼吸系统有影响',
          suggestion: '疾病患者避免长时间、高强度的户外锻炼，一般人群适量减少户外运动'
        }
      } else if (aqi <= 300) {
        return {
          guidance: '心脏病和肺病患者症状显著加剧，运动耐受力降低，健康人群普遍出现症状',
          suggestion: '儿童、老年人和病人应停留在室内，避免体力消耗，一般人群避免户外活动'
        }
      } else {
        return {
          guidance: '健康人群运动耐受力降低，有明显强烈症状，提前出现某些疾病',
          suggestion: '儿童、老年人和病人应停留在室内，避免体力消耗，一般人群避免户外活动'
        }
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
        // 计算优良城市占比（AQI <= 100 为优良）
        const goodCities = data.filter(item => item.aqi <= 100)
        this.statistics.goodCityPercent = Math.round((goodCities.length / data.length) * 100)
        // 找出污染最严重的城市
        const worst = data.reduce((max, item) => item.aqi > max.aqi ? item : max, data[0])
        this.statistics.worstCity = worst.cityName
      }
    },
    handleResize() {
      if (this.mapChart) this.mapChart.resize()
    }
  }
}
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

/* 地图容器样式 */
.map-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  position: relative;
}

.map-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.map-title {
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.map-title i {
  margin-right: 8px;
  font-size: 20px;
}

.map-search {
  display: flex;
  align-items: center;
}

.map-search >>> .el-input__inner {
  border-radius: 20px;
  border: none;
  background: rgba(255, 255, 255, 0.9);
}

/* 地图图例 */
.map-legend {
  position: absolute;
  left: 20px;
  bottom: 20px;
  background: rgba(255, 255, 255, 0.95);
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  min-width: 160px;
}

.legend-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.legend-time {
  font-size: 12px;
  color: #999;
  margin-bottom: 12px;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
}

.legend-color {
  width: 14px;
  height: 14px;
  border-radius: 3px;
  margin-right: 5px;
}

.legend-text {
  color: #666;
}

/* 侧边栏样式 */
.side-panel {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  height: 580px;
  overflow: hidden;
}

.panel-title {
  padding: 16px 20px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.panel-title i {
  margin-right: 8px;
}

.city-list {
  padding: 10px;
  max-height: 520px;
  overflow-y: auto;
}

.city-item {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 8px;
}

.city-item:hover {
  background: #f5f7fa;
  transform: translateX(5px);
}

.city-rank {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 13px;
  color: #666;
  margin-right: 12px;
}

.city-item:nth-child(1) .city-rank {
  background: #ff6b6b;
  color: white;
}

.city-item:nth-child(2) .city-rank {
  background: #ffa502;
  color: white;
}

.city-item:nth-child(3) .city-rank {
  background: #ffdd59;
  color: #333;
}

.city-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.city-name {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.city-aqi {
  display: flex;
  align-items: center;
  gap: 8px;
}

.aqi-num {
  font-size: 18px;
  font-weight: 600;
}

.aqi-level {
  color: white;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
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

/* 城市详情弹窗样式 */
.city-detail {
  padding: 10px;
}

.aqi-display {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.aqi-value {
  font-size: 48px;
  font-weight: bold;
  margin-right: 15px;
}

.aqi-badge {
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
}

.detail-info {
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  color: #606266;
  font-weight: 500;
}

.info-item .value {
  color: #303133;
  font-weight: bold;
}

.health-advice {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.advice-title {
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}

.advice-title i {
  margin-right: 5px;
  color: #409EFF;
}

.advice-content {
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
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
