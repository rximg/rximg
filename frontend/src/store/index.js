import Vuex from 'vuex';
import Vue from 'vue';
import actions from './actions'
import getters from './getters'
import mutations from './mutations'
import factory from './modules/factory';
import relations from './modules/relations';
import observers from './modules/observers';
import views from './modules/views';
const state = {
  elements: { init: "initvalue" },
  confignames:{
    current:"undefined",
    names:[]
  },
  dirlists:[]
};
Vue.use(Vuex);

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
  modules: {
    factory,
    relations,
    observers,
    views
  }
});
