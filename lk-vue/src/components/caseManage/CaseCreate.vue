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
              <div class="el-upload__tip">仅支持上传xlsx, xls格式</div>
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
                  <el-col :span="16">
                    <el-transfer
                        :data="item.cols"
                        :titles="['Labels', 'Targets']"
                        filterable
                        v-model="item.rightData"
                        :left-defaults="item.leftData"
                        :right-defaults="item.rightData"
                        :button-texts="['选择为x', '选择为y']"
                    />
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="6">
                    <el-radio label="是否是最终的输出结果" v-model="item.isOutput"/>
                  </el-col>
                </el-row>
              </div>

              <div v-if="item.fileType === 'image'">
                <el-row>
                  <el-col :span="6">
                    <el-radio label="是否是最终的输出结果" v-model="item.isOutput"/>
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
import {elTransferConvert} from "@/script/utils";

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
      txtRules: {
        cname: [{required: true, message: "请输入批次名称"}],
        fileType: [{required: true, message: "请选择需要上传的文件类型"}],
        tabularType: [{required: false, message: "请选择任务类型"}],
        imageType: [{required: false, message: "请选择任务类型"}]
      },
      configForm: [],
      processOne: false,
      processTwo: false,
      processThree: false,
      forceStop: false,
      deleteMode: "",
    }
  },
  computed: {
    updatedTxtRules() {
      this.txtRules = {
        cname: [{required: true, message: "请输入批次名称"}],
        fileType: [{required: true, message: "请选择需要上传的文件类型"}],
        tabularType: [{required: !["image", ""].includes(this.createForm.fileType), message: "请选择任务类型"}],
        imageType: [{required: !["tabular", ""].includes(this.createForm.fileType), message: "请选择任务类型"}]
      }
    },
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
      ipt = elTransferConvert(ipt)
      axios.post("http://localhost:9000/cases/create/logic", ipt, {
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(resp => {
        let res = resp.data
        if (res.code === 1) {
          this.boxInfo.title = "提示"
          this.boxInfo.re_direct = "/manage"
          this.boxInfo.msg = "逻辑关系提交成功"
          this.boxVisible = true
          this.processThree = true
        } else {
          this.boxInfo.title = "提示"
          this.boxInfo.msg = res.msg
          this.boxVisible = true
        }
      })
    },
    uploadSuccess(resp, file) {
      const data = resp.data
      const filename = data.pop()
      let msg = "文件上传成功"
      if (resp.code === 1) {
        if (["xlsx", "xls"].includes(filename.slice(filename.lastIndexOf('.') + 1))) {
          let cols = []
          data.forEach(item => {
            cols.push({key: item, label: item})
          })
          const item = {
            cid: this.cid,
            fileName: filename,
            cols: cols,
            fileType: "tabular",
            isOutput: false,
            leftData: [],
            rightData: []
          }
          this.configForm.push(item)
          this.processTwo = true
        } else {
          const item = {
            cid: this.cid,
            fileName: filename,
            fileType: "image",
            isOutput: false,
            leftData: [],
            rightData: [],
            cols: []
          }
          this.configForm.push(item)
          this.processTwo = true
        }
      } else {
        msg = "上传文件失败"
      }
      this.boxInfo.title = "提示"
      this.boxInfo.msg = msg
      this.boxVisible = true
    },
    uploadFailed(err) {
      this.boxInfo.title = "提示"
      this.boxInfo.msg = "文件上传失败"
      this.boxVisible = true
    }
    ,
    uploadDelete(file, fileList) {
      file = JSON.parse(JSON.stringify(file))
      let ipt = {filePath: file.name, mode: this.deleteMode}
      axios.post("http://localhost:9000/oss/delete/", ipt).then(resp => {
        let res = resp.data
        if (res.code === 1) {
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