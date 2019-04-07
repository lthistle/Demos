// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)
//App.use(cors())
Vue.config.productionTip = false
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
Vue.component('reactive', {
	extends: VueChartJs.Bar,
	mixins: [VueChartJs.mixins.reactiveProp],
	data: function () {
		return {
			options: {
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true
						},
						gridLines: {
							display: true
						}
					}],
					xAxes: [{
						ticks: {
							beginAtZero: true
						},
						gridLines: {
							display: false
						}
					}]
				},
				legend: {
					display: false
				},
				tooltips: {
					enabled: true,
					mode: 'single',
					callbacks: {
						label: function(tooltipItems, data) {
							return '$' + tooltipItems.yLabel;
						}
					}
				},
				responsive: true,
				maintainAspectRatio: false,
				height: 200
			}
		}
	},
	mounted () {
		// this.chartData is created in the mixin
		this.renderChart(this.chartData, this.options)
	}
})

var vm = new Vue({
	el: '.app',
	data () {
		return {
    	datacollection: null
    }
	},
	created () {
		this.fillData()
	},
	methods: {
		fillData () {
        this.datacollection = {
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
          datasets: [
            {
              label: 'Data One',
              backgroundColor: '#f87979',
              data: [this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt(), this.getRandomInt()]
            }
          ]
        }
      },
    getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      }
	}
})
