import Vue from 'vue'
import Vuex from 'vuex'
import fetch from './modules/fetch'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    fetch
  }
})
