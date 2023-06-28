<template>
  <div class="container">
    <el-container>
      <el-header>
        <h3>Welcome To Lk-Concrete Management and Analysis System</h3>
      </el-header>
      <el-main>
        <router-link to="/login">
          <el-button>
            点击进入
          </el-button>
        </router-link>
      </el-main>
    </el-container>
  </div>
</template>

<script>
  export default {
    name: "Top",
    data(){
      return {}
    }
  }
</script>

<style scoped lang="css">
  *{
    justify-content: center;
    align-items: center;
  }


  .container{
    margin: 25vh 20vw;
    background: linear-gradient(to bottom, #c7f6f6, #88a7f5);
    height: auto;
  }
</style>