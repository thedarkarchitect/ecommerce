var updateBtns = document.getElementsByClassName('update-cart')//this class belongs to the button we need to control
//this is similar to python 'self' keyword

for (i=0; i < updateBtns.length; i++){//to get access to all the buttons and know which button we are at at any time 
    updateBtns[i].addEventListener('click', function(){//listening for clicks for all buttons
        var productId = this.dataset.product//this will get product id
        var action = this.dataset.action//this will give it an action 
        console.log('productId: ', productId, 'Action: ', action)
        console.log('User: ', user)

        if (user == 'AnonymousUser'){
            console.log('User is not authenticated')
        }else{
            updateUserOrder(productId, action)
        }

    })
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