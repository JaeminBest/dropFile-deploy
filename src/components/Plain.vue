<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list dense>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
            <v-icon>mdi-email</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Contact</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Application</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col class="text-center">
            <v-container fluid>
              <v-data-iterator
                :items="items"
                item-key="name"
                :single-expand="true"
                hide-default-footer
              >
                <template v-slot:default="{ items, isExpanded, expand }">
                  <v-row>
                    <v-col
                      v-for="item in items"
                      :key="item.name"
                      cols="12"
                      sm="6"
                      md="4"
                      lg="3"
                    >
                      <v-card>
                        <v-card-title>
                          <h4>{{ item.name }}</h4>
                        </v-card-title>
                        <v-switch
                          :input-value="isExpanded(item)"
                          :label="isExpanded(item) ? 'Expanded' : 'Closed'"
                          class="pl-4 mt-0"
                          @change="(v) => expand(item, v)"
                        ></v-switch>
                        <v-divider></v-divider>
                        <v-list v-if="isExpanded(item)" dense>
                          <v-list-item>
                            <v-list-item-content>Calories:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.calories }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Fat:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.fat }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Carbs:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.carbs }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Protein:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.protein }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Sodium:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.sodium }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Calcium:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.calcium }}</v-list-item-content>
                          </v-list-item>
                          <v-list-item>
                            <v-list-item-content>Iron:</v-list-item-content>
                            <v-list-item-content class="align-end">{{ item.iron }}</v-list-item-content>
                          </v-list-item>
                        </v-list>
                      </v-card>
                    </v-col>
                  </v-row>
                </template>
              </v-data-iterator>
            </v-container>
            <v-file-input show-size label="File input"></v-file-input>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
  // import Login from './Login.vue'
  export default {
    name: 'Plain',
    // components: {
    //   Login
    // },
    props: {
      source: String,
      items: 
    },
    data: () => ({
      drawer: null,
    }),
  }
</script>