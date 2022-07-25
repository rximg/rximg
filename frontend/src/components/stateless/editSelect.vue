<template>
  <span>
    <template v-if="selectStatus">
      <a-select
        style="width: 128px"
        v-model:value="group"
        option-label-prop="label"
        @change="selectChange"
      >
        <template v-slot:dropdownRender="menu">
          <div>
            <v-nodes :vnodes="menu" />
            <a-divider style="margin: 4px 0" />
            <div
              style="padding: 4px 8px; cursor: pointer"
              @mousedown="(e) => e.preventDefault()"
              @click="switchToNewItem"
            >
              <plus-square-outlined /> New
            </div>
          </div>
        </template>
        <a-select-option
          class="delete-icon"
          :value="item"
          v-for="item in groupList"
          :key="item"
          :label="item"
        >
          {{ item }}
          <delete-outlined 
            style="position: absolute; top: 30%; right: 10%"
            @click.stop="deleteItem(item)"
          />
        </a-select-option>
      </a-select>
    </template>
    <template v-else>
      <a-input
        style="width: 128px"
        v-model:value="editNameValue"
        placeholder="enter a new name"
        @pressEnter="finishNewEdit"
      >
        <template v-slot:addonAfter>
          <enter-outlined @click="finishNewEdit"/>
        </template>
      </a-input>
    </template>
  </span>
</template>

<script>
import * as Vue from 'vue'
import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import axios from 'axios'
export default {
  name: 'editSelect',
  components: {
    VNodes: {
      functional: true,
      render: (h, ctx) => ctx.props.vnodes,
    },
  },

  data() {
    return {
      selectStatus: true,
      groupListValue: undefined,
      groupValue: undefined,
      editNameValue: '',
    }
  },
  computed: {
    ...mapState({
      configNamesX: (state) => state.confignames,
    }),
    // ...mapGetters(["currentConfigName","configNames"])
    group: {
      get: function () {
        if (this.groupValue == undefined) {
          // this.groupList = this.configNamesX.names
          return this.configNamesX.current
        } else {
          return this.groupValue
        }
      },
      set: function (value) {
        this.groupValue = value
      },
    },
    groupList: {
      get: function () {
        if (this.groupListValue == undefined) {
          return this.configNamesX.names
        } else {
          return this.groupListValue
        }
      },
      set: function (value) {
        this.groupListValue = value
      },
    },
  },
  // watch:{
  //   configNamesX: function(config){
  //     console.log("config",config)
  //     this.group = config.current
  //     this.groupList = config.names
  //   }
  // },
  // mouted(){
  // this.groupList = this.names
  // this.group = this.current
  // },
  methods: {
    ...mapActions(['setCurrentConfigNameAndReload']),
    async deleteItem(label) {
      let response = await axios.delete('api/config/' + label)
      if (response.data.type == 'success') {
        let groupList = this.groupList
        const index = groupList.indexOf(label)
        groupList.splice(index, 1)
        this.groupList = groupList
        //TODO 删除文件的bug。
      }
    },
    selectChange(value) {
      console.log('select change', value)
      this.setCurrentConfigNameAndReload(value)
    },
    switchToNewItem() {
      this.selectStatus = false
    },
    finishNewEdit() {
      let groupList = this.groupList
      groupList.splice(0, 0, this.editNameValue)
      this.groupList = groupList
      this.group = this.editNameValue
      this.selectStatus = true
      this.setCurrentConfigNameAndReload(this.group)
    },
  },
}
</script>

<style scoped>
.ant-input {
  width: 128px;
}
</style>
