<template>
<div>
  <TheNavBar />
  <div id='keydiv'>
  <input class="form-control" type="text" placeholder="VGhpcyBpcyBhIHNhbXBsZSBrZXkgaWYgeW91IGRpZG4ndCBrbm93" aria-label="Search" id='search-bar' >
  </div>
  <div id='bigboi'>

  <div id="votebox" v-for="person in people" class="border border-primary rounded">
    <h3>{{person[0]}}</h3>
    <img id='votepic' :src="person[1]"/>
    <br>
    <b-button @click="doThing()" variant='outline-dark' id='button-vote'>{{voteStatus}}</b-button>
  </div>
</div>
</div>
</template>

<script>
import TheNavBar from '@/components/TheNavBar'
export default {
  name: 'Vote',
  components: {
    TheNavBar
  },
  data() {
    return {
      v1num: 9,
      v2num: 5,
      hasVoted: false,
      voteStatus: 'Vote',
      people: [['Tim Kaine','https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Tim_Kaine_116th_official_portrait.jpg/719px-Tim_Kaine_116th_official_portrait.jpg','Vote'],['Corey Stewart','https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Corey_Stewart_8_by_10_crop.jpg/330px-Corey_Stewart_8_by_10_crop.jpg','Vote']]
    }
  },
  methods: {
    doThing() {
      if(!this.hasVoted) {
        this.voteStatus = 'Voted'
        this.v1num += 1
        this.hasVoted = true
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#bigboi {
  display: flex;
  justify-content: center;
}
#votebox {
  margin: 60px;
  height: 400px;
  width: 300px;
  border-width: 3px !important;
  border-color: #352e84 !important;
  text-align: center;
}
#votepic {
  height: 70%;
}
#button-vote {
  margin: 10px;
  width: 100px;
}
h3 {
  padding-top: 10px;
}
#keydiv {
  display: flex;
  margin: 0 auto;
  margin-top: 10px;
  justify-content: center;
  width: 500px
}
</style>
