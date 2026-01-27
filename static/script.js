const main = document.querySelector('#root')
if (!main) throw Error('App cannot run. No #root found.')

const pages = {}
const defaultPage = 'home'
// const defaultSection = 'home'
const VARS = {
	showClass: 'show',
	activeApp: defaultPage,
	// activeSection: defaultSection
}

function compilePages () {
	const children = Array.from(main.children)
	children.forEach(child => {
		pages[child.id] = {
			sections: {},
			page: child
		}
		const sections = child.querySelectorAll('.section')
		Array.from(sections).forEach(s => pages[child.id].sections[s.id] = s)
	})
}

function activateLinks () {
	const links = document.querySelectorAll('a')
	links.forEach(link => {
		link.onclick = (e) => {
			e.preventDefault()
			const parts = e.currentTarget.pathname.split('/').filter(x => x != '')
			if (parts[0] !== VARS.activeApp) changeApp(parts[0])
			if (parts.length > 1)	changeSection(parts[1])
		}
	})
}

function changeApp (name) {
	hideAllApps()
	pages[name].page.classList.add(VARS.showClass)
	VARS.activeApp = name
}

function changeSection (name) {
	hideAllSections()
	pages[VARS.activeApp].sections[name].classList.add(VARS.showClass)
}

function hideAllSections () {
	const sections = pages[VARS.activeApp].sections
	Object.keys(sections).forEach(key => {
		sections[key].classList.remove(VARS.showClass)
	})
}

function hideAllApps () {
	Object.keys(pages).forEach(key => {
		pages[key].page.classList.remove(VARS.showClass)
	})
}

function appLoad () {
	compilePages()
	activateLinks()
	changeApp(defaultPage)
}

appLoad()