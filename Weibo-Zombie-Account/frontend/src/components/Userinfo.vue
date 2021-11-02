<template>
  <div class="test">
    <Divider style="margin-top:45px">该用户的基本信息</Divider>
    <div class="block">
      <p>uid：{{uid}}</p>
      <p>用户名：{{screen_name}}</p>
      <p>性别：{{gender}}</p>
      <p>总微博数：{{statuses_count}}</p>
      <p>粉丝数：{{followers_count}}</p>
      <p>关注数：{{follow_count}}</p>
      <p>个人简介：{{description}}</p>
      <p>微博等级：{{urank}}</p>
      <p>会员等级：{{mbrank}}</p>
      <p>是否认证？{{verified}}</p>
      <p>认证原因：{{verified_reason}}</p>
    </div>
    <Divider>用户微博信息分析结果</Divider>
    <div class="block">
      <p>转发微博数：{{retweets}}</p>
      <p>原创微博数：{{original}}</p>
      <p>平均点赞数：{{dalllike}}</p>
      <p>平均评论数：{{dallcomm}}</p>
      <p>平均转发数：{{dallrepo}}</p>
      <p>预测结论：这个用户<b>{{isreal}}</b></p>
    </div>
  </div>

</template>

<script>
import { Divider } from 'vux'

export default {
  components: { Divider },
  data() {
    return {
      uid: this.$route.params.id,
      screen_name: '',
      gender: '',
      statuses_count: '',
      followers_count: '',
      follow_count: '',
      description: '',
      avatar_hd: '',
      urank: '',
      mbrank: '',
      verified: '',
      verified_reason: '',
      retweets: '',
      original: '',
      dalllike: '',
      dallcomm: '',
      dallrepo: '',
      isreal: ''
    }
  },
  beforeRouteUpdate(to, from, next) {
    if (to.fullPath != from.fullPath) {
      next()
      this.$data.uid = to.params['id']
      this.getUserById(this.$data.uid)
    }
  },
  mounted() {
    this.getUserById(this.$data.uid)
  },
  methods: {
    getUserById(uid) {
      this.$axios
        .get(`http://49.234.202.99:80/api/data`, {
          params: {
            id: uid
          }
        })
        .then(response => {
          this.screen_name = response.data.userInfo.screen_name
          this.gender = response.data.userInfo.gender
          this.statuses_count = response.data.userInfo.statuses_count
          this.followers_count = response.data.userInfo.followers_count
          this.follow_count = response.data.userInfo.follow_count
          this.description = response.data.userInfo.description
          this.avatar_hd = response.data.userInfo.avatar_hd
          this.urank = response.data.userInfo.urank
          this.mbrank = response.data.userInfo.mbrank
          if (response.data.userInfo.verified) {
            this.verified = '已认证'
          } else {
            this.verified = '未认证'
          }
          this.verified_reason = response.data.userInfo.verified_reason
          this.retweets = response.data.userInfo.retweets
          this.original = response.data.userInfo.original
          this.dalllike = response.data.userInfo.dalllike.toFixed(2)
          this.dallcomm = response.data.userInfo.dallcomm.toFixed(2)
          this.dallrepo = response.data.userInfo.dallrepo.toFixed(2)

          if (response.data['isreal']) {
            this.isreal = '是普通人'
          } else {
            this.isreal = '是水军'
          }
        })
        .catch(error => {
          console.log(error)
        })
    }
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