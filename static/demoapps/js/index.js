$(function(){
     var li = $('.navi li');
     li.each(function(){
        var this_li = this;
       $(this_li).find('a').click(function(){
         if($(this_li).hasClass('c-open')){
           $(this_li).find('ul').slideUp(400);
           $(this_li).removeClass('c-open');
         }else{
           $(this_li).find('ul').slideDown(400);
           $(this_li).addClass('c-open');
         }
       })
     });
});

$(".has_submenu").each(function(){
    var t = this;
    $(t).find('li').each(function () {
        var a = $(this).find("a:eq(0)");
        if (window.location.pathname==$(a).attr('href')){
            $(t).addClass('open');
            $(this).addClass("active");
            $(this).find("a:eq(0)").addClass('active')
        }
    })

});

// 提示框
function tooltip(content) {
    var d=dialog({
        width: 440,
        title: "提示",
        content: '<div class="king-notice3 king-notice-fail">'+
            '<div class="king-notice-text">'+
                    content.slice(0, 300) +
            '</div>'+
        '</div>',
        ok: function() {
                // do something
            }
    });
    
    d.show();
}

function response_500_alert(res) {
  var error = res.responseText.slice(0, 100);
  if (error.search("ConnectionError") != -1){
    tooltip("JenkinsServer没有启动")
  }else if(error.search("Authentication failed.") != -1){
    tooltip("登录认证失败，请检查秘钥文件是否正确")
  }
  else {
    tooltip(error)
  }
}