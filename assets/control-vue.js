var app = new Vue({
  el: '#app',
  data: {
    entries: []
  },
  methods: {
    addEntry: function () {
      this.entries.push({"first_line": "", "second_line": "", "delay": 5000})
    },
    showEntry: function (entry) {
      let url_params = new URLSearchParams(entry).toString();
      fetch('/api?' + url_params)
    },
    removeEntry: function(idx) {
      this.entries.splice(idx, 1);
    }
  }
})