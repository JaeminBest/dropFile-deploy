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
            <h2> Content-based PDF Document Path Auto-Recommendation System </h2>
            <h3> CS372 NLP course Term Project </h3>
            <v-row align="start" justify="center">
              <!-- <v-col lg="2" md="2" xs="2"> 
                <v-spacer/> 
                <v-btn
                  color="indigo"
                  dark
                  @click="fetch()"
                >
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </v-col> -->
              <v-col lg="9" md="9" xs="9"> <v-spacer/> </v-col>
              <v-col lg="2" md="2" xs="2">
                <v-dialog v-model="dialog1" persistent max-width="700">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      color="indigo"
                      dark
                      v-bind="attrs"
                      v-on="on"
                      @click="dirPath=parentPath"
                    >
                      New Directory
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="headline">만들 디렉토리의 경로는 무엇인가요?</v-card-title>
                    <v-card-text>
                      <v-row justify="center">
                        <v-text-field
                          v-model="dirPath"
                          hint="path should start with ROOT PATH"
                          :disabled="lock1"
                        ></v-text-field>
                      </v-row>
                      <v-col justify="center" align="center">
                        <v-progress-circular indeterminate color="indigo" v-if="loading1"/>
                        <div v-if="msg1.length!=0">
                          <h3>{{msg1}}</h3>
                        </div>
                      </v-col>
                    </v-card-text>
                    <v-card-actions v-if="!btn1">
                      <v-spacer></v-spacer>
                      <v-btn color="indigo" text :disabled="loading1" @click="dialog1 = false; msg1=''">만들지 않을래요</v-btn>
                      <v-btn color="indigo" text :disabled="dirPath.length==0 || loading1" @click="createDirectory(dirPath); dirPath=''">이걸로 만들게요</v-btn>
                    </v-card-actions>
                    <v-card-actions v-else>
                      <v-spacer></v-spacer>
                      <v-btn color="indigo" text @click="dialog1 = false; btn1 = false; msg1=''; lock1 = false; dirPath=''">돌아가기</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-col>
            </v-row>
            <v-row align="start" justify="center">
              <v-col lg="10" md="10" xs="10">
                <v-card height="700px">
                  <dirroot v-if="!loading"
                    v-bind:items="items" 
                    v-bind:parentPath="parentPath"
                    :isparent="true"/>
                  <v-overlay
                    :absolute="true"
                    :value="overlay"
                  >
                    <v-progress-circular color="indigo" indeterminate/>
                  </v-overlay>
                </v-card>
              </v-col>
            </v-row>
            <transition name="fade" hide-on-leave="true">
              <v-row align="start" justify="center" v-if="!btn2">
                <v-col lg="9" md="9" xs="9">
                  <v-file-input
                    show-size 
                    :disabled="loading2"  
                    label="File input" 
                    v-model="file"
                  />
                </v-col>
                <v-col lg="1" md="1" xs="1">
                  <v-btn v-if="!loading2" color="indigo" dark @click="upload()">DROP</v-btn>
                  <v-progress-circular v-else color="indigo" indeterminate/>
                </v-col>
              </v-row>
              <v-row align="start" justify="center" v-else>
                <v-col lg="10" md="10" xs="10">
                  <div v-if="msg2.length!=0">
                    {{msg2}}
                  </div>
                  <div v-else>
                    <h4> 해당 디렉토리에 저장하시겠습니까? </h4>
                  </div>
                </v-col>
                <v-col lg="9" md="9" xs="9">
                  <v-text-field
                    label="저장될 디렉토리 경로"
                    :readonly="loading3 || lock2"
                    placeholder="추천 디렉토리 경로가 없습니다"
                    v-model="new_dir_path"
                  ></v-text-field>
                </v-col>
                <v-col lg="1" md="1" xs="1">
                  <v-btn v-if="msg2.length!=0" color="indigo" dark @click="dialog2 = false; btn2 = false; msg2=''; lock2 = false;">돌아가기</v-btn>
                  <v-btn v-else-if="!loading3" 
                    color="indigo" 
                    dark @click="accept()">
                    ACCEPT
                  </v-btn>
                  <v-progress-circular v-else color="indigo" indeterminate/>
                </v-col>
              </v-row>
            </transition>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer
      color="indigo"
      app
    >
      <span class="white--text">&copy; 2020 CS372 Project</span>
    </v-footer>
  </v-app>
</template>

<script>
  import DirectoryRoot from '@/components/DirectoryRoot.vue'
  import { mapMutations, mapGetters } from 'vuex'
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
      status: false,
      pk: "",
      msg1: "",
      msg2: "",
      dirPath: "",
      loading1: false,
      loading2: false,
      loading3: false,
      btn1: false,
      btn2: false,
      dialog1: false,
      overlay: false,
      lock1: false,
      lock2: false,
      parentPath: "",
    }),
    created: function() {
      this.fetch();
    },
    computed: {
      ...mapGetters('fetch', ['fetchFlag']),
    },
    watch: {
      fetchFlag: function(a,b) {
        if (a && !b) {
          setTimeout(() => {
            this.fetch();
            this.switchOff();
          }, 2000);
        }
      }
    },
    methods: {
      ...mapMutations('fetch',[
        'switchOff'
      ]),
      ...mapMutations('fetch',[
        'switchOn'
      ]),
      fetch() {
        var that = this;
        that.loading = true;
        that.overlay = true;
        //var response;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/show/`)
              .then(response => {
                this.items = lodash.cloneDeep(response.data.items);
                this.parentPath = response.data.parent_path;
              })
              .then(() => {
                setTimeout(() => {
                  that.loading = false;
                  that.overlay = false;
                  this.switchOff();
                }, 2000);
              });
          } catch (error) {
            setTimeout(() => {
              that.loading = false;
              that.overlay = false;
            }, 2000);
            reject(error);
          }
        });
      },
      upload() {
        var that = this;
        that.loading2 = true;
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
                setTimeout(() => {
                  that.loading2 = false;
                  that.btn2 = true;
                  this.new_dir_path = this.data.new_dir_path;
                }, 2000);
              });
          } catch (error) {
            setTimeout(() => {
              that.loading2 = false;
            }, 2000);
            reject(error);
          }
        });
      },
      accept() {
        var that = this;
        that.loading3 = true;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/files/${this.data.pk}/accept-upload/?new_dir_path=${this.new_dir_path}`)
              .then(response => {
                if (response.data.status=='no') {
                  setTimeout(() => {
                    that.loading3 = false;
                    that.lock2 = false;
                    this.msg2 = "파일 업로드에 실패했습니다. 이미 존재하는 디렉토리의 하위 경로로 입력해주세요.";
                  }, 2000);
                  throw "file upload error";
                }
                this.pk = response.data.pk;
              })
              .then(() => {
                setTimeout(() => {
                  that.loading3 = false;
                  that.file = undefined;
                  that.new_dir_path = '';
                  this.msg2 = "파일 업로드에 성공했습니다. 더 업로드하고 싶다면 '돌아가기' 버튼을 눌러주세요";
                  this.switchOn();
                }, 2000);
              });
          } catch (error) {
            setTimeout(() => {
              that.loading3 = false;
              that.new_dir_path = "";
              that.file = undefined;
            }, 2000);
            reject(error);
          }
        });
      },
      createDirectory(dirPath) {
        var that = this;
        that.loading1 = true;
        that.lock1 = true;
        let formData = new FormData();
        formData.append("path", dirPath);
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .post(`/api/dirs/`, formData, {
                headers: {
                  "Content-Type": "multipart/form-data"
                },
              })
              .then(res => {
                if (res.data.status=='no') {
                  setTimeout(() => {
                    that.loading1 = false;
                    that.lock1 = false;
                    this.msg1 = "디렉토리 생성에 실패했습니다. 이미 존재하는 디렉토리의 하위 경로로 입력해주세요.";
                    this.dirPath = this.parentPath;
                  }, 2000);
                  throw "create directory error";
              }})
              .then(() => {
                setTimeout(() => {
                    that.loading1 = false;
                    that.btn1 = true;
                    this.msg1 = "성공적으로 디렉토리를 만들었습니다";
                    this.switchOn();
                  }, 2000);
              });
          } catch (error) {
            reject(error);
            
          }
        });
      },
      track() {

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
  .disable-events {
  pointer-events: none
}
</style>