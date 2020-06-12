<template>
  <Plain>
    <Login/>
  </Plain>
</template>

<script>
  import Plain from '@/components/Plain.vue'

  export default {
    name: 'Main',
    components: {
      Plain,
      Login
    },
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>