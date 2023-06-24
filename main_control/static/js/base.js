let slide = true;
const ele = document.getElementsByClassName('container2');
ele[0].addEventListener('click',function (){
    if (slide){
        var show = document.getElementsByClassName("slide");
        show[0].style.display = "inline";
        slide = false
    }
    else{
        slide = true
        var show = document.getElementsByClassName("slide");
        show[0].style.display = "none";
    }
})
