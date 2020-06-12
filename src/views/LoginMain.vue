<template>
  <div class="home">
    <Login/>
  </div>
</template>

<script>
  import Login from '@/components/Login.vue'
  export default {
    name: 'LoginMain',
    components: {
      Login
    },
    props: {
      source: String,
    },
  }
</script>