// FROM https://stackoverflow.com/a/2117523
function uuidv4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

var app = new Vue({
  el: '#app',
  data: {
    entries: []
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
      delete this.entries[id]
    },
    saveEntries: function() {
      fetch('/api/lower_thirds', {method: "POST", body: JSON.stringify(this.entries)})
    },
    loadEntries: function() {
      fetch('/api/lower_thirds').then((req) => req.json()).then((ent) => this.entries = ent)
    },
    importSchedule: function() {
      fetch('/api/import_schedule', {method: "POST"})
    }
  },
  mounted () {
    this.loadEntries();
  }
})