<template>
</template>
<script>
export default {
props: {
  title: String,

},
  name: 'gtm',
  data() {
    return {
    };
  },
  mounted() {
    console.log('send data')
    //this.$gtm.trackView('MyScreenName', 'currentpath');
  }
};</script>

