


/* for search engen */
 let serachEng = document.querySelector('.forhover')
 let mybtn=document.querySelector('.mybtn');
serachEng.onclick =function(){
    serachEng.style.backgroundColor='rgb(36, 45, 32)';
    serachEng.style.color='darkgreen';  
    mybtn.style.backgroundColor='rgb(36, 45, 32)';
    mybtn.style.color='darkgreen';  
}
/*-------------- endfor search engen  ---------------*/

/* for navbar */
/* 1- for alphan in navbar using scroll and pages  */
let getNavAtt=document.querySelector('.navbar');
let bodyTemp=document.querySelectorAll('.html');
let getNavClasses=getNavAtt.className;
bodyTemp.forEach(function(e){
	e.onscroll=function(){
        a=window.scrollY;
        function track(e) {
            if(e.pageY-a>0 && e.pageY-a<95  )
            getNavAtt.className=getNavClasses;
        }
        addEventListener("mousemove", track, false);
		a=window.scrollY;
        if(a>100){
          //  console.log(a);  to see scrolling 
            getNavAtt.className=getNavClasses+ 'handlerScroll';
        }
        else if(a<10000)
        {
            getNavAtt.className=getNavClasses;
        }

	};
});
/*-------------- endfor navbar  ---------------*/