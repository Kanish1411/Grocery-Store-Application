<template>
    <div v-if="$store.state.checkl ">
    <Navbar showHomeLink showUserhome/>
    <div text-align="centre" class="margin-form">
      <h1>Cart</h1>
      <ul v-if="items.length > 0">
        <h4 v-for="i in items" :key="i.id">
            Name: {{ i.name }}­ ­­­ ­ {{   }} Quantity:  {{ i.qty }} ­ ­­­ ­ Price: {{ i.price }}
            <button class="btn btn-danger" @click="deletecart(i.id)">Remove</button>
            <button class="btn btn-primary" @click="updatecart(i.id,i.iid)">Update</button>
        <br>
        <br>
        </h4>
        <br>
        <h3>Total Price  : {{ this.totalPrice }}</h3>
      </ul>
      <h4 v-else>No itmes in cart</h4>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
export default {
    name: "Cart",
    components:{
      Navbar,
    },
    data(){
        return{
        items: [],
        totalPrice: 0,
        msg:"Are you sure you want to delete?",
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

        async getitems() {
        let token = localStorage.getItem("token");
        const userId = this.$route.params.id;
        const response = await axios.get(`getitems/${userId}`, {
          headers: {
            Authorization: "Bearer " + token,
          },
        });

        this.items = response.data;
        for (const item of this.items) {
          this.totalPrice += item.price;
        }
        },
        async deletecart(id){
          try {
            const isConfirmed = window.confirm(this.msg);
            if (isConfirmed){
            let token = localStorage.getItem("token");
            const response = await axios.post("/deletecart", {
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

        async updatecart(cid,id){
          console.log(id)
          this.msg="do u want to update"
          this.deletecart(cid)
          this.$router.push({
          name: 'addtocart',
          params: { id: id, idu: this.$route.params.id },
        })
        },
    },
    mounted(){
        this.getitems()
    },
    created(){
        this.checklogin()
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