let lightMode = false
let pageMode = document.getElementById('page-mode')
let myBody = document.getElementById('body')
let pageModeText = document.getElementById('page-mode-text')
let icon = document.querySelector('#page-mode > a > i')
let titles = document.querySelectorAll('.fashion_taital')
let boxMain = document.querySelectorAll('.box_main')
let boxText = document.querySelectorAll('.shirt_text')
let priceText = document.querySelectorAll('.price_text span')
let discountSpan = document.querySelectorAll('#discounte_span')
let singleProductPage = document.querySelectorAll('.product-page p')
let singleProductPageSpan = document.querySelectorAll('.product-page p span')
let tagsSpan = document.querySelectorAll('.product-page p a')





pageMode.addEventListener('click', e=>{



body.classList.toggle('light-body')
body.classList.toggle('dark-body')

icon.classList.toggle('fa-moon-o')
icon.classList.toggle('fa-sun-o')


if (body.classList[0] == 'dark-body') {

	pageModeText.innerText = 'لایت مود' ;




	titles.forEach(h1 => {

		h1.style.color = 'white'
	})


	boxMain.forEach(box =>{
		box.style.backgroundColor = '#ffffff'
	})

	boxText.forEach(text =>{

		text.style.color = '#30302e'
	})

	priceText.forEach(text => {

		text.style.color = '#30302e'
	})


	singleProductPage.forEach(p =>{

		p.style.backgroundColor = 'white'

	})
		singleProductPageSpan.forEach(span =>{

		span.style.color = 'black'

	})



	tagsSpan.forEach(tag =>{

		tag.style.color = 'blue'

	})
	// discountSpan.forEach(span =>{

	// 	span.style.backgroundColor = 'red'
	// })




}



else {
	pageModeText.innerText = 'دارک مود'


	titles.forEach(h1 => {

		h1.style.color = 'black'
	})

	boxMain.forEach(box =>{
		box.style.backgroundColor = '#3c3f41'
	})

	boxText.forEach(text =>{

		text.style.color = '#ffffff'
	})
	priceText.forEach(text => {

		text.style.color = '#ffffff'
	})
// discountSpan.forEach(span =>{

// 		span.style.backgroundColor = 'black'
// 	})

		singleProductPage.forEach(p =>{

		p.style.backgroundColor = '#252525'

	})
			singleProductPageSpan.forEach(span =>{

		span.style.color = 'white'

	})

			tagsSpan.forEach(tag =>{

		tag.style.color = 'red'

	})

}



})