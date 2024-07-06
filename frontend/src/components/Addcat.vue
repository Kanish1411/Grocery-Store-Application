<template>
  <div v-if="$store.state.checkl && $store.state.checkadmin">
    <Navbar showadHomeLink  showReqLink />
    <div class="margin-form">
      <h1>Add Category Page</h1>
   
      <form @submit.prevent="addCategory">
        <label for="categoryName">Category Name:</label>
        <input type="text" v-model="categoryName" id="categoryName" required />
        <br />
        <button class="btn btn-primary" type="submit">Add Category</button>
      </form>

      <br />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: "Addcat",
  components: {
    Navbar,
  },
  data() {
    return {
      categoryName: "", 
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
                    data: dat
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
        async addCategory() {
      try {
        let token = localStorage.getItem("token");
        const response = await axios.post("addc",
          {
            name: this.categoryName,
          },
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );

        console.log(response.data.message);

        if (response.data.message === "success") {
          this.$router.push('/admin');
          console.log("Category added successfully");
        } else {
          console.error("Failed to add category");
        }
      } catch (error) {
        console.error("Error adding category:", error);
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