
// Staticke stvari, promenljive relevantne za ovaj fajl
const tag = []
const addTagButton = document.querySelector("#addTag")
const submitButton = document.querySelector("#submitButton")

submitButton.addEventListener("click",beforeSubmit)
addTagButton.addEventListener("click",addTag)

// Funkcija koju pozivamo pre submit-ovanja forme, koja ce da zapakuje tagove odvojene zarezom u textinput
// Koje cemo moci posle kroz backend lako da parsiramo
function beforeSubmit()
{
    let taginput = document.querySelector("#taginput")
    taginput.value = tag
}


// Funkcija koja stvara i dodaje HTML element tag-a
function addTag()
{

    let taginput = document.querySelector("#taginput")
    let text = taginput.value

    if(text == "")
    {
        return;
    }
    tag.push(text)
    let tagdiv = document.querySelector("#tags")
    let new_tag = createTag(text)
    tagdiv.appendChild(new_tag)
    taginput.value = ""


}

// Funkcija koja kreira sam tag
function createTag(text)
{
    let new_tag = document.createElement("span")
    new_tag.className = "badge"
    new_tag.style = "background-color: #b7472a; color: beige"
    new_tag.innerHTML = text;
    new_tag.style.marginLeft = "2px"
    new_tag.style.marginRight = "2px"

    return new_tag
}