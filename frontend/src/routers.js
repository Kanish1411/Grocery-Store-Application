import {createRouter, createWebHistory} from  'vue-router'
import Login from '.\\components\\Login.vue'
import Home from '.\\components\\Home.vue'
import Register from '.\\components\\Register.vue'
import About from '.\\components\\About.vue'
import Userhome from '.\\components\\Userhome.vue'
import Manager from '.\\components\\Manager.vue'
import Admin from '.\\components\\Admin.vue'
import Addcat from '.\\components\\Addcat.vue'
import Request from '.\\components\\Request.vue'
import Updatecat from '.\\components\\Updatecat.vue'
import Additem from '.\\components\\Additem.vue'
import Updateitem from '.\\components\\Updateitem.vue'
import Addtocart from '.\\components\\Addtocart.vue'
import Cart from '.\\components\\Cart.vue'
import Req from '.\\components\\Req.vue'

const routes =[ 
    {
        path: "/",
        component: Home,
    },
    {
        path:"/login",
        component:Login
    },
    {
        path:"/register",
        component:Register
    },
    {
        path:"/about",
        component:About
    },
    {
        path:"/manager/:id",
        component:Manager,
        name:"manager"
    },
    {
        path:"/admin",
        component:Admin
    },
    {
        path:"/user/:id",
        component:Userhome,
        name:"user"
    },
    {
        path:"/request",
        component:Request
    },
    {
        path:"/addcat",
        component:Addcat
    },
    {
        path: '/update-category/:id',
        name: 'updateCategory',
        component: Updatecat, 
      },
      {
        path: '/additem/:id',
        name: 'additem',
        component: Additem, 
      },
      {
        path: '/updateitem/:id',
        name: 'updateitem',
        component: Updateitem, 
      },
      {
        path: '/addtocart/:idu/:id',
        name: 'addtocart',
        component: Addtocart
      },
      {
        path: '/cart/:id',
        name: 'cart',
        component: Cart
      },
      {
        path: '/req/:id',
        name:'request',
        component:Req,
      }
]

const router=createRouter({
    history:createWebHistory(),
    routes,
})
export default router;