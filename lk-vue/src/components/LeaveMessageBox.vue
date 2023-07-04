<template>
  <el-dialog
      title="Tips"
      width="30%"
      v-model="isVisible"
      :modal="false"
      :append-to-body="true"
      class="box"
      :show-close="false"
  >

    <span>{{ info.msg }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="toNext">确定</el-button>
        <el-button @click="toNow">留在原地</el-button>
      </span>
    </template>

  </el-dialog>
</template>

<script>

export default {
  name: "LeaveMessageBox",
  data() {
    return {
      isVisible: false
    }
  },
  props: {
    boxVisible: {type: Boolean, default: false},
    info: {
      title: {type: String, default: ""},
      msg: {type: String, default: ""},
    }
  },
  methods: {
    toNext(){
      this.$emit("toNext")
    },
    toNow(){
      this.$emit("toNow")
    },
  },
  watch: {
    boxVisible(newVal, oldVal) {
      this.isVisible = newVal
    }
  }
}
</script>

<style scoped>

.box{
  background: rgba(170, 170, 170, 0.7);
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>