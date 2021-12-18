// FROM https://stackoverflow.com/a/2117523
function uuidv4() {
  return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
    (
      c ^
      (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
    ).toString(16)
  );
}

function missingSpeakers(entries, known_ids) {
  missing_speakers = Object.entries(entries).filter(
    (x) => !known_ids.has(x[0])
  );
  missing_speakers.sort((a, b) =>
    a[1].first_line > b[1].first_line
      ? 1
      : b[1].first_line > a[1].first_line
      ? -1
      : 0
  );
  return missing_speakers;
}

var app = new Vue({
  el: "#app",
  data: {
    entries: {},
    talks: {},
    version: "",
  },
  methods: {
    addEntry: function () {
      this.$set(this.entries, uuidv4(), {
        first_line: "",
        second_line: "",
        delay: 5000,
        always_show: true,
      });
    },
    showEntry: function (entry) {
      let url_params = new URLSearchParams(entry).toString();
      fetch("/api?" + url_params);
    },
    removeEntry: function (id) {
      this.$delete(this.entries, id);
    },
    save: function () {
      fetch("/api/storage", {
        method: "POST",
        body: JSON.stringify({
          lower_thirds: this.entries,
          talks: this.talks,
          version: this.version,
        }),
      });
    },
    load: function () {
      fetch("/api/storage")
        .then((req) => req.json())
        .then((storage) => {
          this.entries = storage.lower_thirds;
          this.talks = storage.talks;
          this.version = storage.version;
        });
    },
    importSchedule: function () {
      fetch("/api/import_schedule", { method: "POST" }).then(this.load);
    },
    reset: function () {
      fetch("/api/storage", { method: "DELETE" }).then(this.load);
    },
  },
  mounted() {
    this.load();
  },
  computed: {
    upcomingTalks: function () {
      talk_list = Object.entries(this.talks).map(([talk_id, talk], _) => {
        start = new Date(talk.start);
        end = new Date(talk.start);
        end.setSeconds(end.getSeconds() + talk.duration);
        return { ...talk, id: talk_id, start, end };
      });
      talk_list.sort((a, b) =>
        a.start > b.start ? 1 : b.start > a.start ? -1 : 0
      );
      now = new Date();
      return talk_list.filter((x) => x.end > now);
    },
    alwaysSpeakers: function () {
      return Object.entries(this.entries).filter((x) => x[1].always_show);
    },
    nextTalkSpeakers: function () {
      return this.upcomingTalks.flatMap((talk) => {
        console.log(talk.lower_thirds.map((x) => this.entries[x]));
        return talk.lower_thirds.map((x) => [x, this.entries[x]]);
      });
    },
    nextSpeakers: function () {
      next_speakers = [...this.alwaysSpeakers, ...this.nextTalkSpeakers];
      const speaker_ids = new Set();
      speakers = next_speakers.filter((entry) => {
        if (speaker_ids.has(entry[0])) {
          return false;
        }
        speaker_ids.add(entry[0]);
        return true;
      });
      return [...speakers, ...missingSpeakers(this.entries, speaker_ids)];
    },
  },
});
