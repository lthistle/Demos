<template>
<div>
  <TheNavBar />
  <div class="form-inline">
    <input class="form-control" type="text" v-model="location" placeholder="6560 Braddock Rd" aria-label="Search" id='search-bar' >
    <b-button @click="getPolitician()" variant='outline-dark' id='search-button'>Search</b-button>
  </div>
  <div class="row" v-for="customers in chunkedCustomers">
      <div id='yup' class="column" v-for="customer in customers">
        <span id='personname'><b>{{customer.name}}</b><br></span>
        <img :src="customer.image" height=270px width=200px class="rounded" />
        <span id='personname'><b>Location</b>:  {{customer.city}}, {{customer.state}}<br></span>
        <span id='personname'><b>Party</b>:  {{customer.party}}<br></span>
        <a :href="customer.social" id="personname">Website</a>
     </div>
  </div>
</div>
</template>

<script>
import TheNavBar from "@/components/TheNavBar"
import  { Politician } from '@/politician.js'
var chunk = require('chunk')
export default {
  name: 'P2A',
  components: {
    TheNavBar
  },
  data() {
    return {
      location: '6560 Braddock Rd',
      pname: 'stephen huan',
      plist: [new Politician('Washington','DC','Tim Kaine','timkaine','Democrat',"http://upload.wikimedia.org/wikipedia/commons/a/a3/Tim_Kaine_116th_official_portrait.jpg"), new Politician('Washington','DC','Don Beyer', 'https://beyer.house.gov/rss.xml', 'Democrat', "https://upload.wikimedia.org/wikipedia/commons/e/e3/Don_Beyer%2C_official_114th_Congress_photo_portrait.jpeg"), new Politician('Richmond','VA','Justin Fairfax','https://www.facebook.com/JustinEFairfax/', 'Democrat', "https://upload.wikimedia.org/wikipedia/commons/8/8d/Justin_Fairfax_crop.jpg"), new Politician('Richmond','VA','Dick Saslaw', 'SenSaslaw', 'Democrat', "https://upload.wikimedia.org/wikipedia/commons/0/0f/Sen._Saslaw_2018.jpg"), new Politician('Richmond','VA','Kaye Kory','kayekory','Democrat',"https://upload.wikimedia.org/wikipedia/commons/4/4f/Kaye_Kory_2010.jpg"), new Politician('Richmond','VA','Ralph Northam','GovernorVA','Democrat',"https://upload.wikimedia.org/wikipedia/commons/7/72/Governor_Ralph_Northam_Gives_Inaugural_Address_%2839348612584%29_%28cropped%29.jpg"), new Politician('Washington','DC','Donald Trump','POTUS','Republican',"https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg"), new Politician('Washington','DC','Mike Pence','VP','Republican',"https://upload.wikimedia.org/wikipedia/commons/b/b9/Mike_Pence_official_Vice_Presidential_portrait.jpg"), new Politician('Washington','DC','Mark Warner','W000805','Democrat',"https://upload.wikimedia.org/wikipedia/commons/0/0c/Mark_Warner_113th_Congress_photo.jpg")]
    }
  },
  methods: {
    getPolitician() {
      console.log('starting')
      var Axios = require('axios')
      var xAPIKey = 'ie5EtNqb2pafUpw0FsMC84hHqrW9L4uf2Ql9YTJF'
      Axios.defaults.headers.common['X-API-Key'] = xAPIKey
      var endpoint = "https://fmrrixuk32.execute-api.us-east-1.amazonaws.com/hacktj/legislators"
      let vm = this
      var params_p2a = {
        'address': this.location
      }
      Axios.get(endpoint, {
        params: params_p2a
      }).then(function(response) {
        var data = response.data.officials
        for(let i=0; i< data.length; i++) {

          let name = data[i].first_name.concat(' '.concat(data[i].last_name))
          if(data[i].nickname!='') {
            name = data[i].nickname.concat(' '.concat(data[i].last_name))
          }
          let city = data[i].office_location.city
          let state = data[i].office_location.state
          let social = data[i].socials[0].identifier_value
          let party = data[i].party
          var params_wiki = {
            'format': 'json',
            'action': 'query',
            'prop': 'pageimages',
            'piprop': 'original',
            'titles': name
          }
          console.log(city, state, name, social, party)
          var image = 'nochange'
          Axios.get('https://en.wikipedia.org/w/api.php', {
            params: params_wiki
          }).then(function(rb) {
            console.log(rb)
            var pages = rb.data.query.pages
            var pageKeys = Object.keys(pages)
              if (pages[pageKeys[0]].original == null) {
                image = '#/nopfp.png'
              }
              else {
                image = pages[pageKeys[0]].original.source
              }
              vm.plist.push(new Politician(city, state, name, social, party, image))
            })

        }
      })
      console.log(this.plist)
      //let p = new Politician(3, 4, 5, 6, 7, 8)
    }
  },
  computed: {
    chunkedCustomers() {
      return chunk(this.plist, 4)
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
  width: 300px
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
</style>
