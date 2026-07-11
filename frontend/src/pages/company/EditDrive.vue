<script setup>
import { reactive, onMounted } from "vue";

import { useRoute, useRouter } from "vue-router";

import PageHeader from "../../components/common/PageHeader.vue";

import { getDrive, updateDrive } from "../../api/company";
const route = useRoute();
const router = useRouter();
const form = reactive({});
const load = async () => {
  const { data } = await getDrive(route.params.id);

  Object.assign(form, data);
};

const save = async () => {
  await updateDrive(
    route.params.id,

    form
  );

  router.push("/company/drives");
};

onMounted(load);
</script>
