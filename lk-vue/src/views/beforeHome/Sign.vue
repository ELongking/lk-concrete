<template>
  <div class="signContainer">
    <el-form
        :rules="rules"
        ref="signForm"
        element-loading-text="Login Loading..."
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        :model="signForm">
      <h3 class="signTitle">用户注册</h3>
      <el-form-item prop="username" label="Username: " label-width="30px" class="item">
        <el-input
            size="default"
            type="text"
            v-model="signForm.username"
            autocomplete="off"
            placeholder="请输入用户名"
        ></el-input>
      </el-form-item>

      <el-form-item prop="password" label="Password: " label-width="30px" class="item">
        <el-input
            size="default"
            type="password"
            v-model="signForm.password"
            autocomplete="off"
            placeholder="请输入密码"
            v-on:keyup="strengthShow()"
        ></el-input>
        <el-row>
          <el-col :span="6" id="weak">弱</el-col>
          <el-col :span="6" id="middle">中</el-col>
          <el-col :span="6" id="strong">强</el-col>
        </el-row>
      </el-form-item>

      <el-form-item prop="rePassword" label="re-Password: " label-width="30px" class="item">
        <el-input
            size="default"
            type="password"
            v-model="rePassword"
            autocomplete="off"
            placeholder="请重新输入密码"
        ></el-input>
      </el-form-item>

      <el-button size="default" type="primary" style="width: 30%;" @click="submitSign">Sign In</el-button>
    </el-form>

    <MessageBox class="msgBox" :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"></MessageBox>

  </div>
</template>

<script>
import MessageBox from "@/components/MessageBox.vue"
import $ from "jquery"
import axios from "axios";

export default {
  name: "Sign",
  components: {
    MessageBox
  },
  data() {
    return {
      boxVisible: false,
      boxInfo: {title: "", msg: "", re_direct: ""},
      rePassword: "",
      signForm: {
        username: "",
        password: "",
      },
      rules:{
        username: [{required: true, message: "请输入用户名"}],
        password:[{required: true, message: "请输入密码"}],
        rePassword:[{required: true, message:"请重复输入一次密码"}]
      }
    }
  },
  methods: {
    submitSign() {
      if (this.signForm.password !== this.rePassword) {
        this.boxInfo.title = "注册失败"
        this.boxInfo.msg = "两次输入的密码不一致"
        this.boxVisible = true
        return false
      }

      this.$ref["signForm"].validate(condition => {
        if (condition) {
          let ipt = JSON.parse(JSON.stringify(this.signForm))
          axios.post("http://localhost:9000/enter/sign", ipt).then(resp => {
            if (resp.data.code === 1) {
              this.boxInfo.title = "注册成功"
              this.boxInfo.msg = "点击确定键跳转到登录页"
              this.boxInfo.re_direct = "/login"
              this.boxVisible = true
            } else if (resp.data.code === -1) {
              this.boxInfo.title = "注册失败"
              this.boxInfo.msg = resp.data.msg
              this.boxVisible = true
            }
          })
        } else {
          this.boxInfo.title = "注册失败"
          this.boxInfo.msg = "请检查注册输入或稍后再试"
          this.boxVisible = true
        }
      })
    },
    strengthShow() {
      const weakReg = /^[0-9]{6,16}$|^[a-zA-Z]{6,16}$/;
      const mediumReg = /^[A-Za-z0-9]{6,16}$/;
      const strongReg = /^\w{6,16}$/;

      const password = this.signForm.password;
      if (null !== password) {
        if (password.length >= 6 && password.length <= 16) {
          if (password.match(weakReg)) {
            $('#weak').css('borderTopColor', 'yellow');
          } else if (password.match(mediumReg)) {
            $('#weak').css('borderTopColor', 'yellow');
            $('#middle').css('borderTopColor', 'blue');
          } else if (password.match(strongReg)) {
            $('#weak').css('borderTopColor', 'yellow');
            $('#middle').css('borderTopColor', 'blue');
            $('#strong').css('borderTopColor', 'green');
          }
        } else {
          $('#weak').css('borderTopColor', 'gainsboro');
          $('#middle').css('borderTopColor', 'gainsboro');
          $('#strong').css('borderTopColor', 'gainsboro');
        }
      }
    },
    closeMsgBox() {
      this.boxVisible = false
    },
  },
}
</script>

<style scoped>

.signContainer {
  border-radius: 5%;
  margin: 30vh 30vw;
  background: linear-gradient(to bottom, #afafaf, #e5e5e5);
  height: auto;
  text-align: center;
}

.signTitle {
  margin: 40px auto 20px auto;
  text-align: center;
  color: #505458;
}

#weak,
#middle,
#strong {
  display: inline-block;
  height: 15px;
  width: 48px;
  border-top: 4px solid gainsboro;
  margin-left: 3px;
  font-size: 12px;
  text-align: center;
}

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