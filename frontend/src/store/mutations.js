// const { v4: uuidv4 } = require("uuid");
import Vue from "vue";
const md5 = require("md5");
const deepcopy = require("deepcopy");
const mutations = {
  setElements: (state, elements) => (state.elements = elements),
  initConfigNames(state, { type, current, names }) {
    if (type == "success") {
      state.confignames.current = current;
      state.confignames.names = names;
    }
  },
};

export default mutations;
