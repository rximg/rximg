import Vue from "vue";

const state = {
  locked: false,
  data: {
  }
}
const getters = {
  lockedStatus: (state) => state.locked,
  functionData: (state) => state.data
}
const mutations = {
  setLocked: (state, value) => {
    state.locked = value
  },
  setCurrentFunction: (state, ele) => {
    // state.data = {};
    // Vue.set(state,'date',{})
    if (ele.type == "lambda") {
      state.data = { type: "lambda", line: "" };
    } else {
      state.data = { ...ele };
      if (typeof (state.data.type) == "undefined") {
        state.data.type = "callable"
      }
    }
    console.log("set current func", state.data);
  },
  delCurrentFunction: (state) => {
    state.data = {};
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations
};
