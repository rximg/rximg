
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

function convertDataToStr(uuid,subscribe_item) {
  var {type,value} = subscribe_item.extraData
  if (type=='single'){
    subscribe_item.type = 'str'
    subscribe_item.value = value
  }else{
    subscribe_item.type = 'str'
    subscribe_item.value =`@core.get_subject('${uuid}')`
  }
  return subscribe_item
}
function newobs(uuid) {
  return {
    type: "observerable",
    from: "core",
    name: "build_observerable",
    args: {
      head: {
        // kind: "POSITIONAL_OR_KEYWORD",
        value: "@" + uuid,
      },
      pipe: {
        // kind: "POSITIONAL_OR_KEYWORD",
        type: "list",
        value: [],
      },
      subscribe: {
        type:"str",
        value: "None",
        extraData:{
          type:"single",
          value:null
        }
      }
    },
  }
}

const mutations = {
  // setIndex: (state, index) => {
  //   state.index = index;
  // },
  setRelations: (state, data) => {
    state.data = data;
  },
  newRelation: (state, head_uuid) => {
    // console.log("new relation", head_uuid);
    // let uuid = "OBS_"+uuidv4().substring(0,4)
    // let uuid =head_uuid
    Vue.set(state.data, md5(head_uuid), newobs(head_uuid));
    state.contentChangeTimes += 1;
  },
  swapSubscribeType:(state,{uuid,flag})=>{
    if (flag=='multicast'){
      Vue.set(state.data[uuid].args.subscribe,
        'extraData',{type:'single',value:"None"})
    }else{
      Vue.set(state.data[uuid].args.subscribe,
        'extraData',{type:'multicast',value:[]})
    }
    Vue.set(state.data[uuid].args.subscribe,convertDataToStr(uuid,state.data[uuid].args.subscribe))
    state.contentChangeTimes += 1;
  },
  addMulticast: (state,{uuid,type})=>{
    let multicastindexs = state.data[uuid].args.subscribe.extraData.value
    var num =0
    if (multicastindexs.length>0){
      num = Math.max.apply(Math,multicastindexs)+1
    }
    state.data[uuid].args.subscribe.extraData.value.push(num)
    let new_cmd = `core.get_subject('${uuid}','${type}')`
    let new_uuid = `${uuid}_${num}`
    Vue.set(state.data,new_uuid,newobs(new_cmd))
    Vue.set(state.data[uuid].args.subscribe,convertDataToStr(uuid,state.data[uuid].args.subscribe))
    state.contentChangeTimes += 1;
  },
  deleteMulticast: (state,{uuid,num})=>{
    // let new_uuid = "core.get_subject({0}:str,{1}:int)".format(uuid,num)
    let new_uuid = "{0}_{1}".format(uuid,num)
    Vue.delete(state.data,md5(new_uuid))
    Vue.set(state.data[uuid].args.subscribe,convertDataToStr(uuid,state.data[uuid].args.subscribe))
    state.contentChangeTimes += 1;
  },
  setSubscribe: (state, { uuid,value }) => {
    if (value!="None"){
      state.data[uuid].args.subscribe.extraData.value = '@'+value;
    }else{
      state.data[uuid].args.subscribe.extraData.value = value;
    }
    Vue.set(state.data[uuid].args.subscribe,convertDataToStr(uuid,state.data[uuid].args.subscribe))
    state.contentChangeTimes += 1;
  },
  deleteRelation: (state, subkey) => {
    let split = subkey.lastIndexOf('_')
    if (split>-1){

      let uuid = subkey.substring(0,split)
      let num = parseInt(subkey.substring(split+1))
      let newlist = state.data[uuid].args.subscribe.extraData.value.filter(
        (item)=>item!=num
        )
      Vue.set(state.data[uuid].args.subscribe.extraData, 'value',newlist)
      Vue.set(state.data[uuid].args.subscribe,convertDataToStr(uuid,state.data[uuid].args.subscribe))
    }
    Vue.delete(state.data, subkey);
    // console.log("relation index", key);
    state.contentChangeTimes += 1;
  },
  // cleanSubscribe: (state, key) => {
  //   // Vue.set(state.data[key].args.subscribe, "value", null);
  //   state.contentChangeTimes += 1;
  // },
  // newSubject: (state, head_uuid) => {
  //   // console.log("new relation", head_uuid);
  //   let uuid = "Subject_"+uuidv4().substring(0,4)
  //   Vue.set(state.data, uuid, {
  //     type: "subject",
  //     from: "core",
  //     name: "build_subject",
  //     args: {
  //       head: {
  //         kind: "POSITIONAL_OR_KEYWORD",
  //         value: "@" + head_uuid,
  //       },
  //     },
  //   });
  //   state.contentChangeTimes += 1;
  // },
  // newSubscribe: (state, head_uuid) => {
  //   let uuid = "HEAD_"+uuidv4().substring(0,4)
  //   Vue.set(state.data, uuid, {
  //     type: "subscribe",
  //     from: "core",
  //     name: "build_subsribe",
  //     args: {
  //       head: {
  //         kind: "POSITIONAL_OR_KEYWORD",
  //         value: "@" + head_uuid,
  //       },
  //       subscribe: {
  //         kind: "POSITIONAL_OR_KEYWORD",
  //         value: null,
  //       },
  //     },
  //   });
  //   state.contentChangeTimes += 1;
  // },
  addPipe: (state, { key, pipe_uuid }) => {
    Vue.set(
      state.data[key].args.pipe.value,
      state.data[key].args.pipe.value.length,
      "@"+pipe_uuid
    )
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

  deletePipe: (state, { key, pipe_index }) => {
    Vue.delete(state.data[key].args.pipe.value, pipe_index);
    state.contentChangeTimes += 1;
  },
  // cleanSubscribe: (state, key) => {
  //   Vue.set(state.data[key].args.subscribe, "value", null);
  //   state.contentChangeTimes += 1;
  // },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
};
