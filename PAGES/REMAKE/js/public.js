$(function(){
    // 点击菜单按钮切换
    $(".menu").click(function(){
        $(this).toggleClass("active")
        $(".nav").slideToggle()
    })

// 监控
$(window).resize(function(){
    if($(this).width()>1160){
        $(".nav").show();
    }

})
})