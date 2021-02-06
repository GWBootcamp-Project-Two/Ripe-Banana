/*var request = new XMLHttpRequest()
var query = 

request.open('GET', 'https://ripe-bananas-6.herokuapp.com/api/lookup/', true)
request.onload = function () {
  // Begin accessing JSON data here
  var data = JSON.parse(this.response)

  if (request.status >= 200 && request.status < 400) {
    data.forEach((item) => {
      console.log(item.title)
      console.log(item.description)
      console.log(item.genre)
      console.log(item.maturity)
      console.log(item.services)
    })
  } else {
    console.log('error')
  }
}

request.send()*/