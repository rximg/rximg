import Vue from "vue";
const md5 = require("md5");
const deepcopy = require("deepcopy");
import { isString } from "../utils";
const state = {
  data: {},
};


const getters = {
  allObserver: (state) =>
    Object.keys(state.data).map(function(key) {
      return { uuid: key, ...state.data[key] };
    }),
  keys: (state) => Object.keys(state.data),
  breifTitleByUUID: (state) => (uuid) => {
    var item = state.data[uuid];
    if (item.type != "func") {
      return item.name;
    }
    var titles = [];
    for (var k in item.args) {
      let { type, name, value, title_tag } = item.args[k];
      var title;
      if (title_tag) {
        if (type == "list") {
          title = `${name}=${value.length}`;
        } else if (isString(value) && value[0] == "@") {
          let ref = state.data[value.slice(1, -1)]; //qureyByBriefUUID(state.data,value.slice(1,-1))
          if (ref) {
            title = `${name}=${ref.name}`;
          } else {
            title = `${name}=${value}`;
          }
        } else {
          title = `${name}=${value}`;
        }
        titles.push(title);
      }
    }
    if (titles) {
      return item.name + ":" + titles.join("");
    } else {
      return item.name;
    }
  },
};

const mutations = {
  setObervers: (state, observers) => (state.data = observers),
  editArgInObservers: (state, { index, argname, key, value }) => {
    // console.log("arg in obs", state.data);
    Vue.set(state.data[index].args[argname], key, value);
  },
  deleteObservers: (state, item) => {
    console.log("del", item.uuid);
    Vue.delete(state.data, item.uuid);
  },

  // setFilelistDir:(state,items) => (state.dirlists = items),

  // addFunctions: (state, newfunc) => {
  //   Vue.set(state.observers,newfunc.name,newfunc)
  // },
  addObserverByFunction: function (state, { funcData, args,op }) {

    // let { outputs, returns, name } = funcData;
    let params = op+funcData.name + ":";
    let copy_args = deepcopy(funcData.args);
    if (copy_args){
      Object.keys(args).forEach((k) => {

        copy_args[k].value = args[k];
        copy_args[k].choices = null;
      });
      Object.keys(copy_args).forEach((k) => {
        let v = copy_args[k];
        params += k + "=" + v.value + ",";
      });
    }
    // var outputIndexs = [];
    // for (let k in outputs) {
    //   if (outputs[k]) {
    //     params += k;
    //     outputIndexs.push(parseInt(k));
    //   }
    // }
    // const cuuuid = uuidv4()
    const md5id = md5(params);
    let newfunc = {
      type: "func",
      from: funcData.from,
      uuid: md5id,
      name: funcData.name,
      // output: outputIndexs,
      op:op,
      returnType:funcData.returnType,
      // func_name:
      //return_view: funcData.return_view,
      args: copy_args,
    };
    Vue.set(state.data, md5id, newfunc);
    // return md5id
    if (funcData.returnType=='Observable'){

      this.commit('relations/newRelation',md5id)
    }
    // state.observers = { ...state.observers,
    // [md5id]: newfunc };
  },
  addObserverByFileCreator: (state, playload) => {
    let md5_str = playload.join("");
    const md5id = md5(md5_str);
    let newfunc = {
      type: "func",
      from: "custom",
      uuid: md5id,
      name: "glob_dirs",
      // title:["glob_dirs"],
      args: {
        dirs: {
          index: 1,
          kind: "POSITIONAL_OR_KEYWORD",
          name: "dirs",
          type: "list",
          value: playload,
        },
      },
    };
    Vue.set(state.data, md5id, newfunc);
  },
  addObserverByLambda: (state, {line, argValue, op}) => {
    const md5id = md5(op+line);
    let newfunc = {
      type: "lambda",
      from: "custom",
      line: line,
      args: {
        line:{
          index: 0,
          kind: "POSITIONAL_OR_KEYWORD",
          type: "str",
          value:line,
        },
        args: {
          index: 1,
          kind: "POSITIONAL_OR_KEYWORD",
          type: "list",
          value: argValue,
        },
      },
      op:op,
      uuid: md5id,
      name: "LAMBDA",
      // title:["lambda"]
    };
    // const cuuuid = uuidv4()
    Vue.set(state.data, md5id, newfunc);
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
};
