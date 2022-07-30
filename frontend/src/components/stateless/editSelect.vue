<template>
  <span >
    <template v-if="selectStatus">
      <a-select style="width: 100%" v-model:value="CurrentStateStore.config.current" option-label-prop="label"
        @change="selectChange">
        <template #dropdownRender="{ menuNode: menu }">
          <div>
            <v-nodes :vnodes="menu" />
            <a-divider style="margin: 4px 0" />
            <div style="padding: 4px 8px; cursor: pointer" @mousedown="(e) => e.preventDefault()"
              @click="switchToNewItem">
              <plus-square-outlined /> New
            </div>
          </div>
        </template>
        <a-select-option class="delete-icon" :value="item" v-for="item in CurrentStateStore.config.names" :key="item"
          :label="item">
          {{ item }}
          <delete-outlined style="position: absolute; top: 30%; right: 10%" @click.stop="deleteItem(item)" />
        </a-select-option>
      </a-select>
    </template>
    <template v-else>
      <a-input style="width: 128px" v-model:value="editNameValue" placeholder="enter a new name"
        @pressEnter="finishNewEdit">
        <template #addonAfter>
          <enter-outlined @click="finishNewEdit" />
        </template>
      </a-input>
    </template>
  </span>
</template>

<script setup lang="ts">
// import * as Vue from 'vue'
import { ref, computed } from 'vue'
import { CurrentStateStore, persistStore } from '@/store'
// import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import axios from 'axios'
const VNodes = (_, { attrs }) => {
  return attrs.vnodes;
}
const selectStatus = ref(true)
const groupListValue = ref(null)

const groupValue = ref("")
const editNameValue = ref("")
const deleteItem = async (label: string) => {
  let response = await axios.delete('api/config/' + label)
  if (response.data.type == 'success') {
    const index = CurrentStateStore.config.names.indexOf(label)
    CurrentStateStore.config.names.splice(index, 1)
  }
}
const switchToNewItem = () => {
  selectStatus.value = false
}

const setNewConfig = async (name: string) => {
  let response = await axios.put(`api/config/${name}`)
  persistStore()
  location.reload(true)
}

const selectChange = (value: string) => {
  console.log('select change', value)
  setNewConfig(value)
}

const finishNewEdit = () => {
  CurrentStateStore.config.names.splice(0, 0, editNameValue.value)
  CurrentStateStore.config.current = editNameValue.value
  selectStatus.value = true
  setNewConfig(CurrentStateStore.config.current)
}
</script>

<style scoped>
.ant-input {
  width: 128px;
}
</style>
