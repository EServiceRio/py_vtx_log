<template>
    <div>
        <mainmenu></mainmenu>
        <b-container fluid>
        <div class="card-title mt-5 mb-3 pt-3">
            <div class="row">
                <div class="col text-left"><h2>Fábrica</h2></div>    
            </div>
        </div>
        <hr>
        <div class="container-fluid row m-auto">
            <div class="col-auto">
                <painel></painel>
            </div>
        </div>
        </b-container>
    </div>
</template>

<script>
import mainmenu from '@/components/main_menu.vue'
import painel from '@/components/painel.vue'
export default {
    name:'IndexView',
    components: {
    mainmenu,
    painel
  }
}
</script>