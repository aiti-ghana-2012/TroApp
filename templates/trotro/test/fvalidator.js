
 function fvalidator(form)
 {
   var vname=/^([A-Za-z]{1,10})(\-)?(\s)?([A-Za-z]{1,10})?$/;
   var vpass = /^[3]+$/;
   var errors=[];    
    
    var cname= form.name.value;
    var cpass =form.pword.value;
    
    if(!vname.test(cname))
    errors[errors.length]="invalid username\n";
    
     if(!vpass.test(cpass))
    errors[errors.length]="invalid password\n";
 
 
     if(errors.length>0)
   {
     reportErrors(errors);
     return false;
     
   }      
 
 return true;
 }

function reportErrors(errors)
{
 var msg = "invalid input found in: \n"; 
for(var i=0; i<errors.length; i++) 
{
  var numErrors= i+1;
  msg += + "\n" + numErrors + ". " + errors[i] ;
}

alert(msg)
}




