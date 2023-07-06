<template>
  <div class="container">
    <el-button @click="changeVisible">&lt;点击返回</el-button>

    <el-tabs type="border-card">
      <el-tab-pane label="基本信息">

      </el-tab-pane>
      <el-tab-pane label="数据概览">

        <el-tabs :tab-position="'left'" @tab-change="dataTabChange">
          <el-tab-pane v-for="(item, index) in jsonInfo" :label="item.fileName">
            <div class="dataDetails" v-if="item.fileType === 'tabular'">
              <el-row>
                <el-col :span="8">
                  <el-statistic title="总列数" :value="item.mean.length"></el-statistic>
                </el-col>
                <el-col :span="8">
                  <el-statistic title="X-列数" :value="item.xcols.length"></el-statistic>
                </el-col>
                <el-col :span="8">
                  <el-statistic title="Y-列数" :value="item.ycols.length"></el-statistic>
                </el-col>
              </el-row>

              <el-table :data="reFormatMs(item)" style="width: 100%;">
                <el-table-column prop="name" label="列名" minWidth="24%"/>
                <el-table-column prop="mean" label="平均值" minWidth="24%"/>
                <el-table-column prop="std" label="方差" minWidth="24%"/>
                <el-table-column prop="cats" label="种类" minWidth="24%"/>
              </el-table>

              <el-button-group>
                <el-button ref="boxPlotBtn" @click="boxPlot(item)">箱型图</el-button>
                <el-button @click="heatmapPlot(item)">热力图</el-button>
              </el-button-group>
              <div :id="'chart-' + index"
                   style="
                   height: 80vh;
                   width: 70vw;
                   display: flex;
                   justify-content: center;
                   margin: auto;"
              />
              
            </div>
          </el-tab-pane>
        </el-tabs>

      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import * as echarts from "echarts"
import {doBoxPlot, doHeatmapPlot} from "@/script/chartsPlot";

export default {
  name: "DetailCard",
  data() {
    return {
      chart: null
    }
  },
  props: {
    jsonInfo: {type: Array, required: true},
    baseInfo: {type: Array, required: false}
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById("chart-0"))
    },
    reFormatMs(item) {
      let res = []
      for (let n of item.xcols) {
        let _temp = {name: n, mean: 0, std: 0, cats: "X"}
        const index = item.cols.indexOf(n)
        _temp.mean = item.mean[index]
        _temp.std = item.std[index]
        res.push(_temp)
      }
      for (let n of item.ycols) {
        let _temp = {name: n, mean: 0, std: 0, cats: "Y"}
        const index = item.cols.indexOf(n)
        _temp.mean = item.mean[index]
        _temp.std = item.std[index]
        res.push(_temp)
      }
      return res
    },
    boxPlot(itemInfo) {
      this.chart.clear()
      this.chart.setOption(doBoxPlot(itemInfo))
    },
    heatmapPlot(itemInfo) {
      this.chart.clear()
      this.chart.setOption(doHeatmapPlot(itemInfo))
    },
    changeVisible() {
      this.$emit("toDetailVisible")
    },
    dataTabChange(tabName) {
      this.chart.dispose()
      console.log(tabName)
      const chartContainerId = 'chart-' + tabName;
      this.chart = echarts.init(document.getElementById(chartContainerId));
    }
  }
}
</script>

<style scoped>
.container {
  width: 100%;
}

.dataDetails {
  width: 100%;
}

</style>