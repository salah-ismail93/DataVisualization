<template>
  <div class = "flex flex-col min-h-screen font-Roboto mr-20" >
    <HeaderComponent/>
    <RouterView/>
  </div>
</template>
<script>
import HeaderComponent from "./components/HeaderComponent.vue";

export default {
  name: "App",
  components: {
    HeaderComponent
  },
};
</script>

<style scoped>
.mr-20{
      margin-right: 20rem;

}
</style>