$(function (){
   $("#captcha-btn").click(function (event){
       var email = $("input[name='email']").val();
       alert(email);
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function (result){
                var code = result['code'];
                if(code == 200){
                    alert("邮箱验证码发送成功！")
                }else{
                    alert(result['message'])
                }
            },
            fail:function (error){
                console.log(error);
            }
        })
   });
});