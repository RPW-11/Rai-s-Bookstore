var addBtns = document.getElementsByClassName('add-cart-btn')
for(var i=0; i<addBtns.length; i++){
    addBtns[i].addEventListener('click', function(){
        var bookId = this.dataset.book
        var action = this.dataset.action
        console.log('bookId: ', bookId, 'action: ', action)
        console.log('user', user)
        
        if(user == 'AnonymousUser'){
            console.log('User not logged in')
        }
        else{
            updateUserOrder(bookId, action)
        }
    })  
}

function updateUserOrder(bookId, action){
    console.log('User logged in ')
    var url = '/update-item'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'bookId':bookId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data: ', data)
        location.reload()
    })
}