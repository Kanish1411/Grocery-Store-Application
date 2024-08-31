<template>
    <div class="margin-form">
      <h1>App Development Project 2</h1>
      <router-link to="/login">
        <button class="btn btn-primary">Login</button>
      </router-link>
      <router-link to="/register">
        <button class="btn btn-primary">Register</button>
      </router-link>
    </div>
  </template>
  <script>

export default {
  methods: {
    async logout(){
      this.$store.state.checkl = false;
      this.$store.state.checkadmin = false;
      this.$store.state.checkman=false;
      let token=localStorage.get("token");
      this.$router.push('/');
    },
    async home() {
        try {
          const response = await axios.post('', {});
        } catch (Exception) {
          pass
        }
      },
  },
  mounted(){
    console.log("loggoed out");
    this.logout();
  },
};
  </script>
<style scoped>
.margin-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
    </style>