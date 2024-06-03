
   let test =false;
   let e=0
    $(document).ready(function(){
  $(document).scroll(function(){
    if(155 <window.scrollY && e==0 &&window.scrollY<580){
        $('.titleFA').animate({width:'300px',});
        e=e+1;
        console.log(1);
    }

   
   else if(155 >window.scrollY && e==1  ){ 
       $('.titleFA').animate({width:'0px',});
     console.log(2);
        e=0;
    }
 
    else if(580<window.scrollY && e==1) {
        $('.titleFA').animate({width:'0px',});
        e=0;
        console.log(2);
        }
  
    
   // console.log(e);
  });

});

 


