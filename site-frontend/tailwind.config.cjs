module.exports = {
	purge: [
		"./src/**/*.html",
		"./src/**/*.svelte",
		"./src/**/*.{html,js}",
		"./node_modules/tw-elements/dist/js/**/*.js"
	],
	darkMode: "media",
	theme: {
		extend: {
			flexGrow: {
				2: 2
			},
			maxWidth: {
				screen: "100vw",
				"screen-1/3": "33vw",
				"screen-2/3": "60vw",
				"screen-90": "90vw"
			},
			minWidth: {
				"screen-1/3": "33vw",
				"screen-2/3": "66vw"
			}
		}
	},
	variants: {
		extend: {}
	},
	plugins: [require("tw-elements/dist/plugin")]
};
