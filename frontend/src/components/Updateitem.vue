<template>
    <div v-if="$store.state.checkl && $store.state.checkman">
      <Navbar showadHomeLink  />
      <div class="margin-form">
        <h3> Update item</h3>
        <form @submit.prevent="Updateitem">
      
       <label for="name">Item Name:</label>
       <input  class="form-control" type="text" v-model="name" id="name" required />
       <label for="price">Item Price:</label>
       <input  class="form-control" type="number" v-model="price" id="price" required />
       <label for="qty">Item Quantity:</label>
       <input  class="form-control" type="number" v-model="qty" id="qty" required />
       <label for="dom">Date of Manufacture:</label>
       <input  class="form-control" type="date" v-model="categoryName" id="dom"  />
       <br>
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
    name: "Updateitem",
    components: {
      Navbar,
    },
    data() {
      return {
        name: "",
        price: 0,
        qty: 0,
        dom: new Date(), 
        id: 0,
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
          async checkman(){
          let token = localStorage.getItem("token")
            const response = await axios.get("/cm",{
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
            console.log(response.data.message)
            if (response.data.message == "success") {
                this.$store.commit("setcheckmanager", true);
            }
            // else if(response.data.message =="not approved" ){
            //   this.$store.commit("setcheckmanager", false)
            //   alert("Please wait till ur account is verified")
            //   this.$router.push('/login')
            // }
            else {
            this.$store.commit("setcheckmanager", false)
            alert("You are not an Manager redirecting to home page")
            this.$router.push('/login')
            }
        },
        async Updateitem() {
        try {
          let token = localStorage.getItem("token");
          const id=this.$route.params.id;
          console.log(id)
          const response = await axios.post("updateit",
            {
              name: this.name,
              price: this.price,
              qty: this.qty,
              dom: this.dom,
              id: id
            },
            {
              headers: {
                Authorization: "Bearer " + token,
              },
            }
          );

          if (response.data.message === "success") {
            this.$router.push('/manager');
            console.log("Item updated successfully");
          } else {
            console.error("Failed to update Item");
          }
        } catch (error) {
          console.error("Error Updating Item:", error);
        }
      },
    },
      created(){
          this.checklogin()
          this.checkman()
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