function getRoot (root = 'root') {
	const main = document.querySelector('#' + root)
	if (!main) throw Error('App cannot run. No root element found.')
	return main
}

const pages = {}
const defaultPage = 'home'
const defaultSection = 'home'

const HISTORY = {}

const VARS = {
	showClass: 'show',
	activeApp: defaultPage,
}

// Local Storage keys
const PAGE_LOCATION_KEY = 'fixt_current_page'
const PAGE_SECTION_KEY = 'fixt_current_section'

/**
 * Save current page location to localStorage
 */
function savePageLocation (app, section = null) {
	localStorage.setItem(PAGE_LOCATION_KEY, app)
	if (section) {
		localStorage.setItem(PAGE_SECTION_KEY, section)
	}
}

/**
 * Get saved page location from localStorage
 */
function getSavedPageLocation () {
	const page = localStorage.getItem(PAGE_LOCATION_KEY)
	const section = localStorage.getItem(PAGE_SECTION_KEY)
	return { page: page || defaultPage, section: section || null }
}

/**
 * Clear saved page location
 */
function clearPageLocation () {
	localStorage.removeItem(PAGE_LOCATION_KEY)
	localStorage.removeItem(PAGE_SECTION_KEY)
}

function compilePages (main) {
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
	savePageLocation(name)
}

function changeSection (name) {
	hideAllSections()
	pages[VARS.activeApp].sections[name].classList.add(VARS.showClass)
	savePageLocation(VARS.activeApp, name)
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
	const main = getRoot('root')
	compilePages(main)
	activateLinks()
	
	// Check if user is authenticated
	const isAuthenticated = API.isAuthenticated()
	
	if (!isAuthenticated) {
		// If not authenticated, always show login page
		changeApp('home')
		changeSection('home')
	} else {
		// If authenticated, restore previous page location
		const savedLocation = getSavedPageLocation()
		changeApp(savedLocation.page)
		if (savedLocation.section && pages[savedLocation.page].sections[savedLocation.section]) {
			changeSection(savedLocation.section)
		}
	}
}

appLoad()
