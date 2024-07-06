<template>
    <div v-if="$store.state.checkl && $store.state.checkadmin">
      <Navbar showadHomeLink  showReqLink />
      <div class="margin-form">
        <h1>Update categories</h1>
     <form @submit.prevent="updatecat">
      
       <label for="name">Category Name:</label>
       <input  class="form-control" type="text" v-model="name" id="name" required />
       <button class="btn btn-primary" type="submit">Update</button>
     </form>
        <br />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  
  export default {
    name: "Updatecat",
    components: {
      Navbar,
    },
    data() {
      return {
        name: "", 
      };
    },
      methods: {
          async checklogin(){
              let token = localStorage.getItem("token")
              
              const response = await axios.get("/cl", {
                  headers: {
                      Authorization: "Bearer " + token
                  }}
              )
              if (response.data.message == "success") {
                  this.$store.commit("setcheckl", true)
                  console.log(response, this.checkl)
              }
              else {
              this.$store.commit("setcheckl", false)
              console.log(response)
              this.$router.push('/login')
              }
          },
          async checkad(){
            let token = localStorage.getItem("token")
              const response = await axios.get("/ca",{
                  headers: {
                      Authorization: "Bearer " + token,

                  }
              }
              )
              console.log(response.data.message)
              if (response.data.message == "success") {
                  console.log("hhhhhh")
                  this.$store.commit("setcheckadmin", true);
              }
              else {
              this.$store.commit("setcheckadmin", false)
              alert("You are not an Admin redirecting to home page")
              this.$router.push('/login')
              }
          },
          async updatecat() {
          try {
            let token = localStorage.getItem("token");
            const id=this.$route.params.id;
            const response = await axios.post("updatecat",
              {
                id: id,
                name: this.name, 
              },
              {
                headers: {
                  Authorization: "Bearer " + token,
                },
              }
            );

            if (response.data.message === "success") {
              this.$router.push('/admin');
              console.log("Category updated successfully");
            } else {
              console.error("Failed");
            }
          } catch (error) {
            console.error("Error", error);
          }
      },
    },
      created(){
          this.checklogin()
          this.checkad()
      }
  };
  </script>
  
  <style scoped>
  .margin-form {
    margin: 40px;
  }
  
  .message {
    position: fixed;
    top: 6%;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px;
    width: 100%;
    text-align: center;
    transition: top 0.5s ease;
  }
  
  .success-message {
    background-color: #4CAF50;
    color: white;
  }
  
  .error-message {
    background-color: #FF0000;
    color: white;
  }
  </style>