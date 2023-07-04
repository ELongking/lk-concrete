<template>
  <div class="container">
    <el-container>
      <el-header>
        <Header></Header>
      </el-header>

      <el-container>
        <el-aside width="200px" class="aside">
          <el-menu class="menu" @select="handleSelect" :router="true">
            <el-menu-item index="/home/show">
              <span>总览</span>
            </el-menu-item>
            <el-menu-item index="/home/details">
              <span>详细信息</span>
            </el-menu-item>
            <el-menu-item index="/home/pwd">
              <span>修改密码</span>
            </el-menu-item>
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
import Header from "@/components/Header.vue"

export default {
  name: "Home",
  components: {
    Header,
  },
  data() {
    return {}
  },
  created() {
    this.handleSelect("/home/show")
  },
  methods: {
    handleSelect(key, keyPath) {
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

.aside {
  height: calc(100vh - 5rem);
}

.aside > .menu {
  background-color: #313743;
  border-right: none;
}

.aside > .menu span {
  color: white;
}

</style>


<style>
body {
  overflow-x: auto;
}
</style>