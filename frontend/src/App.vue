<template>
  <div id="app">
    <!-- <a-modal :visible="true" title="Basic Modal" > -->
      <!-- <FileBox/> -->
      <!-- <Test/> -->
    <!-- </a-modal> -->
    <a-layout style="height=fullHeight">
      <a-layout-header style="background:#f0f2f5"
        ><a-page-header
          style="border: 1px solid rgb(235, 237, 240)"
          title="RxImg"
          sub-title="Reactive image processing"
        >
          <template slot="extra">
            <span key="1"> name:    </span>
              
            <edit-select key="2"/>
            <a-radio-group key="3" @change="radioChange">
              <a-radio-button value="element">Element</a-radio-button>
              <a-radio-button value="observer">Observer</a-radio-button>
              <a-radio-button value="relations">Relations</a-radio-button>
              <a-radio-button value="viewer">Viewer</a-radio-button>
            </a-radio-group>
            <!-- <a-button key="1" type="primary">
              Setting
            </a-button> -->
          </template>

        </a-page-header>
      </a-layout-header>
      <a-layout-content>

            <a-row :gutter="8">
               <a-col  :span="colShow.element ? colSpan : 0">
                <Element
                  class="main-box-border"
                  :style="{ height: clientHeight * 0.85 + 'px' }"
                />
              </a-col>
              <a-col  :span="colShow.observer ? colSpan : 0">
                <Observer
                  class="main-box-border"
                  :style="{ height: clientHeight * 0.85 + 'px' }"
                />
              </a-col>
              <a-col  :span=" colShow.relations ? colSpan : 0">
                <Relations
                  class="main-box-border"
                  :style="{ height: clientHeight * 0.85 + 'px' }"
                />
              </a-col>
              <a-col  :span="colShow.viewer ? colSpan : 0">
                <Viewer
                  class="main-box-border"
                  :style="{ height: clientHeight * 0.85 + 'px' }"
                />
              </a-col>
            </a-row>
          <!-- </div>
        </template> -->
      </a-layout-content>
      <a-layout-footer style="text-align: center;">copyright</a-layout-footer>
    </a-layout>

  </div>
</template>

<script>
import Relations from "./components/RelationsBox.vue";
import Viewer from "./components/ViewBox.vue";
import Observer from "./components/ObserversBox.vue";
import Element from "./components/ElementsBox.vue";
import { mapActions,} from "vuex";
import editSelect from './components/stateless/editSelect.vue'

import VueDraggableResizable from "vue-draggable-resizable";
import FileBox from "./components/toolbox/FileBox.vue"
export default {
  components: { Relations, Viewer, Observer, Element,editSelect},
  name: "App",
  // mounted() {
  //   window.onresize = () => {
  //     return (() => {
  //       this.fullHeight = document.documentElement.clientHeight;
  //       console.log(this.fullHeight);
  //     })();
  //   };
  // },
  // components: {
  //   HelloWorld
  // }
  data() {
    return {
      clientHeight: document.body.clientHeight,
      width: 0,
      height: 0,
      x: 0,
      y: 0,
      colShow:{
        element:true,
        observer:true,
        relations:true,
        viewer:true
      },
      
    };
  },
    created: function() {
  // created: function() {
    this.initStore();
    // console.log('so emit')
  // },
  },
  mounted() {
    // const that = this
    window.onresize = () => {
      return (() => {
        // window.screenHeight = document.body.clientHeight
        this.clientHeight = document.body.clientHeight;
        // console.log(that.clientHeight)
      })();
    };
  },
  watch: {
    clientHeight(val) {
      if (!this.timer) {
        this.clientHeight = val;
        this.timer = true;
        let that = this;
        setTimeout(function() {
          // 打印screenWidth变化的值
          console.log(that.clientHeight);
          that.timer = false;
        }, 400);
      }
    },
  },
  computed:{
    colSpan:function () {
      var num =0
      for (let key in this.colShow){
        if (this.colShow[key]==true){
          num = num+1
        }
      }
      
      return 24/num
    }
  },
  methods: {
    onResize: function(x, y, width, height) {
      this.x = x;
      this.y = y;
      this.width = width;
      this.height = height;
    },
    onDrag: function(x, y) {
      this.x = x;
      this.y = y;
    },
    ...mapActions(["initStore"]),
    radioChange({target}) {
      let value = target.value
      this.colShow[value] = !this.colShow[value]
        console.log('radio change:',value)
    }
  },

};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

h1 {
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}


/* div.main {
  padding: 10px;
} */
/* .app >>> .ant-row > div {
  background: transparent;
  border: 0;
} */
/* .gutter-box {
  background: #00a0e9;
  padding: 5px 0;
} */
.main-box-border {
  padding: 10px;
  box-shadow: 0px 6px 16px 0px rgba(0, 0, 0, 0.08);
  /* min-height: 600px; */
  border-radius: 2px;
  background: white;
  overflow-y:auto;
  /* height: 100%; */
}

div::-webkit-scrollbar {
    width: 10px;     
    height: 1px;
}
div::-webkit-scrollbar-thumb {
    border-radius: 2px;
    background: #cad0d6;
    
}
div::-webkit-scrollbar-track {
    border-radius: 2px;
    background:transparent;
}
/* a-col.relation-box { */
/* min-height: 600px; */
/* } */
</style>
