// Dictionary that maps flag_id to filename
var FLAGNAMES = {
  1: "Spain",
  2: "Uruguay",
  3: "Spain_Uruguay",
  4: "Portugal",
  5: "Brazil",
  6: "Portugal_Brazil",
  7: "United-Kingdom",
  8: "Netherlands",
  9: "United-States",
  10: "France",
  11: "Denmark",
  13: "Sweden",
  15: "Mexico",
  17: "Norway",
  18: "Denmark_Baltic",
  19: "Argentina",
  20: "Russia"
};

// year label
Vue.component("v-voyage-info", {
  props: ["data", "isVisible"],
  template: `<div class="timelapse-info-container timelapse-info-card" v-if="isVisible">
              <div class='voyage-title-container'>
                <div class='voyage-info-title'>
                  {{shipName}}
                </div>
                <div class='voyage-info-close' @click="close">
                  <i class='fas fa-times'></i>
                </div>
              </div>

              <div class='voyage-nationality-container' v-if="nationalityName">
                <div class='voyage-nationality-title'>
                  {{nationalityName}}
                </div>
                <img :src="flagImgSrc" class='voyage-nationality-flag'>
              </div>

              <div class='voyage-description-container'>
                <p>
                  This <span v-if="shipTonnage">{{shipTonnage}} ton(s)</span> ship 
                  left {{data.source}} with {{data.embarked}} enslaved people and 
                  arrived in {{data.destination}} with {{data.disembarked}}.
                </p>
              </div>

              <div class='voyage-actions-container'>
                <button type="button" class="btn btn-info btn-sm" @click="readMore">Read More</button>
              </div>

            </div>`,

  created() {},
  computed: {
    // compute ship name, which comes from the data object
    shipName() {
      var shipName = (this.data.ship_name || "").trim();
      shipName = shipName != "" ? shipName : gettext("Ship Name Unknown");
      return shipName;
    },

    // compute ship nationality, which comes from the data object
    nationalityName() {
      return this.data.ship_nationality_name || false;
    },

    // compute tonnage
    shipTonnage() {
      return this.data.ship_ton ? parseInt(this.data.ship_ton) : false;
    },

    // // compute voyage link
    // voyageHref() {
    //   return "/voyage/" + this.data.voyage_id + "/variables";
    // },

    // compute flag
    flag() {
      return "flag_" + this.data.nat_id;
    },

    // compute flag image source
    flagImgSrc() {
      var filename = FLAGNAMES[this.data.nat_id];
      var path = "/static/images/flags/";
      var extension = ".png";
      return path + filename + extension;
    }
  },
  methods: {
    close() {
      this.$emit("close-timelapse-info");
    },
    readMore() {
      $vm = this;
      var request = buildRequestBody(this.data.voyage_id, SV_MODE == "intra");
      axios({
        method: "POST",
        url: SEARCH_URL,
        data: request
      })
        .then(function(response) {
          console.log(response.data.data[0]);
          var processedResponse = processResponse(response.data);
          $vm.$emit("set-row-data", processedResponse);
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
});

// year label
Vue.component("v-year", {
  props: ["currentYear"],
  template: `<div class="timelapse-info-container" id="timelapse-year">
        <div class="timelapse-year">{{currentYear}}</div>
        </div>`
});

// speed shifter
Vue.component("v-speed", {
  props: ["speeds", "multiplier", "ui", "options", "control"],
  data: function() {
    return {
      currentIndex: 1
    };
  },
  template:
    '<button type="button" class="btn btn-sm btn-light margin" :class="{ active: isActive }" @click=shift>{{currentSpeed}}x</button>',
  methods: {
    shift: function() {
      // update UI display
      var next = this.currentIndex + 1;
      if (next < this.speeds.length) {
        Vue.set(this, "currentIndex", this.currentIndex + 1);
      } else {
        Vue.set(this, "currentIndex", 0);
      }

      // update animation speed
      var multipliedSpeed = this.speeds[this.currentIndex] * this.multiplier;
      console.log("multiplied speed is: " + multipliedSpeed);
      this.ui.monthsPerSecond = multipliedSpeed;
      this.control.setStepPerSec(
        multipliedSpeed * 10,
        Math.max(1.0, 12 / multipliedSpeed)
      );
    }
  },
  computed: {
    // returns the currentSpeed as a text label
    currentSpeed: function() {
      return this.speeds[this.currentIndex];
    },

    // set this to active whenever it is not the default speed (1x)
    isActive: function() {
      return this.currentIndex != 1;
    }
  }
});

// play/pause button
Vue.component("v-play", {
  props: ["ui", "control"],
  data: function() {
    return {
      play: false,
    };
  },
  template: `<button type="button" class="btn btn-sm btn-light" @click=toggle v-if="play"><i class="fas fa-play"></i></button>
  <button type="button" class="btn btn-sm btn-light" @click=toggle v-else><i class="fas fa-pause"></i></button>`,
  methods: {
    toggle: function() {
      this.play = !this.play;
      if (this.control.isPaused()) {
        this.ui.play();
      } else {
        this.ui.pause();
      }
    }
  }
});

// fullscreen toggle button
Vue.component("v-fullscreen", {
  data: function() {
    return {
      isFullscreen: false
    };
  },
  template: `<button type="button" class="btn btn-sm btn-light" @click=toggle><i class="fas fa-compress"></i></button>`,
  methods: {
    toggle: function() {
      if (this.isFullscreen) {
        this.exitFullscreen();
      } else {
        this.enterFullscreen();
      }
      this.isFullscreen = !this.isFullscreen;
    },

    // enter fullscreen based on browser
    enterFullscreen: function() {
      var mapContainer = voyagesMap._map.getContainer();
      if (mapContainer.requestFullscreen) {
        mapContainer.requestFullscreen();
      } else if (mapContainer.mozRequestFullScreen) {
        /* Firefox */
        mapContainer.mozRequestFullScreen();
      } else if (mapContainer.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        mapContainer.webkitRequestFullscreen();
      } else if (mapContainer.msRequestFullscreen) {
        /* IE/Edge */
        mapContainer.msRequestFullscreen();
      }
    },

    // exit fullscreen based on browser
    exitFullscreen: function() {
      var mapContainer = voyagesMap._map.getContainer();
      if (mapContainer.requestFullscreen) {
        document.exitFullscreen();
      } else if (mapContainer.mozRequestFullScreen) {
        /* Firefox */
        document.mozCancelFullScreen();
      } else if (mapContainer.webkitRequestFullscreen) {
        /* Chrome, Safari and Opera */
        document.webkitExitFullscreen();
      } else if (mapContainer.msRequestFullscreen) {
        /* IE/Edge */
        document.msExitFullscreen();
      }
    }
  }
});
