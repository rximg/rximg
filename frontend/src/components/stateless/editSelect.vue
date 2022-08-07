<template>
  <span>
    <template v-if="selectStatus">
      <a-select style="width: 100%" v-model:value="taskname" option-label-prop="label" @change="selectChange">
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
        <a-select-option class="delete-icon" :value="item" v-for="item in CurrentStateStore.tasks" :key="item"
          :label="item">
          {{ item }}
          <delete-outlined style="position: absolute; top: 30%; right: 10%" @click.stop="deleteItem(item)" />
        </a-select-option>
      </a-select>
    </template>
    <template v-else>
      <a-input-group style="width: 100%" >
        <a-row >
          <a-col :span="18">
            <a-input style="width: 100%" v-model:value="editNameValue" placeholder="enter a new name"
              @pressEnter="finishNewEdit"></a-input>
          </a-col>
          <a-col :span="6">
            <a-button @click="finishNewEdit">Enter</a-button>
          </a-col>
        </a-row>
      </a-input-group>
    </template>
  </span>
</template>

<script setup lang="ts">
// import * as Vue from 'vue'
import { ref, computed } from 'vue'
import { CurrentStateStore, persistStoreFunc, localStorage } from '@/store'
// import { mapActions, mapGetters, mapState, mapMutations } from 'vuex'
import axios from 'axios'
const VNodes = (_, { attrs }) => {
  return attrs.vnodes;
}
const selectStatus = ref(true)
const groupListValue = ref(null)
const taskname = ref(localStorage.value.taskName || '')

const groupValue = ref("")
const editNameValue = ref("")
const deleteItem = async (label: string) => {
  let response = await axios.delete('api/config/' + label)
  if (response.data.type == 'success') {
    const index = CurrentStateStore.tasks.indexOf(label)
    CurrentStateStore.tasks.splice(index, 1)
  }
}
const switchToNewItem = () => {
  selectStatus.value = false
}

const setNewConfig = async (name: string) => {
  // let response = await axios.put(`api/config/${name}`)
  // await persistStoreFunc()
  localStorage.value.taskName = name

  location.reload(true)
}

const selectChange = (name: string) => {
  console.log('select change', name)
  localStorage.value.taskName = name

  location.reload(true)
}

const finishNewEdit = async () => {
  console.log('finish new edit', editNameValue.value)
  localStorage.value.taskName = editNameValue.value
  await axios.put(`api/config/${editNameValue.value}`)
  location.reload(true)
  selectStatus.value = true
}
</script>

<style scoped>
.ant-input {
  width: 128px;
}
</style>
