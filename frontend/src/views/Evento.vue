<template>
    <div>
        <mainmenu></mainmenu>
        <b-container fluid>
        <div class="card-title mt-5 mb-3 pt-3">
            <div class="row">
                <div class="col text-left"><h2>Histórico de Eventos</h2></div>    
            </div>
        </div>
        <hr>
        <b-row align-v="end" cols="1" cols-sm="1" cols-md="2" cols-lg="3"> 
            <b-col class="mb-3">
                <input_datetime id="ini" label="Inicio" @check="processaIni"></input_datetime>
            </b-col>
            <b-col  class="mb-3">
                <input_datetime id="fim" label="Fim" @check="processaFim"></input_datetime>
            </b-col>
            <b-col  class="mb-3">
                <b-button block v-bind:class="{disabled:!dataCheck}" variant="primary" @click="filtra" >Aplicar</b-button>
            </b-col>
        </b-row>  

         <div class="text-center">
            <b-table responsive :fields="campos" :items="items" 
                head-variant="dark" sticky-header="400px">
            </b-table>
        </div>
        

        </b-container>
    </div>
</template>

<script>
import mainmenu from '@/components/main_menu.vue'
import input_datetime from '@/components/dataTime.vue'
export default {
    name:'HistoricoView',
    components: {
    mainmenu,
    input_datetime,
    },
    created(){
            this.load()
        },
        data(){
            return{
                form: new FormData(),
                ini:"",
                fim:"",
                dataCheck:false,
                campos:["hora","Node","Tipo","Evento"],
                items:[],
            }
        },
        computed:{  
        },
        methods:{
            load(){
                this.filtra()
            },
            dataFormat(){
                const formData = new FormData()
                formData.append('ini',`${this.ini}`)
                formData.append('fim',`${this.fim}`)
                return formData
            },
            async filtra(){
                fetch(`/eventos/`,{
                    method: 'post',
                    headers: {
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: this.dataFormat()
            }).then(res=>{
                if(res.status === 200){
                   return res.json()
                }else if(res.status===400) {
                    console.log("erro 400")
                }else{
                    throw 'Erro - servidor fora do ar '
                }
            }).then(result=>{
                 this.items = result
            }).catch(erro=>{
                console.log(erro)
            })
            },
            processaIni(valor){
                this.ini = valor
                if(this.ini!="" && this.fim!=""){this.dataCheck=true}
                else{this.dataCheck=false}
            },
            processaFim(valor){
                this.fim=valor
                if(this.ini!="" && this.fim!=""){this.dataCheck=true}
                else{this.dataCheck=false}
            },
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
        },

}
</script>