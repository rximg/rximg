import Vue from 'vue'
import axios from "axios";

const state = {
    data:{},
    parameters:{},
    logs:[],
    ndarrayNormal:{},
    ndarrayROI:{},
}

const getters = {
    allParameters:(state)=>state.parameters,
    getNDArrayNormal:(state)=>(post_id)=>{
        return state.ndarrayNormal[post_id]
    },
    getNDArrayROI:(state)=>(post_id)=>{
        return state.ndarrayROI[post_id]
    }
}

const mutations = {
    cleanLogs(state){
        state.logs = []
    },
    SOCKET_emitResult(state,data){
        Vue.set(state.logs,state.logs.length, data)
    },
    setNDArrayNormal(state,{type,post_id,data}){
        if (type=='success'){
            Vue.set(state.ndarrayNormal,post_id,data)
        }
    },
    setNDArrayROI(state,{type,post_id,data}){
        if (type=='success'){
            state.ndarrayROI[post_id]=data
        }
    },
    setParameter(state,data){
        state.parameters = data
    },
    addParameter(state,{name,type,value}){
        if(name){
            let key = "parameter_"+name
            let item = {
                tag:name,
                name:"parameter",
                from:"custom",
                args:{
                    "input_":{
                        type:type,
                        value:value
                    }
                }
            }

            Vue.set(state.parameters,key,item)
        }
    },
    delParameter(state,name){
        let key = "parameter_"+name
        Vue.delete(state.parameters,key)
    }
}
const actions = {
    async queryNDArray({state,commit},post_id){
        let response = await axios.post("api/ndarray",{
            ndid:post_id
        });
        commit("setNDArrayNormal",response.data)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
  };