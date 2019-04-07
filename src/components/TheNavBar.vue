<template>
  <div>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <b-navbar-brand href="#">Dēmos</b-navbar-brand>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
        <b-nav-item href="#/home" id='item-home'>Home</b-nav-item>
        <b-nav-item href="#/vote" id='item-vote'>Vote</b-nav-item>
        <b-nav-item href="#/news" id='item-news'>News</b-nav-item>
        <b-nav-item href="#/politicians" id='item-poli'>Politicians</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
  </div>
</template>
<script>
export default {
  name: 'TheNavBar'
}
</script>

<style scoped>
.navbar {
  background-color: #352e84 !important;
}
</style>
