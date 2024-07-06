<template>
    <div v-if="$store.state.checkl  && $store.state.checkman">
    <Navbar showHomeLink showDashman />
    <div text-align="centre" class="margin-form">
      <h1>Request page</h1>
      <form @submit.prevent="req">
      <label for="task">Task:</label>
        <select class="form-control" v-model="task" required>
          <option value="Create ">Create</option>
          <option value="Update ">Update</option>
          <option value="Delete ">Delete</option>
        </select>
        <label for="cname">Category name:</label>
        <input class="form-control" type="text" v-model="cname" required>
        <br>
        <button class="btn btn-primary">Submit</button>
    </form>
    </div>

  </div>
  </template>

  <script>
  import axios from 'axios';
  import Navbar from './Navbar.vue';
  export default {
    name: "Req",
    components:{
      Navbar,
    },
    data(){
        return{
        cname:"",
        task:"",
        log:0,
        }
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
          async req(){
          try {
            const response = await axios.post('interact', {
            id:this.$route.params.id,
            cname: this.cname,
            task: this.task,
            });
            } catch (error) {
            pass
            }
          },
          async login(){
            console.log("login required")
            this.$router.push("/login")
          },
          async logg(){
            if (this.log==1){
                this.login()
            }
          }
      },
      mounted(){
        this.logg
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