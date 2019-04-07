<template>
  <div>
  	<h1>Bar Chart</h1>
  	<reactive :chart-data="datacollection"></reactive>
  	<button class="button is-primary" @click="fillData()">Randomize</button>
  </div>
</template>
<script>
export default {
  name: 'Test'
}
</script>
