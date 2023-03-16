<template>
    <div>
         <div class="col-auto">
            <div class="bg-light border rounded mb-5 p-2 painel">
                <h3 class="text-center">{{data.name}}</h3>
                <div class="m-auto text-center" v-if="data.online=='True'"><img :src="motorImg" height="160px"></div>
                <div class="m-auto text-center" v-else><img :src="getImgUrl('motorOffLine')" height="160px"></div>
                <b-form-group v-if="data.vibraX>0" class="m-2" label="Veloc. RMS X(mm/s):" label-for="x">
                    <b-form-input v-model="data.vibraX" v-bind:class="alerta1"  name="x" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.vibraZ>0" class="m-2" label="Veloc. RMS Z(mm/s):" label-for="z">
                    <b-form-input v-model="data.vibraZ" v-bind:class="alerta2"  name="z" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                 <b-form-group v-if="data.vibraX2>0" class="m-2" label="Acele. Pico X(G):" label-for="x2">
                    <b-form-input v-model="data.vibraX2" v-bind:class="alerta3"  name="x2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.vibraZ2>0" class="m-2" label="Acele. Pico Z(G):" label-for="z2">
                    <b-form-input v-model="data.vibraZ2" v-bind:class="alerta4"  name="z2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.corrente>0" class="m-2" label="Corrente(A):" label-for="z2">
                    <b-form-input v-model="data.corrente" v-bind:class="alerta6"  name="z2" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
                <b-form-group v-if="data.temp>0" class="m-2" label="Temperatura(Cº):" label-for="temp">
                    <b-form-input v-model="data.temp" v-bind:class="alerta5" name="temp" disabled size="lg" type="text"></b-form-input>
                </b-form-group>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "painel",
    created(){
      this.load()
      setInterval(()=>{this.load()},2000)
    },
    data(){
      return{
          data:{}
      }
    },
    methods:{
        load(){
            this.readData()
        },
        getImgUrl(pet) {
            var images = require.context('../assets/', false, /\.png$/)
            return images('./' + pet + ".png")
        },
        async readData() {
        fetch('/nodes/',{
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
        alerta(id){
            switch (id) {
                case 0:
                    return "text-center text-primary"
                case 1:
                    return "text-center text-warning"
                case 2:
                    return "text-center text-danger"
                default:
                    return "text-center"
            }
        },
    },
    computed:{
        motorImg(){
          switch (this.data.estado) {
              case "OK":
                  return this.getImgUrl("motorOk")
                case "falha":
                  return this.getImgUrl("motorFalha")
                 case "alerta":
                  return this.getImgUrl("motorAlerta")
              default:
                  return this.getImgUrl("motorPreto")
          }
        },
        alerta1(){
            return this.alerta(this.data.alerta[0])
        },
         alerta2(){
            return this.alerta(this.data.alerta[1])
        },
         alerta3(){
            return this.alerta(this.data.alerta[2])
        },
         alerta4(){
            return this.alerta(this.data.alerta[3])
        },
        alerta5(){
            return this.alerta(this.data.alerta[4])
        },
        alerta6(){
            return this.alerta(this.data.alerta[5])
        },

    },
    props:{
    },
}
</script>

