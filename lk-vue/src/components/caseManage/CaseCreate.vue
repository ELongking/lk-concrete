<template>
  <div>
    <h3>批次创建-描述</h3>
    <el-form
        :rules="txtRules"
        ref="createForm"
        :model="createForm"
    >
      <el-row>
        <el-col :span="8">
          <el-form-item prop="cname" label="批次名称: " label-width="160px" class="item">
            <el-input
                size="default"
                type="text"
                v-model="createForm.cname"
                autocomplete="off"
                placeholder="请输入批次名称"
            />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="12">
          <el-form-item prop="fileType" label="上传文件类型: " label-width="160px" class="item">
            <el-radio-group v-model="createForm.fileType">
              <el-radio label="tabular" border>仅表格</el-radio>
              <el-radio label="image" border>仅图片</el-radio>
              <el-radio label="tni" border>图片和表格</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="10">
          <el-form-item label="表格任务类型: " label-width="160px" class="item">
            <el-radio-group
                :disabled="createForm.fileType === 'image'"
                v-model="createForm.tabularType"
            >
              <el-radio label="cls" border>分类</el-radio>
              <el-radio label="reg" border>回归</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>

        <el-col :span="10">
          <el-form-item label="图像任务类型: " label-width="160px" class="item">
            <el-radio-group
                :disabled="createForm.fileType === 'tabular'"
                v-model="createForm.imageType"
            >
              <el-radio label="cls" border>分类</el-radio>
              <el-radio label="det" border>检测</el-radio>
              <el-radio label="seg" border>分割</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>

    <el-button size="default" type="primary" style="width: 20%;" @click="submitForm">提交</el-button>

    <el-divider/>

    <div v-if="processOne">
      <h3>批次创建-文件</h3>
      <el-row>
        <el-col :span="8">
          <el-upload
              v-if="createForm.fileType !== 'image'"
              action="http://localhost:9000/oss/upload/tabular"
              accept=".xlsx,.xls,.xls"
              name="file"
              :on-success="uploadSuccess"
              :on-error="uploadFailed"
          >
            <el-button type="primary">点击上传表格文件</el-button>
            <template #tip>
              <div class="el-upload__tip">仅支持上传xlsx, xls格式</div>
            </template>
          </el-upload>
        </el-col>

        <el-col :span="8">
          <el-upload
              v-if="createForm.fileType !== 'tabular'"
              action="http://localhost:9000/oss/upload/image"
              accept=".zip,.rar,.7z"
              name="file"
              :on-success="uploadSuccess"
              :on-error="uploadFailed"
          >
            <el-button type="primary">点击上传图片和标注文件</el-button>
            <template #tip>
              <div class="el-upload__tip">仅支持压缩包上传</div>
            </template>
          </el-upload>
        </el-col>
      </el-row>
    </div>

    <el-divider/>


    <div v-if="processTwo">
      <h3>批次创建-关系</h3>

      <el-form
          ref="configForm"
          :model="configForm"
      >
        <div>
          <el-tabs>
            <el-tab-pane v-for="(item, index) in configForm" :label="item.name">
              <div v-if="item.type === 'tabular'">
                <span>表格数据逻辑(若发现列名出现问题, 则请删除并重新导入)</span>
                <el-transfer
                    :data="item.cols"
                    v-model="item.cols"
                    :titles="['Labels', 'Targets']"
                />
                <span>是否为输出的结果</span>
                <el-radio label="true" v-model="item.output"></el-radio>
              </div>

              <div v-if="item.type === 'image'">
                <span>是否为输出的结果</span>
                <el-radio label="true" v-model="item.output"></el-radio>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-form>
    </div>

    <MessageBox :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"></MessageBox>
  </div>
</template>

<script>
import axios from "axios";
import MessageBox from "@/components/MessageBox.vue";
import {readXlsx} from "@/script/excel";

export default {
  name: "CaseCreate",
  components: {MessageBox},
  data() {
    return {
      cid: "",
      createForm: {
        cname: "",
        fileType: "",
        tabularType: "",
        imageType: "",
      },
      boxVisible: false,
      boxInfo: {title: "", msg: "", re_direct: ""},
      txtRules: {
        cname: [{required: true, message: "请输入批次名称"}],
        fileType: [{required: true, message: "请选择需要上传的文件类型"}],
      },
      configForm: [],
      processOne: true,
      processTwo: true,
      processThree: false,
    }
  },
  methods: {
    submitForm() {
      this.$refs["createForm"].validate(condition => {
        if (condition) {
          let ipt = JSON.parse(JSON.stringify(this.createForm))
          axios.post("http://localhost:9000/cases/create", ipt).then(resp => {
            const res = resp.data
            if (res.code === 1) {
              this.boxInfo.title = "提示"
              this.boxInfo.msg = "描述提交成功"
              this.boxVisible = true
              this.processOne = true
              this.cid = res.data
            } else {
              this.boxInfo.title = "提示"
              this.boxInfo.msg = res.msg
              this.boxVisible = true
            }

          })
        }
      })
    },
    uploadSuccess(resp, file) {
      const filename = resp.data
      let msg = "文件上传成功"
      if (["xlsx", "xls"].includes(filename.slice(filename.lastIndexOf('.') + 1))) {
        const res = readXlsx(file)
        console.log("res = " + res)
        if (res.flag) {
          let cols = []
          for (let col in res.headers) {
            let ans = {key: "", label: "", disabled: false}
            ans.key = col
            ans.label = col
            cols.push(ans)
          }
          console.log("cols = " + cols)
          this.configForm.push({name: filename, cols: cols, type: "tabular", output: false})
        } else {
          msg = "表格数据无法读取, 请手动删除已上传的文件"
        }
      } else {
        this.configForm.push({name: filename, type: "tabular", output: false})
      }
      this.boxInfo.title = "提示"
      this.boxInfo.msg = msg
      this.boxVisible = true
    },
    uploadFailed(err, resp, file) {
      this.boxInfo.title = "提示"
      this.boxInfo.msg = "文件上传失败, 错误 => " + err
      this.boxVisible = true
    },
    uploadDelete(mode) {
      axios.post("http://localhost:9000/oss/delete/" + mode).then(resp => {
      })
    },
    closeMsgBox() {
      this.boxVisible = false
    },
  }
}
</script>

<style scoped>

</style>