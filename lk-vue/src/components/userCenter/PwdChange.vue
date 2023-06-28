<template>
  <div class="container">
    <el-form :model="pwdForm">
      <el-form-item label="原密码">
        <el-input
            v-model="pwdForm.oriPwd"
            placeholder="请输入现在的密码"
            size="default"
        ></el-input>
      </el-form-item>
      <el-form-item label="新密码">
        <el-input
            v-model="pwdForm.newPwd"
            placeholder="请输入新密码"
            size="default"
        ></el-input>
      </el-form-item>
      <el-form-item label="再次输入">
        <el-input
            v-model="rePwd"
            placeholder="请再次输入新密码"
            size="default"
        ></el-input>
      </el-form-item>
    </el-form>

    <el-button size="default" type="primary" style="width: 30%;" @click="submitChange">提交</el-button>
    <MessageBox class="msgBox" :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"></MessageBox>
  </div>
</template>


<script>
import MessageBox from "@/components/MessageBox.vue";
import axios from "axios";

export default {
  name: "pwdChange",
  components: {MessageBox},
  data() {
    return {
      pwdForm: {
        oriPwd: "",
        newPwd: "",
      },
      rePwd: "",
      boxVisible: false,
      boxInfo: {title: "", msg: "", re_direct: ""},
    }
  },
  methods: {
    submitChange() {
      let flag = true
      if (this.pwdForm.newPwd !== this.rePwd) {
        this.boxInfo.title = "提交失败"
        this.boxInfo.msg = "两次输入的密码不一致"
        this.boxVisible = true
        flag = false
      }
      if (this.pwdForm.newPwd === "") {
        this.boxInfo.title = "提交失败"
        this.boxInfo.msg = "密码不能为空"
        this.boxVisible = true
        flag = false
      }

      if (flag) {
        let ipt = JSON.parse(JSON.stringify(this.pwdForm))
        axios.post("http://localhost:9000/uc/changePwd", ipt).then(resp => {
          const res = resp.data
          console.log(res)
          if (res.code === 1) {
            this.boxInfo.title = "修改成功"
            this.boxInfo.msg = "点击确定键跳转到首页"
            this.boxInfo.re_direct = "/home/show"
            this.boxVisible = true
          } else if (res.code === -1) {
            this.boxInfo.title = "注册失败"
            this.boxInfo.msg = res.message
            this.boxVisible = true
          }
        })
      }
    },
    closeMsgBox() {
      this.boxVisible = false
    }
  }
}
</script>

<style scoped>
.msgBox {
  display: flex;
  flex-direction: column;
  margin: 0 !important;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-height: calc(100% - 30px);
  max-width: calc(100% - 30px);
}

.el-dialog__body {
  flex: 1;
  overflow: auto;
}
</style>