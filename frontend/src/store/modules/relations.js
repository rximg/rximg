
import Vue from "vue";
const md5 = require("md5");
const deepcopy = require("deepcopy");
import { v4 as uuidv4 } from "uuid";
const state = {
  index: -1,
  data: {},
  contentChangeTimes: 0,
};
const getters = {
  relationChange: (state) => state.contentChangeTimes,
  keys: (state) => Object.keys(state.data),
};

const mutations = {
  setIndex: (state, index) => {
    state.index = index;
  },
  setRelations: (state, data) => {
    state.data = data;
  },
  newRelation: (state, head_uuid) => {
    // console.log("new relation", head_uuid);
    let uuid = "OBS_"+uuidv4().substring(0,4)
    Vue.set(state.data, uuid, {
      type: "observerable",
      from: "core",
      name: "build_observerable",
      args: {
        head: {
          kind: "POSITIONAL_OR_KEYWORD",
          value: "@" + head_uuid,
        },
        pipe: {
          kind: "POSITIONAL_OR_KEYWORD",
          type: "list",
          value: [],
        },
      },
    });
    state.contentChangeTimes += 1;
  },

  newSubject: (state, head_uuid) => {
    // console.log("new relation", head_uuid);
    let uuid = "Subject_"+uuidv4().substring(0,4)
    Vue.set(state.data, uuid, {
      type: "subject",
      from: "core",
      name: "build_subject",
      args: {
        head: {
          kind: "POSITIONAL_OR_KEYWORD",
          value: "@" + head_uuid,
        },
      },
    });
    state.contentChangeTimes += 1;
  },
  newSubscribe: (state, head_uuid) => {
    let uuid = "HEAD_"+uuidv4().substring(0,4)
    Vue.set(state.data, uuid, {
      type: "subscribe",
      from: "core",
      name: "build_subsribe",
      args: {
        head: {
          kind: "POSITIONAL_OR_KEYWORD",
          value: "@" + head_uuid,
        },
        subscribe: {
          kind: "POSITIONAL_OR_KEYWORD",
          value: null,
        },
      },
    });
    state.contentChangeTimes += 1;
  },
  addPipe: (state, { key, pipe_uuid }) => {
    Vue.set(
      state.data[key].args.pipe.value,
      state.data[key].args.pipe.value.length+1,
      "@"+pipe_uuid
    )
    state.contentChangeTimes += 1;
  },
  setSubscribe: (state, { key, subscribe_uuid }) => {
    console.log(key,subscribe_uuid)
    state.data[key].args.subscribe.value = "@"+subscribe_uuid;
    state.contentChangeTimes += 1;
  },
  swapPipes: (state, { relationIndex, oldIndex, newIndex }) => {
    // console.log(relationIndex, oldIndex, newIndex,state.data[relationIndex])
    let pipes = state.data[relationIndex].args.pipe.value;
    let temp = pipes.slice(oldIndex, 1);
    pipes.slice(newIndex, 0, temp);
    state.data[relationIndex].args.pipe.value = pipes;
    state.contentChangeTimes += 1;
  },
  deleteRelation: (state, key) => {
    console.log("relation index", key);
    Vue.delete(state.data, key);
    state.contentChangeTimes += 1;
  },
  deletePipe: (state, { key, pipe_index }) => {
    Vue.delete(state.data[key].args.pipe.value, pipe_index);
    state.contentChangeTimes += 1;
  },
  cleanSubscribe: (state, key) => {
    Vue.set(state.data[key].args.subscribe, "value", null);
    state.contentChangeTimes += 1;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
};
