<template>
<div id='bigbox'>
  <img src="https://cdn.pixabay.com/photo/2015/02/24/15/41/dog-647528__480.jpg" height="160" id="my_pic" />
  <div id="title" style="display: inline-block;"><p><b id='mytitle'>How Trump Built his Wall</b></p> <p id='mypara'>D Trump</p></div>
</div>
</template>
<script>
export default {
  name: 'Article',
  data() {
    my_source: 'https://cdn.pixabay.com/photo/2015/02/24/15/41/dog-647528__480.jpg'
  }
}
</script>
<style scoped>
p {
  padding: 0px;
  margin: 0px;
}
#bigbox {
  border: 3px solid #352e84;
  width: 900px;

  margin-left: 30px;
}
#my_pic {
  border: 3px solid #352e84;
}
#mypara {
  padding-top:10px;
  font-size: 20px;
}
#mytitle {
  font-size: 30px;
}
#title {
  padding: 0px;
  margin: 0px;
}
</style>
