// module.exports = {
// 	content: ['./src/**/*.{html,js,svelte,ts}'],
// 	theme: {
// 		extend: {}
// 	},
// 	plugins: []
// };
module.exports = {
	// add this section
	purge: ['./src/**/*.html', './src/**/*.svelte'],
	darkMode: false,
	theme: {
		extend: {}
	},
	variants: {
		extend: {}
	},
	plugins: []
};
