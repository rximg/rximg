<template>
  <div>
    <a-modal
      :visible="visible"
      title="List"
      @ok="handleOk"
      @cancel="setVisible(false)"
    >
      <a-row>
        <a-col :span="20">
          <a-select  style="width: 100%" default-value="int" v-model="selectType">
            <!-- <div> -->
            <a-select-option
              v-for="(value, key) in typeOptions"
              :key="key"
              :value="value"
              >{{ value }}
            </a-select-option>
            <!-- </div> -->
          </a-select>
        </a-col>
        <a-col :span="4" >
          <a-button @click="addItem" icon="plus">
            <!-- <a-icon type="plus-circle" /> -->
          </a-button>
        </a-col>
      </a-row>
      <a-row v-for="(item, index) in items" :key="index">
        <a-col :span="20" >
          <div v-if="item.type == 'bool'">
            <a-switch
              @change="inputChange($event, index)"
              :default-checked="item.defaultValue"
            />
          </div>
          <div v-else-if="item.type == 'int'">
            <a-input-number 
            style="width: 100%"
              @change="inputChange($event, index)"
              :defaultValue="item.defaultValue"
            />
          </div>
          <div v-else-if="item.type == 'float'">
            <a-input-number
            style="width: 100%"
              @change="inputChange($event, index)"
              :step="0.1"
              :defaultValue="item.defaultValue"
            />
          </div>
          <div v-else-if="item.type == 'ref'">
            <!-- <a-input
            style="width: 100%"
              :defaultValue="item.defaultValue"
              @change="inputChange($event, index)"
            /> -->
              <a-select
              style="width: 100%"
              @change="changeRefSelect($event, index)"
            >
              <a-select-option
                v-for="(value, index) in allRefable"
                :key="index"
              >
                {{ repr(value) }}
              </a-select-option>
            </a-select>
          </div>
          <div v-else-if="item.type=='str'">
            <a-input
            style="width: 100%"
            :defaultValue="item.defaultValue"
            @input="lineChange($event,index)"
            />

          </div>
        </a-col>
        <a-col :span="4">
          <a-button @click="delItem($event,index)" icon="close">
            <!-- <a-icon type="del" /> -->
          </a-button>
        </a-col>
      </a-row>
    </a-modal>
    <a-button style="width: 100%" @click="setVisible(true)"
      >List[{{ lenItem }}]</a-button
    >
  </div>
</template>

<script>
import Vue from 'vue';
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "List",
  data() {
    return {
      items: [],
      emit_items:[],
      typeOptions: ["int", "float", "bool","ref","str"],
      selectType: "int",
      visible: false,
    };
  },
  mounted(){
      this.$emit(
        "change",null)
  },
  computed: {
    lenItem() {
      return this.emit_items.length;
    },
    ...mapGetters(["repr","allRefable"]),
  },
  methods: {
    // 将setCurrentFunctionArg由VUEX替换为通过事件传出去

    // setValueFromRefs(value) {
    //   this.valueFromRefs = value;
    // },
    addItem() {
      let is_last_emputy = this.items.length!=0 && (this.items.slice(-1)[0].edit  !== true)
      // console.log("add item",this.items.length!=0 , (this.items.slice(-1)[0].edit  !== true),this.items.slice(-1)[0]);
      if (is_last_emputy) {
        return;
      }
      let selectType = this.selectType;
      let defaultValue = 0;
      if (selectType == "bool") {
        defaultValue = false;
      } else if (selectType == "ref") {
        defaultValue = "";
      }
      this.items.push({
        type: selectType,
        value: defaultValue,
      });
    },
    // changeSelect(value, option,index) {
    //   console.log("set choices", value, this.ranges[value.key]);
    //   // this.$emit("emitValue",this.ranges[value.key],);
    // },
    changeRefSelect(value,index){
      // console.log('change ref select',value,this.allRefable[value])
      value = this.allRefable[value]
      if (!value.startsWith("@")) {
        value = "@" + value;
      }
      this.items[index].value = value
      this.items[index].edit = true
      // this.$emit("emitValue",this.isolat_value);
      // console.log("set value ", this.isolat_value);
    },
    delItem(e,index){
      // console.log(this.items,index);
      Vue.delete(this.items,index)},
    inputChange(value, index) {
      this.items[index].value = value;
      this.items[index].edit = true;
      // this.$emit("emitValue", value);
      console.log("get value", value, index);
    },
    lineChange(value, index) {
      this.items[index].value = value.target.value;
      this.items[index].edit = true;
      // this.$emit("emitValue", value);
      console.log("get value", value, index);
    },
    handleOk(e) {
      this.$emit(
        "change",
        this.items.map(function(item) {
          return item.value;
        })
      );
      this.emit_items = this.items
      this.items=[]
      this.visible = false;
    },
    handleCancel(e) {
      this.visible = false;
    },
    setVisible(value) {
      this.visible = value;
    },
  },
};
</script>

<style></style>
