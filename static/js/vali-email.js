window.onload=function() {
    const emailfield=document.getElementById("emailf");
    const emailfeed=document.getElementById("emailfeedbackarea");
    const usernamefeed=document.getElementById("usernamefeedbackarea");
    const showps=document.getElementById("show");
    const ps=document.getElementById("passwordf");
    const username=document.getElementById("usernamef");

    show.addEventListener("click",()=>{
        if(showps.textContent==="Show"){
            showps.textContent="Hide";
            ps.setAttribute("type","text");
        }
        else{
            showps.textContent="Show";
            ps.setAttribute("type","password");
        }
    });
    username.addEventListener("keyup",(e)=>{
        const value = e.target.value;
        usernamefeed.classList.remove("is-valid");
        usernamefeed.style.display="none";
        if(value.length>0){
            fetch('/auth/valid-username/',{
                method: "POST",
                body: JSON.stringify({username:value}),})
                .then((res)=>res.json()).then((data)=>{
                    console.log(data);
                    if(data.username_error){
                        usernamefeed.classList.add("is-valid");
                        usernamefeed.style.display="block";
                        usernamefeed.innerHTML=`<p>${data.username_error}</p>`;
                    }
                })
            }
        })
    emailfield.addEventListener("keyup",(e)=>{
        const val=e.target.value;
        emailfeed.classList.remove("is-valid");
        emailfeed.style.display="none";
        if(val.length>0){
            fetch('/auth/valid-email/',{
            method: 'POST',
            body:JSON.stringify({email:val}),})
            .then((res)=>res.json()).then((data)=>{
                console.log(data);
                if(data.email_error){
                    emailfeed.classList.add("is-valid");
                    emailfeed.style.display="block";
                    emailfeed.innerHTML=`<p>${data.email_error}</p>`;
                }
            })
    }
        })
}
