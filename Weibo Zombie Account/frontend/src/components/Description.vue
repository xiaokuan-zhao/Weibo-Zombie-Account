<template>
  <div>
    <Divider>水军识别说明</Divider>
    <p class="text block">考虑到微博的防爬虫机制相当严格，爬取速度过快会被<b>封锁ip</b>，本应用仅对单用户信息进行快速分析并归入档案</p>
    <p class="text block">在搜索框中输入用户的uid，开始识别</p>
    <a class="block"
       href="https://weibo.com/ttarticle/p/show?id=2309404206774541494693&mod=zwenzhang?comment=1&sudaref=www.baidu.com&display=0&retcode=6102">如何找到某用户的uid？</a>
    <p class="block"
       style="color:#a35252">服务器响应的时间可能达到20秒或更久</p>
    <p class="block"
       style="color:#a35252">（如果太长时间无法响应，请回到首页）</p>
    <p class="block"
       style="color:#a35252;"><i>本项目基于一组已知水军样本，但不排除部分普通用户和水军被误判的可能</i></p>
  </div>
</template>

<script>
import { Divider } from 'vux'

export default {
  components: {
    Divider
  }
}
</script>

<style>
.block {
  margin-top: 20px;
  padding-left: 5%;
  padding-right: 5%;
}

.test {
  color: #757575;
}
</style>