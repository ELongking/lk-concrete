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
          <el-form-item prop="tabularType" label="表格任务类型: " label-width="160px" class="item">
            <el-radio-group
                :disabled="['image', ''].includes(this.createForm.fileType)"
                v-model="createForm.tabularType"
            >
              <el-radio label="cls" border>分类</el-radio>
              <el-radio label="reg" border>回归</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>

        <el-col :span="10">
          <el-form-item prop="imageType" label="图像任务类型: " label-width="160px" class="item">
            <el-radio-group
                :disabled="['tabular', ''].includes(this.createForm.fileType)"
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
              accept=".xlsx"
              name="file"
              :on-success="uploadSuccess"
              :on-error="uploadFailed"
              :on-remove="uploadDelete"
          >
            <el-button type="primary" @click="this.deleteMode = 'tabular'">点击上传表格文件</el-button>
            <template #tip>
              <div class="el-upload__tip">仅支持上传xlsx格式</div>
            </template>
          </el-upload>
        </el-col>

        <el-col :span="8">
          <el-upload
              v-if="createForm.fileType !== 'tabular'"
              action="http://localhost:9000/oss/upload/image"
              accept=".zip"
              name="file"
              :on-success="uploadSuccess"
              :on-error="uploadFailed"
              :on-remove="uploadDelete"
          >
            <el-button type="primary" @click="this.deleteMode = 'image'">点击上传图片和标注文件</el-button>
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
            <el-tab-pane v-for="(item, index) in configForm" :label="item.fileName">
              <div v-if="item.fileType === 'tabular'">
                <el-row>
                  <el-col :span="12">
                    表格数据逻辑(若发现列名出现问题, 则请删除并重新导入)
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="24">
                    <el-table
                        :data="item.setting"
                        style="width: 85%; margin: auto">
                      <el-table-column prop="col" label="列名"/>

                      <el-table-column label="是否属于X集合">
                        <template #default="{row}">
                          <el-checkbox v-model="row.isX"/>
                        </template>
                      </el-table-column>

                      <el-table-column label="是否是类别列">
                        <template #default="{row}">
                          <el-checkbox v-model="row.isCat"/>
                        </template>
                      </el-table-column>

                      <el-table-column label="选择主体">
                        <template #default="{row}">
                          <el-select v-model="row.subject" :disabled="!row.isX">
                            <el-option
                                v-for="(col, col_index) in item.cols"
                                :key="col_index"
                                :label="col"
                                :value="col"/>
                          </el-select>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-col>
                </el-row>

              </div>

              <div v-if="item.fileType === 'image'">
                <el-row>
                  <el-col :span="24">
                    <el-select v-model="item.batchName" placeholder="选择是否与哪一批同属相同数据">
                      <el-option
                          v-for="(item, idx) in configForm"
                          :key="idx"
                          v-if="item.fileType === 'image'"
                          :label="item.fileName"
                          :value="item.fileName"
                      />
                    </el-select>
                  </el-col>
                </el-row>
              </div>

            </el-tab-pane>
          </el-tabs>
        </div>

        <el-button type="default" size="default" @click="submitLogic">逻辑关系提交</el-button>
      </el-form>
    </div>

    <MessageBox :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"/>
    <LeaveMessageBox
        :boxVisible="leaveBoxVisible"
        :info="leaveBoxInfo"
        @toNext="toNext"
        @toNow="toNow"
    />
  </div>
</template>

<script>
import axios from "axios";
import MessageBox from "@/components/MessageBox.vue";
import LeaveMessageBox from "@/components/LeaveMessageBox.vue";
import {getFileOriName, convertToStringArray} from "@/script/utils";

export default {
  name: "CaseCreate",
  components: {MessageBox, LeaveMessageBox},
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
      leaveBoxVisible: false,
      leaveBoxInfo: {title: "", msg: "", re_direct: ""},
      configForm: [],
      processOne: false,
      processThree: false,
      forceStop: false,
      deleteMode: "",
    }
  },
  computed: {
    txtRules: function () {
      return {
        cname: [{required: true, message: "请输入批次名称"}],
        fileType: [{required: true, message: "请选择需要上传的文件类型"}],
        tabularType: [{required: !["image", ""].includes(this.createForm.fileType), message: "请选择任务类型"}],
        imageType: [{required: !["tabular", ""].includes(this.createForm.fileType), message: "请选择任务类型"}]
      }
    },
    processTwo: function () {
      return this.configForm.length !== 0
    }
  },
  beforeRouteLeave(to, from, next) {
    if (!this.processThree && this.processOne) {
      this.leaveBoxInfo.title = "提示"
      this.leaveBoxInfo.msg = "您的数据并未完全提交, 是否仍离开该页面?"
      this.leaveBoxVisible = true
      this.toNext = () => {
        axios.post("http://localhost:9000/cases/delete/" + this.cid).then(() => {
        })
        next()
      }
      this.toNow = () => {
        next(false);
        this.leaveBoxVisible = false;
      }
    } else if (!this.processOne || this.processThree) {
      next()
    }
  },
  methods: {
    submitForm() {
      this.$refs["createForm"].validate(condition => {
        if (condition) {
          let ipt = JSON.parse(JSON.stringify(this.createForm))
          axios.post("http://localhost:9000/cases/create/intro", ipt).then(resp => {
            const res = resp.data
            if (res.code === 1) {
              this.boxInfo.title = "提示"
              this.boxInfo.msg = "描述提交成功"
              this.boxVisible = true
              this.processOne = true
              this.cid = res.data
              this.processOne = true
            } else {
              this.boxInfo.title = "提示"
              this.boxInfo.msg = res.msg
              this.boxVisible = true
            }

          })
        }
      })
    },
    submitLogic() {
      let ipt = JSON.parse(JSON.stringify(this.configForm))
      axios.post("http://localhost:9000/cases/create/logic", ipt, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(resp => {
        let res = resp.data
        if (res.code === 1) {
          this.boxInfo.title = "提示"
          this.boxInfo.re_direct = "/manage"
          this.boxInfo.msg = "逻辑关系提交成功, 点击返回主页"
          this.boxVisible = true
          this.processThree = true
          axios.post("http://localhost:9000/cases/detail/generate/", {cid: this.cid})
        } else {
          this.boxInfo.title = "提示"
          this.boxInfo.msg = res.msg
          this.boxVisible = true
        }
      })
    },
    uploadSuccess(resp, file) {
      const data = convertToStringArray(resp.data)
      const filename = data.pop()
      let msg = "文件上传和验证成功"
      if (getFileOriName(filename, "suffix") === "xlsx") {

        let setting = []
        data.forEach(col => {
          const _setting = {col: col, isX: true, isCat: false, subject: col}
          setting.push(_setting)
        })

        const item = {
          cid: this.cid,
          fileName: getFileOriName(filename, "name"),
          cols: data,
          fileType: "tabular",
          setting: setting,
        }
        this.configForm.push(item)
      } else {
        const number = data.pop()
        const exampleNames = data.slice(1)
        const item = {
          cid: this.cid,
          fileName: getFileOriName(filename, "name"),
          fileType: "image",
          batchName: getFileOriName(filename, "name"),
          number: number,
          exampleNames: exampleNames
        }
        this.configForm.push(item)
      }
      this.boxInfo.title = "提示"
      this.boxInfo.msg = msg
      this.boxVisible = true
    },
    uploadFailed(resp, file, fileList) {
      const error = JSON.parse(resp.message)
      this.boxInfo.title = "提示"
      this.boxInfo.msg = error.msg
      this.boxVisible = true
    }
    ,
    uploadDelete(file, fileList) {
      file = JSON.parse(JSON.stringify(file))
      let ipt = {filePath: file.name, mode: this.deleteMode}
      axios.post("http://localhost:9000/oss/delete/", ipt).then(resp => {
        let res = resp.data
        if (res.code === 1) {
          this.configForm = this.configForm.filter(item => item.fileName !== file.name)
          this.boxInfo.title = "提示"
          this.boxInfo.msg = "删除成功"
          this.boxVisible = true
          return true
        } else {
          this.boxInfo.title = "提示"
          this.boxInfo.msg = msg
          this.boxVisible = true
          return false
        }
      })
    },
    closeMsgBox() {
      this.boxVisible = false
    },
    toNext() {
    },
    toNow() {
    },
  }
}
</script>

<style scoped>

</style>