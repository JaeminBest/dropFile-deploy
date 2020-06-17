const state = () => ({
    flag: false
})
  
const getters = {
    fetchFlag : state => {
        return state.flag
    }
}

const actions = {}

const mutations = {
    switchOn (state) {
        state.flag = true;
    },
    switchOff (state) {
        state.flag = false;
    }
}
  
export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
