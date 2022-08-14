<template>
  <div class="main">
    <a-autoComplete
      v-model:value="seach_feild"
      :data-source="history"
      style="width: 100%"
      placeholder="input here"
    >
      <a-input>
        <!-- <a-icon v-slot="suffix" type="search" /> -->
      </a-input>
    </a-autoComplete>

    <a-collapse
      accordion
      class="ele-collapse"
      v-model:value="activeKey"
      default-active-key="cv2"
    >
    
      <a-collapse-panel
        v-for="(items, ele_key) in panelElements"
        :key="ele_key"
        :header="ele_key"
        :collapsible="disabled ? Object.keys(items).length == 0 : header"
      >
        <!-- {{items}}  :collapsible="Object.keys(items).length == 0" -->
        <div style="max-height: 200px; overflow-y: auto">
          <p 
            v-for="(panelitem, item_key) in items"
            :key="item_key"
            @click="submitElement(panelitem)"
            @mouseenter="openNotification(panelitem.name,panelitem.doc)"
          >
          <!-- <a-tooltip placement="bottom" :title="panelitem.doc" :overlayStyle="{width: 480}"> -->

            {{ panelitem.name }}
          <!-- </a-tooltip> -->
          </p>
        </div>
      </a-collapse-panel>
    </a-collapse>
    <!-- <Factory v-if="functionData" /> -->
  </div>
</template>

<script setup lang="ts">
import { RXFunction,LambdaFunction } from "@/store/RxLibrary";
import { ref, computed ,h } from "vue";
import _ from 'lodash'

// import { mapGetters, mapMutations, useStore } from "vuex";
import { libraryStore,CurrentStateStore } from "@/store";
const activeKey = ref(["cv2"]);
const seach_feild = ref("");
const history = ref([]);
// const libraryDoc = ref('')
import { notification } from 'ant-design-vue';

const openNotification = _.throttle( (name:string,doc:string) => {
      notification['info']({
        message: name,
        description:doc,
        maxCount:2,
        style:{width:'480px'}
      });
    },500)

function submitElement(item) {
  if (!history.value.includes(item.name)) {
    history.value.unshift(item.name);
  }
  let rxfunc = null
  if (item.type =='lambda'){
    rxfunc = new LambdaFunction(item)
  }else{
    rxfunc = new RXFunction(item);
  }
  CurrentStateStore.setFunction(rxfunc);
  CurrentStateStore.setMainMenu(['factory']);
}
// const allElements = libraryStore;
const panelElements = computed(() => {
  if (seach_feild.value) {
    let res_with_str_in_search_feild = {};
    for (let key in libraryStore.value) {
      let mod = {};
      for (let modkey in libraryStore.value[key]) {
        let is_modkey_substr_in_search_feild =
          modkey.indexOf(seach_feild.value) != -1;
        if (is_modkey_substr_in_search_feild) {
          mod[modkey] = libraryStore.value[key][modkey];
        }
      }
      res_with_str_in_search_feild[key] = mod;
    }
    return res_with_str_in_search_feild;
  } else {
    return libraryStore.value;
  }
});
</script>

<style scoped>
div.main {
  padding: 10px;
}
a-collapse.ele-collapse {
  padding: 10px;
  min-height: 300px;
}
</style>
