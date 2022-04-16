
const state = {
    locked:false,
    data:{
    }
}
const getters = {
    lockedStatus:(state)=>state.locked,
    functionData:(state)=>state.data
}
const mutations = {
    setLocked:(state,value)=>{
        state.locked = value
    },
    setCurrentFunction: (state, ele) => {
        if (ele.type == "lambda") {
          state.data = { type: "lambda", line: "" };
        } else {
          state.data = { ...ele };
          if(typeof(state.data.type)=="undefined"){
            state.data.type = "callable"
          }
        }
        console.log("set current func", state.data);
      },
      delCurrentFunction: (state) => {
        state.data = null;
      },
}

export default { 
    namespaced: true,
    state, 
    getters, 
    mutations };
