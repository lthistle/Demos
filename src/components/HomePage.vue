
<template>
<div>
  <TheNavBar />
  <div id='opacity-div'>
  <div id="logobox-div">
    <img src="@/logo.svg" alt='logo' width=600px>
    <br>
    <p id='quote'><i>Secure voting and empowerment of citizens to make civic change</i></p>
    <br>
    <b-button @click="gotopage('#/politicians')" variant='outline-dark' id='button-pol'>Find Politicians</b-button>
    <b-button @click="gotopage('#/news')" variant='outline-dark' id='button-news'>Get News</b-button>
    <b-button @click="gotopage('#/vote')" variant='outline-dark' id='button-vote'>Vote</b-button>
  </div>
</div>
</div>

</template>

<script>
import TheNavBar from "@/components/TheNavBar"

export default {
  name: 'HomePage',
  components: {
    TheNavBar
  },
  methods: {
    gotopage(myurl) {
     window.location.href = myurl
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#logobox-div {
  padding-top: 50px;
  margin: 0 auto;
  text-align: center;
  background-image: linear-gradient(rgba(200, 200, 200, 0.8), rgba(255, 255, 255, 0.5)), url("http://pollingplacephotoproject.org/wp-content/uploads/2017/11/o-VOTING-facebook.jpg");
  height: 100vh;
}
#quote {
  padding-top: 30px;
  text-decoration: italic;
}
#button-pol, #button-news, #button-vote {
  width: 200px;
  height: 75px;
  margin: 1px;
  font-size: 20px;
}
</style>
