<template>
  <div>
    <li>
      <a>{{ currentDir }}</a>
      <a type="float:right">
        <a-switch checked-children="hidden" default-checked />
      </a>
    </li>
    <a-list item-layout="horizontal">
      <RecycleScroller
        v-infinite-scroll="handleInfiniteOnLoad"
        style="height: 320px"
        :items="items.slice(0, index)"
        :item-size="32"
        key-field="value"
        :infinite-scroll-disabled="busy"
        :infinite-scroll-distance="10"
      >
        <a-list-item slot-scope="{ item }" @click="fetchFiles(item.value, item.type)">
          <a-icon :type="item.type" />
          <li type="float:left" >{{ item.value }}</li>
        
          <a-button 
            v-if="item.type!='rollback'" 
            icon="plus" 
            @click.stop="setDirText(item.value)"
            size="small"> 
          </a-button>
        </a-list-item>
      </RecycleScroller>
    </a-list>
        <a-input-search v-model="dirText" placeholder="input dir" size="small" @search="addDirTexts">
      <a-button slot="enterButton">
        <a-icon type="plus" />
      </a-button>
    </a-input-search>
    <a-list item-layout="horizontal" style="height: 96px">
        <a-list-item v-for="(text,index) in retDirTexts" :key=index>
          <li >{{ text }}</li>
        </a-list-item>
    </a-list>
  </div>
</template>

<script>

import infiniteScroll from "vue-infinite-scroll";
import { RecycleScroller } from "vue-virtual-scroller";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";
import { mapActions, mapGetters } from "vuex";

export default {
  name: "FileBox",
  directives: { infiniteScroll },
  components: {
    RecycleScroller,
  },
  data() {
    return {
      currentDir: "~",
      files: [],
      index: 15,
      loading: false,
      busy: false,
      page: 10,
      isHiddenFile: true,
      dirText:"",
      retDirTexts:[],
    };
  },
  computed: {
    items: function() {
      let allFiles = this.files;
      // console.log('len allFiles',allFiles.length)
      if (this.isHiddenFile) {
        allFiles = this.files.filter(function(item) {
          // console.log('length',item.value,item.value[0] != "." ,item.value=='..',(item.value[0] != ".") | (item.value=='..'))
          if ((item.value[0] != ".") | (item.value == "..")) {
            return true;
          }
        });
      }
      // console.log('len allFiles',allFiles.length,allFiles)
      return allFiles;
    },
    // ...mapGetters(["fileLists"]),
  },
  watch:{
    retDirTexts(val){
      console.log("sendArg",val);
      this.$emit("sendArgData",val)
    }
  },

  mounted: function() {
    this.getFileList({
      type: "init",
    }).then((v) => {
      this.files = v["data"];
      this.currentDir = v["origin"];
    });
  },
  methods: {
    ...mapActions(["getFileList"]),
    fetchFiles(dir_, type) {
      if (type != "file") {
        this.getFileList({
          dir: dir_,
          origin: this.currentDir,
        }).then((v) => {
          this.files = v["data"];
          this.currentDir = v["origin"];
        });
      }
    },
    handleInfiniteOnLoad() {
      if (this.index < this.items.length) {
        this.index += this.page;
      }
    },
    setDirText(text){
      this.dirText =this.currentDir+'/'+text 
    },
    addDirTexts(text){
      this.retDirTexts.push(text)
    }
  },
};
</script>
<style></style>
