<template>
  <v-app id="inspire">
    <v-app-bar
      app
      color="indigo"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>DropFile</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col class="text-center" align='start' justify="center">
            <h1>DropFile</h1>
            <h2> Content-based Lecture File Path auto-recommendation System </h2>
            <h3> CS372 NLP course Term Project </h3>
            <v-flex lg11>
              <v-row justify="space-around" rows=5>
                <v-spacer/>
                <v-btn class="ma-2" color="primary" dark>New Directory
                  <v-icon dark right>mdi-create-new-folder</v-icon>
                </v-btn>
              </v-row>
            </v-flex>
            <dirroot v-bind:items="items"/>
            <v-file-input show-size label="File input" v-model="file"></v-file-input>
    
            <transition name="fade" hide-on-leave="true">
              <v-container
                v-if="!done"
                v-show="!done">
                <v-row 
                  justify="center"
                  style="height: 100px;"
                >
                  <v-btn color="primary" @click="upload">업로드하기</v-btn>
                  <v-progress-linear
                    :active="true"
                    :background-opacity="0.3"
                    :height="5"
                    :value="progress"
                    color="light-blue"
                  ></v-progress-linear>
                </v-row>
              </v-container>
              <v-container
                v-else
                v-show="done">
                <h4> {{pk}} 해당 디렉토리에 저장하시겠습니까? </h4>
                <v-row 
                  justify="space-between"
                  style="height: 100px;"
                >
                  <v-text-field
                    v-model="new_dir_path"
                  ></v-text-field>
                  <v-btn color="primary" @click="accept">저장하기</v-btn>
                </v-row>
              </v-container>
            </transition>
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
  import DirectoryRoot from '@/components/DirectoryRoot.vue'
  const lodash = require("lodash")

  export default {
    name: 'Main',
    components: {
      dirroot: DirectoryRoot
    },
    props: {
      source: String,
    },
    data: () => ({
      drawer: null,
      progress: 0,
      file: undefined,
      done: false,
      items: [],
      data: {},
      loading: false,
      new_dir_path: "",
      expand: false,
      status: false,
      pk: "",
    }),
    created: function() {
        var that = this;
        setTimeout(() => {
          that.loading = true;
        }, 2000);
        //var response;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/show/`)
              .then(response => {
                this.items = lodash.cloneDeep(response.data);
              })
              .then(() => {
                setTimeout(() => {
                  that.loading = false;
                }, 2000);
              });
          } catch (error) {
            reject(error);
            setTimeout(() => {
              that.loading = false;
            }, 2000);
          }
        });
      },
    methods: {
      upload() {
        var that = this;
        that.expand = true;
        let formData = new FormData();
        formData.append("file", this.file);
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .post(`/api/files/pre-upload/`, formData, {
                headers: {
                  "Content-Type": "multipart/form-data"
                },
                onUploadProgress: function(progressEvent) {
                  this.progress = parseInt(
                    Math.round((progressEvent.loaded * 100) / progressEvent.total)
                  );
                }.bind(this)
              })
              .then(res => {
                this.data = lodash.cloneDeep(res.data);
                this.new_dir_path = this.data.new_dir_path;
                setTimeout(() => {
                  that.done = true;
                }, 2000);
              });
          } catch (error) {
            reject(error);
          }
        });
      },
      accept() {
        var that = this;
        that.loading = true;
        
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/files/${this.data.pk}/accept-upload/?new_dir_path=${this.new_dir_path}`)
              .then(response => {
                this.status = (response.data.status=='no') ? false: true;
                this.pk = response.data.pk;
              })
              .then(() => {
                setTimeout(() => {
                  that.loading = false;
                  that.done = true;
                  that.file = undefined;
                }, 2000);
              });
          } catch (error) {
            reject(error);
            setTimeout(() => {
              that.loading = false;
              that.done = false;
              that.new_dir_path = "";
              that.file = undefined;
            }, 2000);
          }
        });
      },
      updateHierarchy(new_dir_path,pk,name) {
        const dirnames = new_dir_path.split('/');
        var hier = this.items;
        var target = undefined;
        var idx;
        var pos=0;
        while (hier.length!=0) {
          for (idx=0; idx<hier.length; idx++) {
            if (hier[idx].name==dirnames[pos]) {
              target = hier;
              hier = hier[idx].children;
            }
          }
          pos++;
        }
        if (pos==dirnames.length) {
          target.files.push({'pk':this.pk,'name':name,'path':new_dir_path+'/'+name})
        }
      }
    }
  }
</script>

<style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
  h1 {font-size:128px;}
</style>