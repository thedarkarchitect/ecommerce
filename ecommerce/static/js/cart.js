var updateBtns = document.getElementsByClassName('update-cart')//this class belongs to the button we need to control
//this is similar to python 'self' keyword

for (i=0; i < updateBtns.length; i++){//to get access to all the buttons and know which button we are at at any time 
    updateBtns[i].addEventListener('click', function(){//listening for clicks for all buttons
        var productId = this.dataset.product//this will get product id
        var action = this.dataset.action//this will give it an action 
        console.log('productId: ', productId, 'Action: ', action)

        console.log('User: ', user)
        if (user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            console.log('User is logged in, sending data')
        }

    })
}