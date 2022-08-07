<template>
  <div style="overflow-y: hidden">
    <!-- {{title}}{{title}} -->
    <div v-if="titleStr">
      <a-tag @click="swithTitle">{{ titleStr }}</a-tag>
    </div>
    <div v-else>
      <div v-if="winHeight" @mousewheel.prevent="scrollevent">
        <div
          v-bind:style="{ width: winWidth + 'px', height: winHeight + 'px' }"
          :id="'wrapper' + id"
        >
          <div v-show="pixShow">
            <div :id="'pixContainer' + id"></div>
          </div>
          <div v-show="!pixShow">
            <img :id="'imgContainer' + id" />
          </div>
          <!-- <button @click="state">click</button> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as Vue from 'vue'
//TODO imgmap左右移动，
import { Heatmap } from '@antv/g2plot'
import  { Image } from 'image-js'
import axios from 'axios'

// import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
// var readJson = require('read-package-json')
// import { data } from "./demo.js";
export default {
  name: 'NDArray',
  props: {
    winWidth: Number,
    title: String,
    id: String,
    apiurl: String,
    // imgurl: String,
  },
  data() {
    return {
      titleStr: this.title,
      winHeight: 0,
      pixShow: false,
      imgShape: {
        width: 0,
        height: 0,
        resizeRaito: 1,
      },
      imgHandle: Object,
      maxScale: -1,
      r_zoom: 1,
      pixshowGrid: 32,
      // imgData: ""
      // zoomStep: 10,
    }
  },
  // created() {

  // },
  watch: {
    winHeight: function () {
      this.imgHandle.then(this.procceImage)
    },
    // imgData:function(data){
    //   const imgHandle = Image.load(this.imgulr);
    //   this.imgHandle = imgHandle;
    //   imgHandle.then(this.getImageShape);
    // }
  },
  computed: {
    // pixShow: function () {
    //   return this.r_zoom <= 1;
    // },
    // ...mapGetters("views",["getNDArrayNormal"]),
    // imgData:function () {
    //   return this.getNDArrayNormal(this.id)
    // },
    imgurl: function () {
      let url = this.apiurl + '/ndarray/' + this.id
      console.log('imgurl', url)
      return url
    },
    zoomStep: function () {
      if (this.r_zoom <= 3) {
        return 0.2
      } else {
        return 1
      }
    },
  },
  methods: {
    // ...mapActions("views",["queryNDArray"]),
    swithTitle() {
      // console.log("imgurl",this.imgurl)
      this.titleStr = ''
      let imgurl = this.apiurl + '/ndarray/' + this.id
      console.log(imgurl, typeof imgurl)
      this.imgHandle = Image.load(imgurl)
      this.imgHandle.then(this.setImageHeight)
      // this.queryNDArray(this.id)
    },
    async getPix({ x, y, width, height }) {
      let imgPixurl = this.apiurl + '/ndarrayPix'
      // {x,y,width,height} = croppix

      let response = await axios.post(imgPixurl, {
        id: this.id,
        xmin: x,
        ymin: y,
        xmax: x + width,
        ymax: y + height,
      })
      this.heatmapPlot.update({
        data: response.data.data,
      })

      this.pixShow = true
    },

    scrollevent(event) {
      var delta = 0
      if (!event) event = window.event
      if (event.wheelDelta) {
        delta = event.wheelDelta / 120
        if (window.opera) delta = -delta
      } else if (event.detail) {
        delta = -event.detail / 3
      }
      // console.log('zoom delta',this.r_zoom,delta)
      this.r_zoom += delta * this.zoomStep
      // let r_zoom = this.maxScale / this.winWidth;
      let r_ow = this.imgShape.width / this.winWidth
      if (this.r_zoom >= this.maxScale) {
        this.r_zoom = this.maxScale
      } else if (this.r_zoom <= 1) {
        this.r_zoom = 1
      }
      var cropZero = {
        x: event.offsetX * r_ow * (1 - 1 / this.r_zoom),
        y: event.offsetY * r_ow * (1 - 1 / this.r_zoom),
        width: this.imgShape.width / this.r_zoom,
        height: this.imgShape.height / this.r_zoom,
      }
      if (this.r_zoom == this.maxScale) {
        this.getPix(cropZero)
      } else if (1 < this.r_zoom < this.maxScale) {
        // console.log(image,document.getElementById("result"))
        this.pixShow = false
        // let cropZero = [
        //   event.offsetX * r_ow * (1 - 1/this.r_zoom),
        //   event.offsetY * r_ow * (1 - 1/this.r_zoom),
        //   this.imgShape.width / this.r_zoom,
        //   this.imgShape.height / this.r_zoom,
        // ];
        this.imgHandle.then((image) => {
          document.getElementById('imgContainer' + this.id).src = image
            .crop(cropZero)
            .resize({
              width: this.winWidth,
              height: this.winHeight,
            })
            .toDataURL()
        })
      }
    },
    setImageHeight(img) {
      this.imgShape.width = img.width
      this.imgShape.height = img.height
      if (img.width > this.winWidth) {
        this.imgShape.resizeRaito = this.winWidth / img.width
      }
      this.winHeight = img.height * this.imgShape.resizeRaito
      this.maxScale = (this.imgShape.width * this.pixshowGrid) / this.winWidth
      this.r_zoom = 1
      console.log('init zoom scale', this.winHeight, this.maxScale, this.r_zoom)
    },
    procceImage(image) {
      // this.getImageShape(image)
      // console.log(image, document.getElementById("imgContainer"));
      document.getElementById('imgContainer' + this.id).src = image
        .resize({
          width: this.winWidth,
          height: this.winHeight,
        })
        .toDataURL()
      const heatmapPlot = new Heatmap(
        document.getElementById('pixContainer' + this.id),
        {
          xField: 'x',
          yField: 'y',
          xAxis: false,
          yAxis: false,
          colorField: 'v',
          color: ['#dddddd', '#9ec8e0', '#5fa4cd', '#2e7ab6', '#114d90'],
          tooltip: {
            fields: ['x', 'y', 'v'],
          },
          reflect: 'y',
          label: {
            formatter: (datum) => datum.format,
            style: {
              fill: '#fff',
              shadowBlur: 2,
              shadowColor: 'rgba(0, 0, 0, .45)',
              fontSize: 8,
            },
          },
          axis: false,
          data: {},
          autoFit: false,
          width: this.winWidth,
          height: this.winHeight,
        }
      )
      heatmapPlot.render()
      this.heatmapPlot = heatmapPlot
    },
  },
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
