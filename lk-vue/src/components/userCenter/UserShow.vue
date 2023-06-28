<template>
  <div>
    <el-row>
      <el-col :span="12">
        <el-statistic title="欢迎" :value="info.username"></el-statistic>
      </el-col>
      <el-col :span="12">
        <el-statistic title="上次登录时间" :value="timeStr"></el-statistic>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from "axios";
import {timeFormatConvert} from "@/script/utils"

export default {
  name: "UserShow",
  data() {
    return {
      info: {
        username: "",
        lastLogin: -1
      },
      timeStr: ""
    }
  },
  mounted() {
    console.log(this)
    this.homeShow()
  },
  methods: {
    homeShow() {
      axios.get("http://localhost:9000/uc/show").then(resp => {
        const res = resp.data;
        if (res.code === 1) {
          this.info.username = res.data.username
          this.info.lastLogin = res.data.lastLogin
          this.timeStr = timeFormatConvert(this.info.lastLogin)
        }
      })
    },
  }
}
</script>

<style scoped>

</style>