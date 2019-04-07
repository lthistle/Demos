<template>
<div>
  <TheNavBar />
  <div class="form-inline" id="searchdiv">
    <input class="form-control" type="text" v-model="searchcontent" placeholder="Brexit" aria-label="Search" id='search-bar' >
    <b-button @click="getStuff()" variant='outline-dark' id='search-button'>Search</b-button>
  </div>

  <div id='my-article' v-for="person in getList">

      <img :src="person.image" :href="person.url" width=20% id="my_pic" />
      <div>
        <a :href="person.url"><h2><b>{{person.title}}</b></h2></a>
        <p>{{person.author}}</p>
      </div>
  </div>

  <canvas id="barChart"</canvas>
</div>
</template>

<script>
import Article from '@/components/Article'
import TheNavBar from '@/components/TheNavBar'
import  { Passage } from '@/passage.js'
export default {
  name: 'News',
  components: {
    TheNavBar,
    Article
  },
  data() {
    return {
      articles: [],
      searchcontent: 'Brexit'
    }
  },
  methods: {
    getStuff() {
      var Axios = require('axios')
      var xAPIKey = 'ie5EtNqb2pafUpw0FsMC84hHqrW9L4uf2Ql9YTJF'
      Axios.defaults.headers.common['X-API-Key'] = xAPIKey

      var endpoint = "http://34.73.212.18/query?"
      let vm = this
      var parameters = {
        'search': this.searchcontent
      }
      console.log(this.searchcontent)
      Axios.get(endpoint, {
        params: parameters
      }).then(function(response) {
        vm.articles = []
        console.log(response)
        var keys = Object.keys(response['data'])
        for(let i=0; i<Math.min(keys.length,10); i++) {
          //console.log(response['data'][keys[i]])
          vm.articles.push(new Passage(keys[i],response['data'][keys[i]][0],response['data'][keys[i]][1],response['data'][keys[i]][2]))
        }
      })
      console.log(this.articles)
      }
    },
    computed: {
      getList() {
        return this.articles
      }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#search-button {
  margin-top: 10px;
  margin-left: 5px;
}
#search-bar {
  margin-top: 10px;
  margin-left: 10px;
  width: 350px
}
#yup {
  padding-top: 50px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 0 auto;
}
#personname {
  display: flex;
  align-items: center;
  justify-content: center;
}
#searchdiv {
  display: flex;
  justify-content: left;
}
#my-article {
  height: 140px;

  width: 100%;
  display: flex;
  margin-left: 20px;
  margin-top: 10px;
}
#my_pic {
  border: 3px solid #352e84;
}
h2 {
  padding: 10px
}
p {
  padding-left: 12px;
}
a {
  color: black;
  text-decoration: none;
}
</style>
