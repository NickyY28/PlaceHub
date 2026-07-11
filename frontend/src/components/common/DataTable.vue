<template>
  <div class="card shadow-sm border-0">
    <div class="card-body">
      <div v-if="search" class="mb-3">
        <input
          v-model="searchText"
          class="form-control"
          placeholder="Search..."
        />
      </div>

      <div v-if="loading" class="text-center py-5">Loading...</div>

      <div
        v-else-if="filteredRows.length === 0"
        class="text-center py-5 text-muted"
      >
        No Data Found
      </div>

      <div v-else class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>#</th>

              <th
                v-for="column in columns"
                :key="column.key"
                @click="sort(column.key)"
                style="cursor: pointer"
              >
                {{ column.label }}
              </th>

              <th v-if="$slots.actions">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(row, index) in paginatedRows" :key="row.id">
              <td>
                {{ (currentPage - 1) * perPage + index + 1 }}
              </td>

              <td v-for="column in columns" :key="column.key">
                <slot :name="column.key" :row="row">
                  {{ row[column.key] }}
                </slot>
              </td>

              <td v-if="$slots.actions">
                <slot name="actions" :row="row" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @change="changePage"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

import Pagination from "./Pagination.vue";

const props = defineProps({
  columns: Array,

  rows: Array,

  loading: Boolean,

  search: {
    type: Boolean,
    default: true,
  },

  perPage: {
    type: Number,
    default: 10,
  },
});

const searchText = ref("");

const currentPage = ref(1);

const sortKey = ref("");

const asc = ref(true);

const filteredRows = computed(() => {
  let data = [...props.rows];

  if (searchText.value) {
    data = data.filter((item) =>
      JSON.stringify(item)

        .toLowerCase()

        .includes(searchText.value.toLowerCase())
    );
  }

  if (sortKey.value) {
    data.sort((a, b) => {
      if (a[sortKey.value] > b[sortKey.value]) return asc.value ? 1 : -1;

      if (a[sortKey.value] < b[sortKey.value]) return asc.value ? -1 : 1;

      return 0;
    });
  }

  return data;
});

const totalPages = computed(() => {
  return Math.ceil(filteredRows.value.length / props.perPage) || 1;
});

const paginatedRows = computed(() => {
  const start = (currentPage.value - 1) * props.perPage;

  return filteredRows.value.slice(
    start,

    start + props.perPage
  );
});

const sort = (key) => {
  if (sortKey.value === key) {
    asc.value = !asc.value;
  } else {
    sortKey.value = key;

    asc.value = true;
  }
};

const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;

  currentPage.value = page;
};
</script>
