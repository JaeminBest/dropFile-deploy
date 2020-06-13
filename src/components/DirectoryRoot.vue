<template>
  <v-container fluid>
    <v-data-iterator
      :items="items"
      item-key="name"
      :single-expand="true"
      hide-default-footer
    >
      <template v-slot:default="{ items, isExpanded, expand }">
        <v-container>
          <v-layout column justify-space-around>
            <v-flex lg12|md12
              v-for="item in items"
              :key="item.name">
              <v-card
                :ripple="false"
                @click="(v) => expand(item, v)">
                <v-card-title>
                  <v-icon>mdi-folder</v-icon>
                  <h4>   /storage/{{ item.name }}</h4>
                  <v-spacer/>
                  <!-- <v-switch
                    :input-value="isExpanded(item)"
                    :label="isExpanded(item) ? '닫기' : '펼쳐서 보기'"
                    class="pl-4 mt-0"
                    @change="(v) => expand(item, v)"
                  ></v-switch> -->
                </v-card-title>
                <v-divider></v-divider>
                <v-list v-if="isExpanded(item)" dense>
                  <v-list-item v-if="item.children.length!=0">
                    <DirectoryRoot v-bind:items="item.children"/>
                  </v-list-item>
                  <v-list-item
                    v-if:="item.files"
                    v-for="file in item.files"
                    :key="file.name">
                    <v-icon>mdi-description</v-icon>
                    <h4>{{ file.name }}</h4>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </template>
    </v-data-iterator>
  </v-container>
  
</template>


<script>
  // import DirectoryBlock from './DirectoryBlock.vue'
  export default {
    name: 'DirectoryRoot',
    components: {
      DirectoryRoot: Object
      // dirblock: DirectoryBlock
    },
    props: {
      source: String,
      items: Array
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>