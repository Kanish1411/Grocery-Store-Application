<template>
    <div v-if="$store.state.checkl ">
    <Navbar showHomeLink showCartLink/>
    <div text-align="centre" class="margin-form">
      <h1>User page</h1>
      <form  @submit.prevent="search">
    <input class="form-control" type="text" v-model="sear" >
    <button class="btn btn-primary">Search</button>
</form>
        <br>
        <ul v-if="cat.length > 0">
      <h3 v-for="c in cat" :key="c.id">{{ c.name }}
        <br>
      <h5 v-for="i in items" :key="i.id">
        <h5 v-if="i.cid==c.id">
          <h5 v-if="i.qty >0">
          Name: {{ i.name }}­ ­­­ ­ {{   }} Quantity:  {{ i.qty }} ­ ­­­ ­ Price: {{ i.price }}­ ­­­ ­ DOM: {{ i.dom }}<br>
          <button class="btn btn-primary" @click="this.$router.push({
      name: 'addtocart',
      params: { id: i.id, idu: idu },
    })">Add to cart</button>
          </h5>
          <h5 v-else>
            Name: {{ i.name }}­ ­­­ ­ Soldout
          </h5>
      </h5>
      </h5>
      <br>
      </h3>
    </ul>
    <h4 v-else>No categories available Yet</h4>
  </div>
</div>
<div v-else>
  {{ this.login() }}
</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
    name: "User",
    components:{
      Navbar,
    },
    data(){
        return{
        cat: [],
        items:[],
        idu:0,
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
        async search(){
          let token = localStorage.getItem("token")
          const response = await axios.post("search", {
                  key: this.sear,
                },
                {
                headers: {
                    Authorization: "Bearer " + token
                }}
            )
            console.log(response.data.cat)
            this.cat=response.data.cat;
            this.items=response.data.it;
        },
        async login(){
          console.log("login required")
          this.$router.push("/login")
        }
    },
    mounted(){
        this.search()
    },
    created(){
        this.checklogin(),
        this.idu= this.$route.params.id;
        console.log(this.idu);
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