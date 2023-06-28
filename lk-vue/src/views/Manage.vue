<template>
  <div class="container">
    <el-container>
      <el-header>
        <Header></Header>
      </el-header>

      <el-container>
        <el-aside width="200px" class="aside">
          <el-menu class="menu" @select="handleSelect" :router="true">
            <el-menu-item index="/manage/show">
              <span>查看批次</span>
            </el-menu-item>
            <el-menu-item index="/manage/create">
              <span>创建新批次</span>
            </el-menu-item>
            <el-sub-menu>
              <template #title>
                <span>关于/帮助</span>
              </template>
              <el-menu-item index="/manage/ha#qianyan">前言</el-menu-item>
              <el-menu-item index="/manage/ha#guanli">管理</el-menu-item>
              <el-menu-item index="/manage/ha#xunlian">训练</el-menu-item>
              <el-menu-item index="/manage/ha#tuili">推理</el-menu-item>
              <el-menu-item index="/manage/ha#zongjie">开源总结</el-menu-item>
            </el-sub-menu>

          </el-menu>
        </el-aside>

        <el-main>
          <router-view></router-view>
        </el-main>

      </el-container>
    </el-container>
  </div>
</template>


<script>
import Header from "@/components/Header.vue";

export default {
  name: "Manage",
  components: {Header},
  data(){
    return{

    }
  },
  mounted() {
    this.handleSelect("/manage/show")
  },
  methods:{
    handleSelect(key, path){
      this.$router.push(key)
    }
  }
}
</script>

<style scoped>
.el-main {
  background-color: #e9edf1;
  height: calc(100vh - 5rem);
}
.aside{
  height: calc(100vh - 5rem);
}

.aside > .menu {
  background-color: #313743;
  border-right: none;
}
.aside > .menu span{
  color: white;
}

.el-main::-webkit-scrollbar {
  display: none;
}
</style>