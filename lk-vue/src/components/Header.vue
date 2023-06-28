<template>
  <div class="header">
    <el-row>
      <el-col :span="5"><div @click="router().push('/home')">首页</div></el-col>
      <el-col :span="5"><div @click="router().push('/manage')">管理系统</div></el-col>
      <el-col :span="5"><div @click="router().push('/train')">训练系统</div></el-col>
      <el-col :span="5"><div @click="router().push('/infer')">推理系统</div></el-col>
      <el-col :span="4"><div @click="logOut">退出登录</div></el-col>
    </el-row>

  </div>
</template>


<script>
import router from "@/router";
import axios from "axios";

export default {
  name: "Header",
  methods: {
    router() {
      return router
    },
    logOut(){
      axios.get("http://localhost:9000/enter/logout").then(resp=>{
        let res = resp.data
        if (res.code === 1){
          router.push("/")
        }
      })
    }
  }
}
</script>

<style scoped>
  .el-row .el-col > div:hover{
    background: #056969;
  }

  .el-row .el-col > div{
    cursor: pointer;
  }

  .header{
    height: 3rem;
  }
</style>