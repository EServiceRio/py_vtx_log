<template>
    <div>
    <label class="m-auto pr-3" for="ini-data">{{label}}</label>
    <b-input-group>
        <b-form-input
            @change=" mudaDataIni(false)"
            :state="iniDataState"
            :id="id+'ini-data'"
            v-model="iniDataFormatada"
            type="text"
            autocomplete="off"
            placeholder="DD-MM-AAAA"
        ></b-form-input>
        <b-input-group-append>
            <b-form-datepicker
                @input=" mudaDataIni(true)"
                v-model="iniData"
                right
                button-only
                locale="br"
                :area-controls="id+'ini-data'"
            ></b-form-datepicker>
        </b-input-group-append>
    </b-input-group>
        <b-input-group>
        <b-form-input
            @change="mudaTimeIni(false)"
            :state="iniTimeState"
            :id="id +'ini-time'"
            v-model="iniTimeFormatada"
            type="text"
            autocomplete="off"
            placeholder="HH:MM"
        ></b-form-input>
        <b-input-group-append>
            <b-form-timepicker
                @input="mudaTimeIni(true)"
                v-model="iniTime"
                locale="br"
                v-bind="timeLabels"
                right
                button-only
                :area-controls="id + 'ini-time'"
            ></b-form-timepicker>
        </b-input-group-append>
    </b-input-group>
    </div>
</template>

<script>
export default {
    name:'dataTime',
    created(){
      this.load()
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
      load(){
        if(this.value.length>0){
          let buffer = this.value.split('T')
          this.iniData = buffer[0]
          this.mudaDataIni(true)
          this.iniTime = buffer[1]
          this.mudaTimeIni(true)
        }
    },
    mudaIni(){
        if(this.iniDataState && this.iniTimeState){
            this.ini=`${this.iniData}T${this.iniTime}`
            this.$emit('check',this.ini)
        }else{
            this.ini=""
            this.$emit('check',"")
        }
    },
    mudaDataIni(reverter){
        var buffern = ""
        if(reverter){
            buffern = this.iniData.split('-')
        }else{
            buffern = this.iniDataFormatada.split('-')
        }
        if(buffern.length==3){
            if(reverter){this.iniDataFormatada = `${buffern[2]}-${buffern[1]}-${buffern[0]}`}
            else{this.iniData = `${buffern[2]}-${buffern[1]}-${buffern[0]}`}
            this.iniDataState=true
            this.mudaIni()
        }
        else{
            this.iniDataFormatada=""
            this.iniData=""
            this.iniDataState=false
            this.$emit('check',"")
        }
    },
    mudaTimeIni(reverter){
        var bufferx = ""
        if(reverter){
            bufferx = this.iniTime.split(':')
            this.iniTimeFormatada=`${bufferx[0]}:${bufferx[1]}`
            this.iniTimeState=true
            this.mudaIni()
        }else{
            bufferx = this.iniTimeFormatada.split(':')
            if(bufferx.length==2){
                if(bufferx[0]>=0 && bufferx[0]<24 && bufferx[1]>-1 && bufferx[1]<61){
                    this.iniTime=this.iniTimeFormatada
                    this.iniTimeState=true
                    this.mudaIni()
                }else{
                    this.iniTimeState=false
                    this.iniTime=""
                    this.iniTimeFormatada=""
                    this.$emit('check',"")
                }
            }else{
                this.iniTime=""
                this.iniTimeFormatada=""
                this.iniTimeState=false
                this.$emit('check',"")
            }
        }
    },
    },
    data(){
      return{
        ini:this.value,
        iniData: "",
        iniDataFormatada:"",
        iniDataState: false,
        iniTime: "",
        iniTimeFormatada: "",
        iniTimeState: false,
        timeLabels: {
            labelHours: 'Horas',
            labelMinutes: 'Minutos',
            labelSeconds: 'Segundos',
            labelIncrement: '+',
            labelDecrement: '-',
            labelSelected: 'Selecionado',
            labelNoTimeSelected: 'Sem Seleção',
            labelCloseButton: 'Fechar'
            }
      }
    },
    computed:{
    },
    props:{
      value: {
        type: String,
        required: false,
        default: "",
      },
      label: {
        type: String,
        required: false,
        default: "",
      },
      id: {
        type: String,
        required: false,
        default: "0",
      },
    },
}
</script>