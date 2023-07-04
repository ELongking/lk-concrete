<template>
  <div class="container">
    <h3>批次管理</h3>

    <el-table :data="allData" style="width: 100%;" empty-text="暂无批次, 请创建新批次。">
      <el-table-column prop="cid" label="批次编号" minWidth="10%"/>
      <el-table-column prop="cname" label="批次名称" minWidth="10%"/>
      <el-table-column prop="fileType" label="文件类型" minWidth="15%"/>
      <el-table-column prop="taskType" label="任务类型" minWidth="15%"/>
      <el-table-column prop="createTime" label="创建时间" minWidth="15%"/>
      <el-table-column prop="lastModify" label="最后修改时间" minWidth="15%"/>
      <el-table-column prop="isTrained" label="是否训练" minWidth="15%"/>
      <el-table-column fixed="right" label="操作" minWidth="15%">
        <template #default="scope">
          <el-button type="primary" size="small" @click="caseDetails(scope.row)">详情</el-button>
          <el-button type="primary" size="small" @click="caseDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>

    </el-table>

    <div class="pagination" style="margin-top: 50px">
      <el-row>
        <el-col :span="4"></el-col>
        <el-col :span="4">
          <el-button :disabled="nowPage === 1" @click="() => {pageShow(nowPage - 1); nowPage--}">&lt;</el-button>
        </el-col>
        <el-col :span="4">
          <el-button :disabled="nowPage === sumPage" @click="() => {pageShow(nowPage + 1); nowPage++}">&gt;</el-button>
        </el-col>
        <el-col :span="6">
          <el-select @change="pageDirect" placeholder="选择页码跳转">
            <el-option v-for="idx in sumPage" :label="idx" :value="idx"/>
          </el-select>
        </el-col>
        <el-col :span="4"></el-col>
      </el-row>
    </div>

    <MessageBox :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"></MessageBox>

  </div>
</template>

<script>
import axios from "axios";
import {timeFormatConvert} from "@/script/utils";
import MessageBox from "@/components/MessageBox.vue";

export default {
  name: "CaseShow",
  components: {MessageBox},
  data() {
    return {
      allData: [],
      nowPage: 1,
      sumPage: 0,
      boxVisible: false,
      boxInfo: {title: "", msg: "", re_direct: ""},
      fileToHans: {"tabular": "数据表格", "image": "图像", "tni": "表格+图像"},
      taskToHans: {"cls": "分类", "reg": "回归", "det": "检测", "seg": "分割"},
      boolToHans: {1: "是", 0: "否"}
    }
  },
  created() {
    this.pageShow(this.nowPage)
  },
  methods: {
    pageShow(p) {
      axios.get("http://localhost:9000/cases/page/" + p).then(resp => {
        let res = resp.data
        if (res.code === 1) {
          this.sumPage = res.data.pages
          this.allData = res.data.list
          this.allData.forEach(item => {
            item.createTime = timeFormatConvert(item.createTime)
            item.lastModify = timeFormatConvert(item.lastModify)
            item.fileType = this.fileToHans[item.fileType]

            let tabType = this.taskToHans[item.tabularType], imgType = this.taskToHans[item.imageType]
            if (tabType === undefined) {
              tabType = "None"
            }
            if (imgType === undefined) {
              imgType = "None"
            }
            item.taskType = tabType + "/" + imgType
            item.isTrained = this.boolToHans[item.isTrained]
          })
        }
      })
    },
    pageDirect(val){
      this.pageShow(val)
      this.nowPage = val
    },
    caseDetails() {

    },
    caseDelete(row) {
      axios.post("http://localhost:9000/cases/delete/" + row.cid).then(resp => {
        let res = resp.data
        if (res.code === 1) {
          this.boxInfo.title = "删除成功"
          this.boxInfo.msg = "请点击返回"
          this.boxInfo.re_direct = "refresh"
          this.boxVisible = true
        } else {
          this.boxInfo.title = "删除失败"
          this.boxInfo.msg = res.msg
          this.boxVisible = true
        }
      })
    },
    closeMsgBox() {
      this.boxVisible = false
    }
  }
}
</script>

<style scoped>

</style>