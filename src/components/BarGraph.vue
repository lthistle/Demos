<script>
import { Bar } from 'vue-chartjs'
export default {
  extends: Bar,
  props: ['voteNumber'],
  mounted () {
    this.renderLineChart()
  },
  computed: {
    chartData: function() {
      return [this.voteNumber, 5, 6]
    }
  },
  methods: {
    renderLineChart: function() {
      this.renderChart( {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
          {
            label: 'GitHub Commits',
            backgroundColor: '#f87979',
            data: this.chartData
          }
        ]
      }, { responsive: true, maintainAspectRatio: false })
    }
  },
  watch: {
    data: function() {
      this._chart.destroy();
      console.log('watched')
      //this.renderChart(this.data, this.options);
      this.renderLineChart();
    }
  }
}
</script>
