<template>
  <div class="container" ref="scrollContainer" @scroll="handleScroll">
    <h3>关于和帮助</h3>
    <el-progress class="progress" type="circle" :show-text="false" :percentage="scrollPercentage"/>
    <div class="branch">
      <h2 class="branchTitle" id="qianyan">前言</h2>
      <p></p>
    </div>
    <div class="branch">
      <h2 class="branchTitle" id="guanli">管理</h2>
      <p></p>
    </div>
    <div class="branch">
      <h2 class="branchTitle" id="xunlian">训练</h2>
      <p>
        我个人比较了市面上的一些Deep Learning Based on Java的方法, 感觉不是很方便
        （毕竟Java主要是写中间件的也不是干这个的）。理论上是网页端发送请求给后台服务器处理, 但是众所周知我个人这里没有什么额外服务器,
        因此这边选择的是使用额外由Python编写的软件进行训练, 相当于将客户端和服务器端划成一个了。下载地址如下：
      </p>
      <el-collapse style="width: 80%; margin: 0 auto;" accordion>
        <el-collapse-item>
          <template #title>
            <div class="collapseItem">BaiDu Cloud</div>
          </template>
          <p></p>
        </el-collapse-item>
        <el-collapse-item>
          <template #title>
            <div class="collapseItem">Google Drive</div>
          </template>
          <p></p>
        </el-collapse-item>
      </el-collapse>
      <p>

      </p>
    </div>
    <div class="branch">
      <h2 class="branchTitle" id="tuili">推理</h2>
      <p>推理流程可有两种形式, 第一种通过网页端推理, 第二种通过软件推理。</p>
      <p></p>
    </div>
    <div class="branch">
      <h2 class="branchTitle" id="zongjie">开源总结</h2>
      <p>个人第一个全栈项目, 所使用的技术均在下方列出（按依赖语言分类）:</p>
      <el-tabs type="border-card" style="width: 80%; margin: 0 auto;">
        <el-tab-pane label="Lang">
          <el-table :data="techDataLang">
            <el-table-column prop="name" label="名称" min-width="45%"/>
            <el-table-column prop="role" label="作用" min-width="45%"/>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="Java">
          <el-table :data="techDataJava">
            <el-table-column prop="name" label="名称" min-width="45%"/>
            <el-table-column prop="role" label="作用" min-width="45%"/>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="Python">
          <el-table :data="techDataPython">
            <el-table-column prop="name" label="名称" min-width="45%"/>
            <el-table-column prop="role" label="作用" min-width="45%"/>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="JavaScript">
          <el-table :data="techDataJs">
            <el-table-column prop="name" label="名称" min-width="45%"/>
            <el-table-column prop="role" label="作用" min-width="45%"/>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>

  </div>
</template>

<script>
export default {
  name: "HelpAbout",
  data() {
    return {
      scrollTop: 0,
      componentHeight: 1,
      techDataLang: [
        {name: "Java", role: "Web后端逻辑/中间件"},
        {name: "Python", role: "软件前后端/ML&DL训练推理"},
        {name: "JavaScript", role: "Web前端"},
        {name: "GPT-3.5", role: "小助手"}
      ],
      techDataJava: [
        {name: "SpringBoot", role: "容器/MVC"},
        {name: "MyBatis", role: "ORM框架"},
        {name: "Redis", role: "缓存"},
        {name: "Druid", role: "数据库连接池"},
        {name: "Swagger-UI", role: "文档生成"},
        {name: "PageHelper", role: "MyBatis分页工具"},
        {name: "HuTool", role: "工具类"},
        {name: "Aliyun-OSS", role: "对象存储"},
        {name: "DeepJavaLibrary", role: "Web端深度学习推理"},
        {name: "JPMML", role: "Web端机器学习推理"}
      ],
      techDataPython: [
        {name: "PyQt5", role: "软件用户界面"},
        {name: "Sklearn", role: "机器学习训练和推理"},
        {name: "Pytorch", role: "深度学习训练和推理"},
        {name: "sklearn2pmml", role: "机器学习模型转PMML"},
        {name: "oss2", role: "对象存储"},
        {name: "DBUtils", role: "数据库连接池"}
      ],
      techDataJs: [
        {name: "Vue3", role: "Web页面主框架"},
        {name: "Element-Plus", role: "组件模板框架"},
        {name: "Jquery", role: "JS模块化操作"},
        {name: "Axios", role: "异步请求"},
        {name: "ECharts", role: "可视化图表"},
      ]
    }
  },
  methods: {
    handleScroll(event) {
      const scrollContainer = event.target;
      this.scrollTop = scrollContainer.scrollTop;
      this.componentHeight = scrollContainer.scrollHeight - scrollContainer.clientHeight;
    }
  },
  computed: {
    scrollPercentage() {
      return Math.round((this.scrollTop / this.componentHeight) * 100);
    },
  },
  mounted() {
    if (window.location.hash) {
      const element = document.querySelector(window.location.hash)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }
    this.$refs.scrollContainer.addEventListener("scroll", this.handleScroll, true)
  },
  beforeUnmount() {
    this.$refs.scrollContainer.removeEventListener("scroll", this.handleScroll)
  }
}
</script>

<style scoped>
.container {
  height: 100vh;
  overflow-y: scroll;
}

.progress {
  position: fixed;
  top: 50px;
  right: 90px;
  padding: 20px;
  width: 40px;
}

.branch {
  width: 86%;
  margin: auto;
}

.branchTitle {
  border-bottom: gray solid 1px;
  padding-bottom: 6px;
}

p {
  text-indent: 2em;
  font-size: 14px;
  line-height: 24px;
  letter-spacing: 0.6px;
}

.collapseItem {
  padding-left: 30px;
}

::-webkit-scrollbar {
  width: 10px;
  height: 1px;
}

::-webkit-scrollbar-track {
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  background-color: rgba(109, 109, 109, 0.4);
  height: 120px;
}
</style>