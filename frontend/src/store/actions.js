import axios from "axios";
import deepcopy from "deepcopy";
const actions = {

  async initStore({ commit, state }) {
    let response = await axios.get("api/elements");
    commit("setElements", response.data);
    response = await axios.get("api/config")
    commit("initConfigNames",response.data)
    response = await axios.get("api/observers");
    commit("observers/setObervers", response.data.observers);
    commit("relations/setRelations", response.data.relations);
    commit("views/setParameter",response.data.parameters)
  },

  async getFileList({ commit }, items) {
    let response;
    if (items.type == "init") {
      response = await axios.get("api/file/listdir/");
    } else {
      response = await axios.post("api/file/listdir/", {
        dirs: items.dir,
        origin: items.origin,
      });
    }
    return response.data;
  },
  async save({ commit, state }) {
    console.log("post observers", state.observers.data);
    await axios.post("api/observers",{
      observers:state.observers.data,
      relations:state.relations.data,
      parameters:state.views.parameters,
    }
     );
  },
  async setCurrentConfigNameAndReload({state,commit,dispatch},name){
    let response = await axios.put("api/config/"+name);
    if (response.data.type=='success'){
      dispatch("initStore",{})
    }
  },
};

export default actions;
