<template>
    <div v-if="$store.state.checkl  && $store.state.checkadmin">
    <Navbar showHomeLink showAddcatLink showReqLink />
    <div text-align="centre" class="margin-form">
      <h1>Admin page</h1>
      <ul v-if="cat.length > 0">
        <h4 v-for="c in cat" :key="c.id">{{ c.name }}
          <br>
        <button class="btn btn-primary" @click="this.$router.push({ name: 'updateCategory', params: { id: c.id } })">update</button>{{   }}
        <button class="btn btn-primary"  @click="deletecat(c.id)">Delete</button>
        <br>
        <br>
        </h4>
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
    name: "Admin",
    components:{
      Navbar,
    },
    data(){
        return{
        cat: [],
        log:0,
        }
    },
    methods: {
        async checklogin(){
            let token = localStorage.getItem("token")
            console.log(token)
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
                    Authorization: "Bearer " + token
                }}
            )
            console.log(response.data.message)
            if (response.data.message == "success") {
                this.$store.commit("setcheckadmin", true);
                this.getcat();
            }
            else {
            this.$store.commit("setcheckadmin", false)
            alert("You are not an Admin redirecting to home page")
            this.$router.push('/login')
            }
        },
        async getcat(){
            const response =await axios.get("getcat",{})
            this.cat=response.data
            console.log(this.cat)
        },
        async deletecat(id){
          try {
            const isConfirmed = window.confirm("are you sure u want to delet this category (all items will be deleted)");
            if (isConfirmed){
            let token = localStorage.getItem("token");
            const response = await axios.post("/deletecat", {
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