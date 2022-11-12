// https://stackoverflow.com/questions/35095455/make-the-same-word-link-to-the-same-page-every-time-it-appears

var labels_and_links = {
	"Universität Zürich": "https://en.wikipedia.org/wiki/University_of_Zurich",
	"PSI": "https://www.psi.ch/de",
	"Universidad de Buenos Aires": "https://en.wikipedia.org/wiki/University_of_Buenos_Aires",
	"CMS experiment": "https://cms.cern/",
	"LHC": "https://home.cern/science/accelerators/large-hadron-collider",
	"INTI": "https://www.inti.gob.ar",
	"Fermilab": "https://www.fnal.gov/",
	"UNSAM": "http://www.unsam.edu.ar/",
	"skipper CCD": "https://arxiv.org/abs/1706.00028",
	"CERN": "https://home.web.cern.ch/",
}

for (const [label, link] of Object.entries(labels_and_links))
	document.body.innerHTML = document.body.innerHTML.replaceAll(label, `<a href=${link}>${label}</a>`);

