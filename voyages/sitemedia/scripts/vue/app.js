// main app
var searchBar = new Vue({
	el: "#search-bar",
	delimiters: ['{{', '}}'],
	data: {
		isAdvanced: true,
		searchFilter: {
			groups: {
				year: year,
				shipNationOwner: shipNationOwner,
				slave: slave,
				itinerary: itinerary,
				captainAndCrew: captainAndCrew,
				source: source,
			},
			outcome1: outcome1,
			outcome2: outcome2,
			outcome3: outcome3,
			outcome4: outcome4,
			outcome5: outcome5,
		},
    places: {},
    ports: {},
		searchQuery: {
			// put the search query in here
		},
		saved: [],
    menuAim: null,
	},
	computed: {
	},
	watch: {
		isAdvanced: function(val){
		},

		searchFilter: {
			handler: function(val){
				// slave count
				this.searchFilter.groups.slave.overallNumbers.count.activated = countActivated(this.searchFilter.groups.slave.overallNumbers);
				this.searchFilter.groups.slave.overallNumbers.count.changed = countChanged(this.searchFilter.groups.slave.overallNumbers);
				this.searchFilter.groups.slave.purchaseNumbers.count.activated = countActivated(this.searchFilter.groups.slave.purchaseNumbers);
				this.searchFilter.groups.slave.purchaseNumbers.count.changed = countChanged(this.searchFilter.groups.slave.purchaseNumbers);
				this.searchFilter.groups.slave.landingNumbers.count.activated = countActivated(this.searchFilter.groups.slave.landingNumbers);
				this.searchFilter.groups.slave.landingNumbers.count.changed = countChanged(this.searchFilter.groups.slave.landingNumbers);
				this.searchFilter.groups.slave.percentageBySexAndAgeGroup.count.activated = countActivated(this.searchFilter.groups.slave.percentageBySexAndAgeGroup);
				this.searchFilter.groups.slave.percentageBySexAndAgeGroup.count.changed = countChanged(this.searchFilter.groups.slave.percentageBySexAndAgeGroup);
				this.searchFilter.groups.slave.otherCharacteristics.count.activated = countActivated(this.searchFilter.groups.slave.otherCharacteristics);
				this.searchFilter.groups.slave.otherCharacteristics.count.changed = countChanged(this.searchFilter.groups.slave.otherCharacteristics);

				this.searchFilter.groups.slave.count.activated = countMenuActivated(this.searchFilter.groups.slave);
				this.searchFilter.groups.slave.count.changed = countMenuChanged(this.searchFilter.groups.slave);

				// source count
				this.searchFilter.groups.source.source.count.activated = countActivated(this.searchFilter.groups.source.source);
				this.searchFilter.groups.source.source.count.changed = countChanged(this.searchFilter.groups.source.source);
				this.searchFilter.groups.source.count.activated = countMenuActivated(this.searchFilter.groups.source);
				this.searchFilter.groups.source.count.changed = countMenuChanged(this.searchFilter.groups.source);

				//SNO
				this.searchFilter.groups.shipNationOwner.voyagesAndVessels.count.activated = countActivated(this.searchFilter.groups.shipNationOwner.voyagesAndVessels);
				this.searchFilter.groups.shipNationOwner.voyagesAndVessels.count.changed = countChanged(this.searchFilter.groups.shipNationOwner.voyagesAndVessels);
				this.searchFilter.groups.shipNationOwner.constructionAndRegistration.count.activated = countActivated(this.searchFilter.groups.shipNationOwner.constructionAndRegistration);
				this.searchFilter.groups.shipNationOwner.constructionAndRegistration.count.changed = countChanged(this.searchFilter.groups.shipNationOwner.constructionAndRegistration);
				this.searchFilter.groups.shipNationOwner.rigTonnageAndGunsMounted.count.activated = countActivated(this.searchFilter.groups.shipNationOwner.rigTonnageAndGunsMounted);
				this.searchFilter.groups.shipNationOwner.rigTonnageAndGunsMounted.count.changed = countChanged(this.searchFilter.groups.shipNationOwner.rigTonnageAndGunsMounted);
				this.searchFilter.groups.shipNationOwner.count.activated = countMenuActivated(this.searchFilter.groups.shipNationOwner);
				this.searchFilter.groups.shipNationOwner.count.changed = countMenuChanged(this.searchFilter.groups.shipNationOwner);

				// captain and crew
				this.searchFilter.groups.captainAndCrew.captainAndCrew.count.activated = countActivated(this.searchFilter.groups.captainAndCrew.captainAndCrew);
				this.searchFilter.groups.captainAndCrew.captainAndCrew.count.changed = countChanged(this.searchFilter.groups.captainAndCrew.captainAndCrew);
				this.searchFilter.groups.captainAndCrew.count.activated = countMenuActivated(this.searchFilter.groups.captainAndCrew);
				this.searchFilter.groups.captainAndCrew.count.changed = countMenuChanged(this.searchFilter.groups.captainAndCrew);
			},
			deep: true,
		},

	},

	methods: {
		// go over items and update counts when the inputs are changed
		changed(variable, changed) {
			// function to locate a variable
			for (key1 in this.searchFilter.groups) {
				for (key2 in this.searchFilter.groups[key1]) {
					if (key2 !== "count") {
						for (key3 in this.searchFilter.groups[key1][key2]) {
							if (key3 == variable.varName) {
								console.log(key3);
								console.log(this.searchFilter.groups[key1][key2][key3]);
								this.searchFilter.groups[key1][key2][key3].changed = changed;
								this.searchFilter.groups[key1][key2][key3].value["searchTerm0"] = variable["searchTerm0"];
								this.searchFilter.groups[key1][key2][key3].value["searchTerm1"] = variable["searchTerm1"];
								this.searchFilter.groups[key1][key2][key3].value["op"] = variable["op"];
							}
						}
					}
				}
			}
			// function to locate a variable
    },

		// turn changed items into activated state; then execute search
		apply(group, subGroup, filterValues) {
			activateFilter(this.searchFilter.groups, group, subGroup, filterValues);
			var searchTerms = searchAll(this.searchFilter.groups);
			alert(JSON.stringify(searchTerms));
			search(this.searchFilter, searchTerms);
		},

		// reset inputs, filters, and counts back to default state
		reset(group, subGroup) {
			resetFilter(this.searchFilter.groups, group, subGroup);
			var searchTerms = searchAll(this.searchFilter.groups);
			search(this.searchFilter, searchTerms);
		},

		toggle() {
			this.isAdvanced = !this.isAdvanced;
		},

		save() {
			var searchTerms = searchAll(this.searchFilter.groups);
			var existingKeys = []
			var key = generateUniqueRandomKey(existingKeys);
			this.saved.unshift({
				key: key,
				searchTerms: searchTerms
			});
		},

		startTour() {
			// Instance the tour
			$(function () {
			    $('[data-toggle="popover"]').popover()
			});

			var tour = new Tour({
				steps: [
				// {
				//   element: ".trans-search-bar",
				//   title: "Search Filter",
				//   content: "This is where you can set up your search filter."
				// },
				{
					element: "#show-query",
					title: "Show Query",
					content: "You can view your current query here."
				},
				{
					element: "#configure-query",
					title: "Configure Query",
					content: "You can choose to show or hide advanced filters."
				},
				{
					element: "#heart-query",
					title: "Save/Load Query",
					content: "You can a particular query and/or load a particular query."
				}
			]});

			// Initialize the tour
			tour.init();

			// Start the tour
			tour.start();
		}
	},

	mounted: function() {
		$('.search-menu').on("click.bs.dropdown", function (e) { e.stopPropagation(); e.preventDefault(); });

    var placesData = new PlacesData();
    placesData.initAsync(function(data) {
      this.places = data;
    });

    var options = [];
    for (key1 in this.places.broad_region) {
      options.push({
        id: this.places.broad_region.key1.pk,
        label: this.places.broad_region.key1.broad_region,
      });
    }
    console.log("logging broad_region");
    console.log(options);

		search(this.searchFilter, []);
	},

  created: function() {

  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {
    $menu.menuAim({
        activate: activateSubmenu,
        deactivate: deactivateSubmenu
    });
  },
})
