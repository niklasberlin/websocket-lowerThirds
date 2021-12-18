// FROM https://stackoverflow.com/a/2117523
function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

var app = new Vue({
  el: '#app',
  data: {
    entries: {},
    talks: {},
    version: ""
  },
  methods: {
    addEntry: function () {
      this.$set(this.entries, uuidv4(), {"first_line": "", "second_line": "", "delay": 5000})
      console.log(this.entries)
    },
    showEntry: function (entry) {
      let url_params = new URLSearchParams(entry).toString();
      fetch('/api?' + url_params)
    },
    removeEntry: function(id) {
      this.$delete(this.entries, id)
    },
    save: function() {
      fetch('/api/storage', {method: "POST", body: JSON.stringify({"lower_thirds":this.entries, "talks":this.talks, "version": this.version})})
    },
    load: function() {
      fetch('/api/storage').then((req) => req.json()).then(storage => { this.entries = storage.lower_thirds; this.talk = storage.talks; this.version = storage.version })
    },
    importSchedule: function() {
      fetch('/api/import_schedule', {method: "POST"}).then(this.load)
    },
    reset: function() {
      fetch('/api/storage', {method: "DELETE"}).then(this.load)
    }
  },
  mounted () {
    this.load();
  }
})