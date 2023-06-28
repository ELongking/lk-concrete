<template>
  <el-dialog
      title="Tips"
      width="30%"
      v-model="isVisible"
      @close="closeBox"
      :modal="false"
      :append-to-body="true"
      class="box"
  >

    <span>{{ info.msg }}</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="toOther">确定</el-button>
      </span>
    </template>

  </el-dialog>
</template>

<script>
import router from "@/router";

export default {
  name: "MessageBox",
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
      re_direct: {type: String, default: "", required: false}
    }
  },
  methods: {
    toOther() {
      if (this.info.re_direct !== "") {
        router.push(this.info.re_direct)
      } else {
        this.closeBox()
      }
    },
    closeBox() {
      this.$emit("closeMsgBox")
    }
  },
  watch: {
    boxVisible(newVal, oldVal) {
      this.isVisible = newVal
    }
  }
}
</script>

<style>

.box{
  background: rgba(170, 170, 170, 0.7);
}

.dialog-footer button:first-child {
  margin-right: 10px;
}
</style>