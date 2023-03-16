<template>
    <div>
        <div>
    <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">
      <img class="mr-3" src="../assets/logo-e-service.png" width="120" height="40">
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item><router-link to="/">Fabrica</router-link></b-nav-item>
        <b-nav-item><router-link to="/hist">histórico</router-link></b-nav-item>
        <b-nav-item><router-link to="/eventos">Eventos</router-link></b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto mr-2">
        <b-nav-item-dropdown right>
          <template #button-content>
            <em><img :src="dxm_online" width="30" height="30" /> </em>
          </template>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
    </div>
    </div>
</template>

<script>
export default {
    name:'main_menu',
    created(){
      this.load()
      setInterval(()=>{this.load()},2000)
    },
    methods:{
      getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
      },
      setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+ d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
      },
      load(){
        this.readData()
      },
      async readData() {
        fetch('/online',{
                method: 'get',
                headers: {
                    'Content-Type': 'application/json',
                }
        }).then(res=>{
            if(res.status === 200){
                return res.text()
            }
        }).then(result=>{
             this.data = JSON.parse(result)
             this.erro= false
        }).catch(erro=>{
            console.log(erro)
            this.erro= true
        })
      },
        getImgUrl(pet) {
            var images = require.context('../assets/', false, /\.png$/)
            return images('./' + pet + ".png")
        },
    },
    data(){
      return{
        data:[],
        erro: true,
      }
    },
    computed:{
      dxm_online(){
        if(this.data.dxm_online=="True"){
          return this.getImgUrl("notifiOk")
        }else{
          return this.getImgUrl("notifiFalha")
        }
      }
    },
    props:{
    },
}
</script>