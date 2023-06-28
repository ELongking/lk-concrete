<template>
  <div class="loginContainer">
    <el-form
        :rules="rules"
        ref="loginForm"
        element-loading-text="Login Loading..."
        element-loading-spinner="el-icon-loading"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        :model="loginForm"
    >
      <h3 class="loginTitle">用户登录</h3>
      <el-form-item prop="username" label="Username: " label-width="30px" class="item">
        <el-input
            size="default"
            type="text"
            v-model="loginForm.username"
            autocomplete="off"
            placeholder="请输入用户名"
        ></el-input>
      </el-form-item>

      <el-form-item prop="password" label="Password: " label-width="30px" class="item">
        <el-input
            size="default"
            type="password"
            v-model="loginForm.password"
            autocomplete="off"
            placeholder="请输入密码"
        ></el-input>
      </el-form-item>

      <el-form-item prop="code" label="Verify Code: " label-width="30px" class="item">
        <el-input
            size="default"
            type="text"
            v-model="loginForm.code"
            autocomplete="off"
            placeholder="点击切换验证码"
            @keydown.enter.native="submitLogin"
        ></el-input>
        <img :src="codeImg" @click="updateVerifyCode" alt="" class="verifyImg">
      </el-form-item>
      <el-button size="default" type="primary" style="width: 30%;" @click="submitLogin">Login</el-button>
    </el-form>

    <el-button size="default" type="primary" style="width: 30%;" @click="toSign">Sign In</el-button>
    <MessageBox :boxVisible="boxVisible" :info="boxInfo" @closeMsgBox="closeMsgBox"></MessageBox>
  </div>
</template>

<script>
import axios from "axios";
import router from "@/router";
import MessageBox from "@/components/MessageBox.vue";

export default {
  name: "Login",
  components: {MessageBox},
  data() {
    return {
      codeUrl: "/enter/verifyCode?t=" + Math.random(),
      codeImg: "",
      loginForm: {
        username: "longking",
        password: "19980917",
        code: "",
      },
      checked: true,
      boxInfo: {title: "", msg: "", re_direct: ""},
      boxVisible: false,
      rules: {
        username: [{required: true, message: "请输入用户名"}],
        password: [{required: true, message: "请输入密码"}],
        code: [{required: true, message: "请输入验证码"}, {min: 4, max: 4, message: "验证码长度为4"}]
      }
    }
  },
  methods: {
    router() {
      return router
    },
    updateVerifyCode() {
      this.codeUrl = "/enter/verifyCode?t=" + Math.random();
      axios.get("http://localhost:9000" + this.codeUrl, {responseType: 'blob'}).then(resp => {
        this.codeImg = URL.createObjectURL(resp.data)
      })
    },
    submitLogin() {
      this.$refs["loginForm"].validate(condition => {
        if (condition) {
          let ipt = JSON.parse(JSON.stringify(this.loginForm))
          axios.post("http://localhost:9000/enter/login", ipt).then(resp => {
            if (resp.data.code === 1) {
              router.push("/home")
            } else {
              this.boxInfo.title = "登录失败"
              this.boxInfo.msg = resp.data.msg
              this.boxVisible = true
              this.updateVerifyCode()
            }
          })
        } else {
          this.boxInfo.title = "登录失败"
          this.boxInfo.msg = "请检查登录输入"
          this.boxVisible = true
        }
      })
    },
    toSign() {
      router.push("/sign")
    },
    closeMsgBox() {
      this.boxVisible = false
    },
  },
  mounted() {
    this.updateVerifyCode()
  },
}
</script>

<style scoped>

.loginContainer {
  border-radius: 5%;
  margin: 30vh 30vw;
  background: linear-gradient(to bottom, #e5e5e5, #afafaf);
  height: auto;
  text-align: center;
}

.loginTitle {
  margin: 40px auto 20px auto;
  text-align: center;
  color: #505458;
}

.loginRemember {
  text-align: left;
  margin: 0 0 15px 0;
}

.item .el-input {
  width: 100%;
  height: auto;
  margin: 20px 0;
}

.el-input__inner {
  background-color: #e8e8e8;
  text-align: center;
  border-color: #c0c4cc;
  color: #000
}

.verifyImg {
  cursor: pointer;
  height: 40px;
  width: 100px
}
</style>