<template>
  <div>
    <a-row v-if="!viewType">
      <a-col :span="4"> name: </a-col>
      <a-col :span="20">
        <a-input style="width: 100%" @input="nameChange" />
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="4" v-if="viewType">
        {{ name }}
      </a-col>
      <a-col :span="16">
        <div v-if="data.type == 'bool'">
          <a-switch :defaultChecked="data.value" @change="inputChange" />
        </div>
        <div v-else-if="data.type == 'int'">
          <a-input-number
            :defaultValue="data.value"
            style="width: 100%"
            @change="inputChange"
          />
        </div>
        <div v-else-if="data.type == 'float'">
          <a-input-number
            :defaultValue="data.value"
            style="width: 100%"
            @change="inputChange"
            :step="0.1"
          />
        </div>
        <div v-else-if="data.type == 'ref'">
          <a-input
            :defaultValue="data.value"
            style="width: 100%"
            @change="inputChange"
          />
        </div>
        <div v-else-if="data.type == 'str'">
          <a-input
            :defaultValue="data.value"
            style="width: 100%"
            @input="lineChange"
          />
        </div>
        <div v-else-if="data.type == 'tuple'">
          <a-input
            :defaultValue="data.value"
            @input="tupleChange"
            style="width: 100%"
          />
        </div>
      </a-col>
      <a-col :span="4">
        <a-select :default-value="data.type" @change="handleTypeChange">
          <a-select-option
            v-for="(tpvalue, key) in typeOptions"
            :key="key"
            :value="tpvalue"
            >{{ tpvalue }}
          </a-select-option>
        </a-select>
      </a-col>
    </a-row>
    <a-row><a-alert v-if="alertValue" :message="alertValue" banner /></a-row>
  </div>
</template>

<script>
export default {
  name: 'Parameter',
  props: {
    viewType: {
      default: true,
      type: Boolean,
    },
    type: {
      default: 'str',
      type: String,
    },
    name: {
      default: '',
      type: String,
    },
    value: null,
  },
  data() {
    return {
      typeOptions: ['int', 'float', 'bool', 'str', 'tuple'],
      data: {
        type: this.type,
        name: this.name,
        value: this.value,
      },
      alertValue: '',
    }
  },
  methods: {
    emitOut() {
      this.$emit('emitValue', {
        type: this.data.type,
        name: this.data.name,
        value: this.data.value,
      })
    },
    inputChange(value) {
      // console.log("on emit", value);
      this.data.value = value
      this.emitOut()
    },
    tupleChange(value) {
      value = value.target.value
      this.data.value = value
      const tupleregex = /^\([0-9,]+\)$/gm
      let regexRet = tupleregex.exec(value)
      if (regexRet != null) {
        this.emitOut()
        this.alertValue = ''
      } else {
        this.alertValue = 'tuple format: ([0-9,]).'
      }
    },
    lineChange(value) {
      this.data.value = value.target.value
      this.emitOut()
    },
    nameChange(value) {
      this.data.name = value.target.value
      this.emitOut()
    },
    handleTypeChange(value) {
      // console.log("handle change",value)
      switch (value) {
        case 'int':
          this.data.value = 0
          break
        case 'float':
          this.data.value = 0
          break
        case 'str':
          this.data.value = ''
          break
        case 'bool':
          this.data.value = false
          break
        default:
          break
      }
      this.data.type = value
    },
  },
  emits: ['emitValue', 'update:value'],
}
</script>
