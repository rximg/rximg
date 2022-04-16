<template>
  <div class="main">
    <h1>Library</h1>
    <a-auto-complete
      v-model="seach_feild"
      :data-source="history"
      style="width: 100%"
      placeholder="input here"
    >
      <a-input>
        <a-icon slot="suffix" type="search" />
      </a-input>
    </a-auto-complete>
    <a-collapse
      accordion
      class="ele-collapse"
      v-model="activeKey"
      default-active-key="cv2"
    >
      <a-collapse-panel
        v-for="(items, model) in elements"
        :key="model"
        :header="model"
        :disabled="Object.keys(items).length == 0"
      >
        <!-- {{items}} -->
        <div style="max-height: 200px;overflow-y:auto;">
          <p
            v-for="(panelitem, key) in items"
            :key="key"
            @click="submitElement(panelitem)"
          >
            {{ panelitem.name }}
          </p>
        </div>
      </a-collapse-panel>
    </a-collapse>
    <Factory v-if="functionData" />
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import Factory from "./FactoryBox.vue";
export default {
  name: "Element",
  components: { Factory },
  data() {
    return {
      activeKey: ["cv2"],
      seach_feild: "",
      history: [],
    };
  },

  methods: {
    ...mapMutations("factory", ["setCurrentFunction"]),
    submitElement(item) {
      if (!this.lockedStatus) {
        if (!this.history.includes(item.name) ) {
          this.history.unshift(item.name);
        }
        this.setCurrentFunction(item);
      } else {
        this.$message.info("Current factory is occupied!");
      }
    },
  },
  computed: {
    ...mapGetters([
      "allElements",
      // "currentFunction",
      // "currentLockFunctionStatus",
    ]),
    ...mapGetters("factory", ["lockedStatus", "functionData"]),
    elements() {
      if (this.seach_feild) {
        let res_with_str_in_search_feild = {};
        for (let key in this.allElements) {
          let mod = {};
          for (let modkey in this.allElements[key]) {
            let is_modkey_substr_in_search_feild =
              modkey.indexOf(this.seach_feild) != -1;
            if (is_modkey_substr_in_search_feild) {
              mod[modkey] = this.allElements[key][modkey];
            }
          }
          res_with_str_in_search_feild[key] = mod;
        }
        return res_with_str_in_search_feild;
      } else {
        return this.allElements;
      }
    },
  },
};
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
