import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    cities: []
  },
  mutations: {
    SET_CITIES(state, cities) {
      state.cities = cities
    }
  },
  actions: {
    async fetchCities({ commit }) {
      try {
        const response = await this._vm.$axios.get('/city/list')
        if (response.data.code === 200) {
          commit('SET_CITIES', response.data.data)
        }
      } catch (error) {
        console.error('获取城市列表失败:', error)
      }
    }
  }
})
