import Vue from 'vue';

// Lib imports
import axios from 'axios';

Vue.prototype.$http = axios;
axios.defaults.headers.get['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.get['Access-Control-Allow-Credentials'] = true;

axios.defaults.proxy = true;
axios.defaults.debug = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";