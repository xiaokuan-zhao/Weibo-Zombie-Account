<template>
  <div class="page">
    <Search v-model="value"
            position="fixed"
            auto-scroll-to-top
            @on-cancel="onCancel"
            @on-submit="onSubmit(value)"
            ref="search">
    </Search>
    <router-view></router-view>
  </div>
</template>

<script>
import { Divider, Flexbox, FlexboxItem, Search } from 'vux'

export default {
  name: 'Index',
  components: {
    Flexbox,
    FlexboxItem,
    Search,
    Divider
  },
  data() {
    return {}
  },
  mount() {},
  methods: {
    onCancel() {
      this.$router.push({
        path: '/'
      })
    },
    onSubmit(val) {
      //console.log('value:' + val)
      //console.log('this:' + this)
      this.$router.push({
        path: `/user/${val}`
      })
    }
  }
}
</script>

<style>
.page {
  width: 100%;
  height: 100%;
  position: absolute;
  margin: 0px;
  padding: 0px;
}
</style>