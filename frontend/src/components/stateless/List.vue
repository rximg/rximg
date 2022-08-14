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
          <a-select
            style="width: 100%"
            default-value="int"
            v-model:value="selectType"
          >
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
        <a-col :span="4">
          <a-button @click="addItem" >
          <template #icon><plus-outlined /></template>
            <!-- <a-icon type="plus-circle" /> -->
          </a-button>
        </a-col>
      </a-row>
      <a-row v-for="(item, index) in items" :key="index">
          <!-- {{item.arg_value}}-{{item.type}}-{{item.type.value=='int'}} -->
        <a-col :span="12">
          <div v-if="item.type ==  'bool'">
            <a-switch  v-model:checked="item.arg_value" />
          </div>
          <div v-else-if="item.type ==  'int'">
            <a-input-number style="width: 100%" v-model:value="item.arg_value" />
          </div>
          <div v-else-if="item.type ==  'float'">
            <a-input-number
              style="width: 100%"
              v-model:value="item.arg_value"
              :step="0.1"
            />
          </div>
          <div v-else-if="item.type=='readonly'">{{item.arg_value}}</div>
          <div v-else-if="item.type=='ref'">
            <a-select style="width: 100%" v-model="item.arg_value">
              <a-select-option v-for="(rxfunc, index) in allRXfunctions" :key="index">
                {{ rxfunc.toString() }}
              </a-select-option>
            </a-select>
          </div>
          <div v-else-if="item.type=='str'">
            <a-input v-model:value="item.arg_value" style="width: 100%" />
          </div>
          <div v-else>
            <a-input v-model:value="item.arg_value" style="width: 100%" />
          </div>
          <!-- <a-alert v-if="alertValue" :message="alertValue" banner /> -->
        </a-col>
        <a-col :span="4">
          <a-button @click="delItem($event, index)" >
          <template #icon><close-outlined /></template>
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

<script setup lang="ts">
import { computed, reactive,shallowReactive, ref } from "vue";
import {RXFunctionsStore} from "@/store";
import {CloseOutlined, PlusOutlined} from "@ant-design/icons-vue";
//TOP list显示具体值
const props = defineProps(['valueModel'])
const emit = defineEmits(["update:valueModel"]);
const selectType = ref("str");
const typeOptions = ["str","ref", "int", "float", "bool" ];
const visible = ref(false);
type ListItemType = {
  type: string,
  arg_value: any
}
// type PropsType = {
//   valueModel: any[];
// };

// const { valueModel = [] } = defineProps<PropsType>();

const items = reactive<ListItemType>([])
if (props.valueModel){
  props.valueModel.forEach(item => {
    items.push({
      type:'readonly',
      arg_value:ref(item)
    })
  } )
}
const lenItem = computed(() => items.length);
// 将setCurrentFunctionArg由VUEX替换为通过事件传出去

// setValueFromRefs(value) {
//   this.valueFromRefs = value;
// },

const allRXfunctions = computed(() => {
  return Object.values(RXFunctionsStore);
});
const addItem = () => {
  console.log("addItem",items);
  let defaultValue: any = 0;
  if (selectType.value == "bool") {
    defaultValue = false;
  } else if (selectType.value == "ref") {
    defaultValue = "";
  }
  items.push({
    type: selectType.value,
    arg_value: ref(defaultValue),
  });
};
const delItem = function (e, index) {
  items.splice(0);
};

const handleOk = function (e) {
  emit(
    "update:valueModel",
    items.map(function (item) {
      return item.arg_value.value;
    })
  );
  visible.value = false;
};
// const handleCancel = function (e) {
//   visible.value = false;
// };
const setVisible = function (value: boolean) {
  visible.value = value;
};
</script>
