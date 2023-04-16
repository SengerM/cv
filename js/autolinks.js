// https://stackoverflow.com/questions/35095455/make-the-same-word-link-to-the-same-page-every-time-it-appears

var labels_and_links = {
	"LHC": "https://home.cern/science/accelerators/large-hadron-collider",
	"skipper CCD": "https://arxiv.org/abs/1706.00028",
}

for (const [label, link] of Object.entries(labels_and_links))
	document.body.innerHTML = document.body.innerHTML.replaceAll(label, `<a href=${link}>${label}</a>`);

