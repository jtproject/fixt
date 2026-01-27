const main = document.querySelector('#root')
if (!main) throw Error('App cannot run. No #root found.')

const pages = {}
const defaultPage = 'home'
const VARS = {
	showClass: 'show'
}

function compilePages () {
	const children = Array.from(main.children)
	children.forEach(child => pages[child.id] = child)
}

function activateLinks () {
	const links = document.querySelectorAll('a')
	links.forEach(link => {
		link.onclick = (e) => {
			e.preventDefault()
			changeApp(e.target.pathname.slice(1))
		}
	})
}

function changeApp (name) {
	hideAllApps()
	pages[name].classList.add(VARS.showClass)
}

function hideAllApps () {
	Object.keys(pages).forEach(key => {
		pages[key].classList.remove(VARS.showClass)
	})
}

function appLoad () {
	compilePages()
	activateLinks()
	changeApp(defaultPage)
}

appLoad()