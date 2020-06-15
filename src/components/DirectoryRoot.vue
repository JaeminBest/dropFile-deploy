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
                </v-card-title>
                <v-divider></v-divider>
                <v-list v-if="isExpanded(item)" dense>
                  <v-list-item v-if="item.children.length!=0">
                    <DirectoryRoot v-bind:items="item.children"/>
                  </v-list-item>
                  <v-list-item
                    v-for="file in item.files"
                    :key="file.name">
                    <v-icon>mdi-description</v-icon>
                    <h4>{{ file.name }}</h4>
                    <v-spacer/>
                    <v-dialog v-model="dialog1" persistent max-width="290">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="light-blue"
                          dark
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon @click="downloadFile(item.pk)">mdi-get-app</v-icon>
                          Download
                        </v-btn>
                      </template>
                      <v-card>
                        <v-card-title class="headline">다운로드하시겠습니까?</v-card-title>
                        <v-col justify="center" align="center">
                          <v-progress-circular v-show="loading1"/>
                          <h3>{{msg1}}</h3>
                        </v-col>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog1 = false">아니요</v-btn>
                          <v-btn color="light-blue" text @click="downloadfile(item.pk)">네</v-btn>
                        </v-card-actions>
                        <v-card-actions v-if="msg1">
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog1 = false; msg1=''">돌아가기</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialog2" persistent max-width="290">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="light-blue"
                          dark
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon>mdi-trending-flat</v-icon>
                          Move
                        </v-btn>
                      </template>
                      <v-card>
                        <v-card-title class="headline">어디로 옮기시겠습니까?</v-card-title>
                        <v-row justify="center">
                          <v-text-field
                            v-model="new_dir_path"
                          ></v-text-field>
                        </v-row>
                        <v-col justify="center" align="center">
                          <v-progress-circular v-show="loading2"/>
                          <h3>{{msg2}}</h3>
                        </v-col>
                        <v-card-actions v-if="!loading2">
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog2 = false">옮기지 않을래요</v-btn>
                          <v-btn color="light-blue" text disabled="!new_dir_path" @click="moveFile(item.pk,new_dir_path)">여기로 옮길게요</v-btn>
                        </v-card-actions>
                        <v-card-actions v-if="msg2">
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog2 = false; msg2=''">돌아가기</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialog3" persistent max-width="290">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          color="light-blue"
                          dark
                          v-bind="attrs"
                          v-on="on"
                        >
                          <v-icon >mdi-delete</v-icon>
                          Delete
                        </v-btn>
                      </template>
                      <v-card>
                        <v-card-title class="headline">정말 지우시겠습니까?</v-card-title>
                        <v-col justify="center" align="center">
                          <v-progress-circular v-show="loading3"/>
                          <h3>{{msg3}}</h3>
                        </v-col>
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog3 = false">아니요</v-btn>
                          <v-btn color="light-blue" text @click="deleteFile(item.pk)">네</v-btn>
                        </v-card-actions>
                        <v-card-actions v-if="msg3">
                          <v-spacer></v-spacer>
                          <v-btn color="light-blue" text @click="dialog3 = false; msg3=''">돌아가기</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
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
      dialog1: false,
      dialog2: false,
      dialog3: false,
      loading1: false,
      loading2: false,
      loading3: false,
      msg1: "",
      msg2: "",
      msg3: "",
      new_dir_path: "",
    }),
    methods: {
      downloadFile(pk) {
        var that = this;
        setTimeout(() => {
          that.loading2 = true;
        }, 2000);
        //var response;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/files/${pk}/`)
              .then(res => {
                if (res.data.status!='ok') {
                  throw "파일 다운로드에 실패했습니다. 관리자에게 문의하십시오"
                }
              })
              .then(() => {
                setTimeout(() => {
                  that.loading1 = false;
                  that.dialog1 = false;
                  that.msg1 = "파일 다운로드에 성공했습니다";
                }, 2000);
              });
          } catch (error) {
            reject(error);
            setTimeout(() => {
              that.loading1 = false;
              that.msg1 = error;
            }, 2000);
          }
        });
      },
      moveFile(pk,new_dir_path) {
        var that = this;
        setTimeout(() => {
          that.loading2 = true;
        }, 2000);
        //var response;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .get(`/api/files/${pk}/move?new_dir_path=${new_dir_path}`)
              .then(res => {
                if (res.data.status!='ok') {
                  throw "파일 옮기기에 실패했습니다, 올바른 디렉토리 경로가 아닙니다"
                }
              })
              .then(() => {
                setTimeout(() => {
                  that.loading2 = false;
                  that.dialog2 = false;
                  that.msg2 = "성공적으로 파일을 옮겼습니다";
                }, 2000);
              });
          } catch (error) {
            reject(error);
            setTimeout(() => {
              that.loading2 = false;
              that.msg2 = error;
            }, 2000);
          }
        });
      },
      deleteFile(pk) {
        var that = this;
        setTimeout(() => {
          that.loading3 = true;
        }, 2000);
        //var response;
        return new Promise((resolve, reject) => {
          try {
            this.$http
              .delete(`/api/files/${pk}/`)
              .then(res => {
                if (res.data.status!='ok') {
                  throw "파일 삭제에 실패했습니다. 관리자에게 문의하십시오."
                }
              })
              .then(() => {
                setTimeout(() => {
                  that.loading3 = false;
                  that.dialog3 = false;
                  that.msg3 = "성공적으로 파일을 삭제했습니다";
                }, 2000);
              });
          } catch (error) {
            reject(error);
            setTimeout(() => {
              that.loading3 = false;
              that.msg3 = error;
            }, 2000);
          }
        });
      }
    }
  }
</script>