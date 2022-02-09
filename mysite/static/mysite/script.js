const getCookie = name => {
    if(!document.cookie) return false;
    return decodeURIComponent(
        document.cookie.split(';').find(cookie => cookie.trim().substring(0, name.length + 1) === (name + '='))
        .substring(name.length + 1)
    );
    }
//Csrf token kinyerése egy cookie-ból
const csrfToken = getCookie('csrftoken');
document.querySelector("#submitButton").addEventListener("click", async e => {
try { 
    const textBoxValue = document.getElementById('text').value;
    if(textBoxValue === ''){
        $('<tr><td class = "other-message-warning">Kérlek írj valamit a textboxba!</td><td></td></tr>').insertBefore("#textBoxosSor");
    }
    else{
        $('<tr><td></td><td class = "my-message">'+textBoxValue+'</td></tr>').insertBefore("#textBoxosSor");
        document.getElementById('text').value = '';
        //POST request küldés
        const response = await fetch(".", {
        method: 'POST',
        headers: {'X-CSRFToken': csrfToken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({data: textBoxValue})
        });
        if(!response.ok) throw new Error(response);
        const data = await response.text();//Vissza érkező httpresponse tartalmának eltárolása
        //JQuery-vel oldalhoz addolás
        $('<tr><td class = "other-message">'+data+'</td><td></td></tr>').insertBefore("#textBoxosSor");
    }
} catch(err){
    console.error(err);
    return;
}
}, {passive: true});