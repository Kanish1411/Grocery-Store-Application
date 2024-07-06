<template>
    <div v-if="$store.state.checkl ">
      <Navbar showUserhome />
      <div class="margin-form">
        <h1>Add to cart Page</h1>
        <form @submit.prevent="addtoc">
        <label for="name">Quamtity:</label>
        <input  class="form-control" type="number" v-model="qty" id="qty" required />
        <button class="btn btn-primary" type="submit">Add</button>
        </form>
        <br />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  
  export default {
    name: "addtocart",
    components: {
      Navbar,
    },
    data() {
      return {
        id: this.$route.params.id,
        idu: this.$route.params.idu,
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
          async addtoc(){
              let token=localStorage.getItem('token');
              const response = await axios.post("addtocart",
              {
                id:this.id,
                idu:this.idu,
                qty:this.qty,
              },
              {
              headers: {
                  Authorization: "Bearer " + token,
                },
              }
              )
              if(response.data.message=="out of stock"){
                alert("entered quantity higher than available")
                window.location.reload();
              }
              else{
                this.$router.push({ name: 'user', params: { id: this.idu } 
                })
              }
          },
         
    },
      created(){
          this.checklogin()
          console.log(this.id)
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