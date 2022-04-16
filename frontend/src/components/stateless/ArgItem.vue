<template>
  <div>
    <a-row>
      <div v-if="valueFromRefs">
        <a-col :span="6"> {{ name }}: </a-col>
        <a-col :span="2">
          <a-button
            @mouseover="setValueFromRefs(false)"
            @mouseleave="clearTimeout"
            ><a-icon type="edit"
          /></a-button>
        </a-col>
        <a-col :span="16">
          <!-- <a-auto-complete
            v-model="autoCompleteValue"
            :data-source="briefKeys"
            style="width: 100%"
            placeholder="input here"
          /> -->
          <a-select style="width: 100%" @change="changeRefSelect">
            <a-select-option v-for="(value, index) in allRefable" :key="index">
              {{ repr(value) }}
            </a-select-option>
          </a-select>
        </a-col>
      </div>
      <div v-if="!valueFromRefs">
        <a-col :span="6"> {{ name }}: </a-col>
        <a-col :span="12">
          <div v-if="type == 'bool'">
            <a-switch
              @change="inputChange"
              :default-checked="defaultValue"
              style="width: 100%"
            />
          </div>
          <div v-else-if="type == 'int'">
            <a-input-number
              style="width: 100%"
              @change="inputChange"
              :defaultValue="defaultValue"
            />
          </div>
          <div v-else-if="type == 'float'">
            <a-input-number
              style="width: 100%"
              @change="inputChange"
              :step="0.1"
              :defaultValue="defaultValue"
            />
          </div>
          <div v-else-if="type == 'choices'">
            <a-select
              label-in-value
              style="width: 100%"
              :defaultValue="{ key: 'default' }"
              @change="changeChoicesSelect"
            >
              <a-select-option
                v-for="(value, label) in args.choices"
                :key="label"
              >
                {{ label }}[{{ value }}]
              </a-select-option>
            </a-select>
          </div>
          <div v-else-if="type == 'list'">
            <List @change="inputChange" />
          </div>
          <div v-else-if="type == 'tuple'">
            <a-input
              :defaultValue="defaultValue"
              @input="tupleChange"
              style="width: 100%"
            />
          </div>
          <div v-else>
            <a-input
              :defaultValue="defaultValue"
              @input="lineChange"
              style="width: 100%"
            />
          </div>
          <a-alert v-if="alertValue" :message="alertValue" banner />
        </a-col>
        <a-col :span="4">
          <a-button>{{ type }}</a-button>
        </a-col>
        <a-col :span="2">
          <a-button
            @mouseover="setValueFromRefs(true)"
            @mouseleave="clearTimeout"
            ><a-icon type="paper-clip"
          /></a-button>
        </a-col>
      </div>
    </a-row>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import List from "./List.vue";

export default {
  // props: ["argvalue"],
  props: {
    defaultValue: {
      type: [Object, Number, String, Boolean, Array],
    },
    args: Object,
    name: String,
    ranges: null,
    type: { type: String, default: "Any" },
    // briefKeys:[]
  },
  name: "ArgItem",
  data() {
    return {
      isolat_value: null,
      valueFromRefs: false,
      timer: null,
      alertValue: "",
    };
  },
  components: { List },

  computed: {
    ...mapGetters(["repr", "allRefable"]),

  },
  methods: {
    changeRefSelect(value) {
      console.log("change ref select", value, this.allRefable[value]);
      value = this.allRefable[value];
      if (!value.startsWith("@")) {
        this.isolat_value = "@" + value;
      }
      this.$emit("emitValue", this.isolat_value);
      console.log("set value ", this.isolat_value);
    },

    setValueFromRefs(value) {
      this.timer = setTimeout(() => {
        this.valueFromRefs = value;
      }, 1000);
    },
    clearTimeout() {
      console.log("clean time out ");
      clearTimeout(this.timer);
    },
    changeChoicesSelect(value, option) {
      console.log("set choices", value, this.args.choices[value.key], option);
      this.$emit("emitValue", this.args.choices[value.key]);
    },

    lineChange(value) {
      // console.log('on emit',value.target.value,value)
      this.$emit("emitValue", value.target.value);
    },
    tupleChange(value) {
      value = value.target.value;
      const tupleregex = /^\([0-9,]+\)$/gm;
      let regexRet = tupleregex.exec(value);
      if (regexRet != null) {
        this.$emit("emitValue", value);
        this.alertValue = "";
      } else {
        this.alertValue = "tuple format: ([0-9,]).";
      }
    },
    inputChange(value) {
      // console.log('on emit',value)
      this.$emit("emitValue", value);
    },
  },
};
</script>
