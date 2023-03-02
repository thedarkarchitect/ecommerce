var updateBtns = document.getElementsByClassName('update-cart')//this class belongs to the button we need to control
//this is similar to python 'self' keyword

for (i=0; i < updateBtns.length; i++){//to get access to all the buttons and know which button we are at at any time 
    updateBtns[i].addEventListener('click', function(){//listening for clicks for all buttons
        var productId = this.dataset.product//this will get product id
        var action = this.dataset.action//this will give it an action 
        console.log('productId: ', productId, 'Action: ', action)
        console.log('User: ', user)

        if (user == 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }

    })
}

function addCookieItem(productId, action){
    console.log('User is not authenticated')

    if (action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item/'

    //we use the fetch API 
    fetch(url, {
        method:'POST',//this is the type of data sent
        headers:{
            'Content-Type':'application/json',//the object
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})//this is the data sent to the backend and it organized and sent as a dictionary
    })

    //return promises response after data is sent
    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data', data)//this is the JsonResponse from the views in updateItem sent after the data is sent to the back end
        location.reload()
    })

}