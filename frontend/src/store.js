import { createStore }from 'vuex'
const store =  createStore({
    state(){
        return{
            token: localStorage.getItem('token'),
            user: null,
            checkl: false,
            checkadmin: false,
            checkman:false,
        }
    },
    mutations:{
        setcheckl(state, payload){
            state.checkl = payload
        },
        setcheckmanager(state, payload){
            state.checkman = payload
        },
        setcheckadmin(state, payload){
            state.checkadmin = payload
        }
    }
}
)
export default store
