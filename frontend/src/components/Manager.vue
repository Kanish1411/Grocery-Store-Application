<template>
  <div v-if="$store.state.checkl  && $store.state.checkman">
  <Navbar showHomeLink showReqtab />
  <div text-align="centre" class="margin-form">
    <h1>Manager page</h1>
    <ul v-if="cate.length > 0">
      <h3 v-for="c in cate" :key="c.id">{{ c.name }}
        <br>
      <h5 v-for="i in items" :key="i.id">
        <h5 v-if="i.cid==c.id">
        {{ i.name }} 
        <button class="btn btn-primary"  @click="this.$router.push({ name: 'updateitem', params: { id: i.id } })">Update</button>{{   }}
        <button class="btn btn-danger" @click="deleteit(i.id)" >Delete Item</button>
        </h5>
      </h5>
      <br>
      <button class="btn btn-primary" @click="this.$router.push({ name: 'additem', params: { id: c.id } })">Add Item</button>
      <br>
      <br>
      </h3>
    </ul>
    <h4 v-else>No categories available Yet</h4>
</div>
</div>
<div v-else>
  {{ this.log=1 }}
</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
  name: "Manager",
  components:{
    Navbar,
  },
  data(){
      return{
      cate: [],
      items: [],
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
      async getcat(){
          const response =await axios.get("getcat",{})
          this.cate=response.data
          console.log(this.cate)
          this.getitem()
      },
      async getitem(){
          const response =await axios.get("getitem",{})
          this.items=response.data
          console.log(this.items)
      },
      async deleteit(id){
          try {
            const isConfirmed = window.confirm("are you sure you want to delete this item, (deleteing this leads to removal of this item from cart)");
            if (isConfirmed){
            let token = localStorage.getItem("token");
            const response = await axios.post("/deleteit", {
              id: id,
            },
            {
            headers: {
              Authorization: "Bearer " + token,
            },
            });
            window.location.reload();
            console.log(response.data.message);
            }
            } catch (error) {
          console.error("Error accepting request:", error);
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
      this.getcat()
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